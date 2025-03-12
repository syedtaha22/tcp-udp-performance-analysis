import socket
import threading
import time

'''
TCP Server for Performance Testing

This script implements a TCP server that handles a single client sending an increasing number 
of messages. It logs communication, records timestamps, and allows controlled shutdown via 
a "STOP" message.

Key Features:
    - Handles a single client sending multiple messages.
    - Logs communication timestamps for latency analysis.
    - Gracefully shuts down when receiving the "STOP" message.

Networking Concepts:
    - socket.AF_INET: Uses IPv4 addressing.
    - socket.SOCK_STREAM: Establishes a TCP connection.
    - socket.SO_REUSEADDR: Allows immediate socket reuse after shutdown.
    - socket.accept(): Waits for client connections.
'''

SERVER_ID = "S"  # Identifier for the server
STOP_SIGNAL = "STOP"  # Special message to terminate the server
LOG_FILE = "tcp_log.txt"  # Log file for storing communication records


class TCPServer:
    '''
    Implements a TCP server handling a single client sending increasing numbers of messages.

    Attributes:
        host (str): Server hostname or IP address.
        port (int): Server port number.
        server_socket (socket): Main socket for handling connections.
        running (bool): Flag to control server execution.
    '''

    def __init__(self, host="localhost", port=12345):
        '''
        Initializes the TCP server.

        Args:
            host (str, optional): Server hostname (default: "localhost").
            port (int, optional): Port number to listen on (default: 12345).
        '''
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow quick restarts
        self.running = True  # Flag to control server execution

    def start(self):
        '''
        Starts the TCP server and listens for incoming client connections.
        '''
        self.server_socket.bind((self.host, self.port))  # Bind socket to host and port
        self.server_socket.listen(1)  # Allow only one client at a time
        print(f"TCP Server [{SERVER_ID}] started on {self.host}:{self.port}")

        # Create (or clear) the log file
        with open(LOG_FILE, "w") as log:
            log.write("TCP Communication Log\n")

        while self.running:
            try:
                # Accept a single client connection
                conn, addr = self.server_socket.accept()
                print(f"Client connected from {addr}")

                # Handle the client in a separate thread
                threading.Thread(target=self.handle_client, args=(conn,)).start()

            except OSError:
                break  # Server socket was closed, exit the loop

        print("TCP Server shutting down.")
        self.server_socket.close()  # Close the server socket

    def handle_client(self, conn):
        '''
        Handles incoming messages from a connected client.

        Args:
            conn (socket): The client socket.
        '''
        with open(LOG_FILE, "a") as log:
            while True:
                try:
                    data = conn.recv(1024)  # Receive message from the client
                    if not data:
                        break  # Client disconnected

                    message = data.decode()  # Decode received message
                    sender_id, receiver_id, text = message.split(":", 2)  # Parse message format

                    log.write(f"{sender_id} -> {SERVER_ID}: {text}\n")

                    if text == STOP_SIGNAL:
                        log.write(f"{sender_id} sent STOP. Server shutting down.\n")
                        conn.sendall(b"Server shutting down...")  # Acknowledge shutdown
                        self.shutdown()
                        return

                    # Fixed response format for consistency
                    response = f"{SERVER_ID} -> {sender_id}: Received '{text}'"
                    conn.sendall(response.encode())  # Send response to the client

                except Exception as e:
                    log.write(f"Error handling client: {e}\n")  # Log errors
                    break  # Exit loop on exception

        conn.close()  # Close client connection

    def shutdown(self):
        '''
        Gracefully shuts down the server.
        '''
        self.running = False
        self.server_socket.close()  # Close the main server socket


if __name__ == "__main__":
    server = TCPServer()
    server.start()  # Launch the server
