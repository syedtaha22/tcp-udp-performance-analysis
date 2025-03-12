import socket

"""
TCP Server for Receiving and Logging Messages

This server listens for incoming TCP connections, receives messages from clients, and logs them.

Functionality:
    - Binds to `localhost:12345` and listens for incoming connections.
    - Accepts a single client connection and processes messages.
    - Responds to each received message with an acknowledgment.
    - Logs all received messages to `tcp_log.txt`.

Networking Methods Used:
    - AF_INET: Specifies IPv4 addressing.
    - SOCK_STREAM: Uses TCP for reliable, connection-oriented communication.
    - socket.bind(): Binds the server to a specific address and port.
    - socket.listen(): Allows the server to accept incoming connections.
    - socket.accept(): Blocks execution until a client connects.
    - socket.recv(): Reads incoming data from the client.
    - socket.sendall(): Sends an acknowledgment back to the client.
    - socket.close(): Closes the connection after communication is complete.
"""

class TCPServer:
    """
    A TCP server that listens for incoming messages, acknowledges them, and logs the data.

        - Binds to `localhost:12345`
        - Accepts a connection from a client.
        - Processes messages in a loop until the client disconnects.
        - Writes received messages to a log file.
    """

    def __init__(self):
        """Initializes the TCP server, binds it to a port, and starts listening for connections."""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("localhost", 12345))
        self.server.listen(5)  # Allows up to 5 pending connections in the queue

    def receive_messages(self):
        """
        Waits for a client connection, receives messages, and logs them.

            - Accepts a client connection.
            - Reads data in 1024-byte chunks.
            - Sends an acknowledgment response.
            - Logs received messages to `tcp_log.txt`.
            - Closes the connection when the client disconnects.
        """

        conn, addr = self.server.accept()  # Blocks until a client connects

        with open("tcp_log.txt", "w") as log:
            while True:
                data = conn.recv(1024)  # Reads up to 1024 bytes from the client
                if not data: # If no data is received, the client has disconnected
                    break
                conn.sendall(b"Received: " + data) # Send an acknowledgment back to the client
                log.write(f"Received: {data.decode()}\n") # Log the received message
        
        conn.close()  # Close client connection
        self.server.close()  # Shut down the server

if __name__ == "__main__":
    server = TCPServer()
    server.receive_messages()

