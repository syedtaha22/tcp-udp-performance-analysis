import socket
import threading

'''

TCP Server for Performance Testing

This script implements a TCP server that handles client connections. It logs communication, records timestamps,
and allows controlled shutdown via a "STOP" message.

Key Features:
    - Handles client connections in separate threads.
    - Logs communication timestamps for latency analysis.
    - Gracefully shuts down when receiving the "STOP" message.

Networking Concepts:
    - socket.AF_INET: Uses IPv4 addressing.
    - socket.SOCK_STREAM: Establishes a TCP connection.
    - socket.SO_REUSEADDR: Allows immediate socket reuse after shutdown.
    - socket.accept(): Waits for client connections.
'''

SERVER_ID = "Server"  # Identifier for the server
STOP_SIGNAL = "STOP"  # Special message to terminate the server

class TCPServer:
    '''
    TCP Server class that handles client connections and logs communication.

    Attributes:
        host (str): Server hostname or IP address.
        port (int): Server port number.
        server_socket (socket): Main socket for handling connections.
        clients (dict): Dictionary storing active client connections.
        lock (threading.Lock): Ensures thread-safe access to shared resources.
        running (bool): Flag to control server execution.
        log_file (str): File to log communication records
    '''

    def __init__(self, host: str = "localhost", port: int = 12345, log_file: str = "tcp_log.txt"):
        '''
        Initializes the TCP server.

        Args:
            host (str, optional): Server hostname (default: "localhost").
            port (int, optional): Port number to listen on (default: 12345).
            log_file (str, optional): File to log communication records (default: "tcp_log.txt").
        '''
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow quick restarts

        # # Allow for larger buffer sizes to handle high-speed connections
        # self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
        # self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)

        self.clients = {}  # Dictionary to store connected clients
        self.lock = threading.Lock()  # Lock for thread-safe operations
        self.running = True  # Flag to control server execution
        self.log_file = log_file  # File to log communication records

    def start(self):
        '''
        Starts the TCP server and listens for incoming client connections.
        '''
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(50)  # Allow up to 50 concurrent connections
        print(f"TCP Server [{SERVER_ID}] started on {self.host}:{self.port}")

        with open(self.log_file, "w") as log:
            log.write("TCP Communication Log\n")

        # Handle incoming messages
        self.handle_messages()

    def handle_messages(self):
        '''
        Main loop to handle incoming messages from clients.
        '''
        while self.running:
            try:
                # Accept new client connections
                conn, addr = self.server_socket.accept()
                with self.lock:
                    client_id = f"C[{len(self.clients) + 1}]"  # Assign a unique ID to the client
                    self.clients[client_id] = conn  # Store client connection

                # Handle the client in a separate thread
                threading.Thread(target=self.handle_client, args=(conn, client_id)).start()

            except OSError:
                break  # Server socket was closed, exit the loop

        print("TCP Server shutting down.")
        self.server_socket.close()  # Close the server socket

    def handle_client(self, conn, client_id):
        '''
        Handles incoming messages from a connected client.

        Args:
            conn (socket): The client socket.
            client_id (str): Unique identifier for the client.
        '''
        with open(self.log_file, "a") as log:
            while True:
                try:
                    data = conn.recv(2048)  # Receive data from the client
                    if not data:
                        break  # Client disconnected

                    message = data.decode()  # Decode received message
                    sender_id, receiver_id, text = message.split(":", 2)  # Parse message format

                    if text == STOP_SIGNAL:
                        log.write(f"{sender_id} sent STOP. Server shutting down.\n")
                        conn.sendall(b"Server shutting down...")  # Acknowledge shutdown
                        self.shutdown()
                        return

                    # Fixed response format for consistency
                    response = f"Received: {text}"
                    conn.sendall(response.encode())  # Send response to the client

                    log.write(f"{SERVER_ID} -> {sender_id}: {response}\n")

                except Exception as e:
                    log.write(f"Error handling {client_id}: {e}\n")  # Log errors
                    break  # Exit loop on exception

        # Remove client from the active clients list
        with self.lock:
            if client_id in self.clients:
                del self.clients[client_id]

        conn.close()  # Close client connection

    def shutdown(self):
        '''
        Gracefully shuts down the server.
        '''
        self.running = False
        self.server_socket.close()  # Close the main server socket