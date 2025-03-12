import socket
import random
import threading

'''
UDP Server for Load Testing

This script implements a multi-threaded UDP server that receives messages from clients,
logs communication, and simulates packet loss before sending acknowledgments.

Key Features:
    - Listens on localhost at port 12345.
    - Assigns unique client IDs for tracking communication.
    - Logs messages sent and received between clients and the server.
    - Stops gracefully when it receives the "STOP" message.

Networking Concepts:
    - socket.AF_INET: Specifies IPv4 addressing.
    - socket.SOCK_DGRAM: Indicates UDP as the transport protocol.
    - socket.recvfrom(): Receives data from a client along with the sender's address.
    - socket.sendto(): Sends a response to the client.
    - threading.Thread: Enables concurrent client handling.
'''


# Constants
SERVER_ID = "S"          # Identifier for the server in logs
STOP_SIGNAL = "STOP"     # Message to signal server shutdown
LOG_FILE = "udp_log.txt" # Log file to record communication


class UDPServer:
    """A multi-threaded UDP server with simulated packet loss and logging."""

    def __init__(self, host="localhost", port=12345, packet_loss=0.01):
        """
        Initializes the UDP server.

        Parameters:
        - host (str): The IP address or hostname to bind the server.
        - port (int): The port number for the server.
        - packet_loss (float): Probability (0-1) of simulating packet loss.

        Attributes:
        - server_socket (socket): The UDP socket for receiving/sending data.
        - clients (dict): Maps client addresses to unique numerical IDs.
        - lock (threading.Lock): Ensures thread-safe logging.
        - running (bool): Controls the server loop.
        - client_counter (int): Tracks unique client ID assignment.
        """
        self.host = host
        self.port = port
        self.packet_loss = packet_loss
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket
        self.clients = {}  # Dictionary to track client IDs
        self.lock = threading.Lock()  # Lock for thread-safe access to shared resources
        self.running = True
        self.client_counter = 1  # Unique client ID counter (C[1], C[2], ...)

    def start(self):
        """Starts the UDP server, listens for incoming messages, and assigns client IDs."""
        
        # Bind the server to the specified host and port
        self.server_socket.bind((self.host, self.port))
        print(f"UDP Server started on {self.host}:{self.port}...")

        # Create (or clear) the log file when the server starts
        with open(LOG_FILE, "w") as log:
            log.write("UDP Communication Log\n")

        # Main loop to handle incoming messages
        while self.running:
            try:
                # Receive message from a client (up to 1024 bytes)
                data, addr = self.server_socket.recvfrom(1024)
                message = data.decode()  # Decode and remove extra whitespace

                # Ignore empty messages
                if not message:
                    continue

                # Check for stop signal
                if message == STOP_SIGNAL:
                    self.running = False
                    break  # Exit the loop to stop the server

                # Assign unique client ID if it's a new client
                with self.lock:
                    if addr not in self.clients:
                        self.clients[addr] = f"C[{self.client_counter}]"  # Assign C[num] ID
                        self.client_counter += 1  # Increment counter for next client

                # Handle the message in a new thread to avoid blocking
                threading.Thread(target=self.handle_client, args=(message, addr)).start()

            except Exception as e:
                print(f"Server error: {e}")

        # Server is shutting down
        print("UDP Server shutting down.")
        self.server_socket.close()  # Close the UDP socket

    def handle_client(self, message, addr):
        """
        Handles a client's message, logs communication, and simulates packet loss.

        Parameters:
        - message (str): The received message from the client.
        - addr (tuple): The address (IP, port) of the client.
        """

        # Extract client ID
        client_id = self.clients.get(addr, "Unknown")

        sender_id, receiver_id, text = message.split(":", 2)  # Parse message format

        # Log received message
        with self.lock:
            with open(LOG_FILE, "a") as log:
                log.write(f"{client_id} -> {SERVER_ID}: {text}\n")

        # Check if the message is a stop command
        if text == STOP_SIGNAL:
            self.running = False  # Stop server loop
            self.server_socket.close()  # Close the server socket
            return  # Exit the function without responding

        # Simulate packet loss
        if random.random() > self.packet_loss:  # Packet successfully received
            response = f"Received '{text}'"
            self.server_socket.sendto(response.encode(), addr)  # Send Response

            # Log sent response
            with self.lock:
                with open(LOG_FILE, "a") as log:
                    log.write(f"{SERVER_ID} -> {client_id}: {response}\n")
        else:
            # Log lost packet (no response sent)
            with self.lock:
                with open(LOG_FILE, "a") as log:
                    log.write(f"{SERVER_ID} -> {client_id}: Packet lost\n")



# Run the server if executed as a script
if __name__ == "__main__":
    server = UDPServer()
    server.start()
