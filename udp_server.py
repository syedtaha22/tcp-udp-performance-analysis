import socket
import random

SERVER_ID = "Server"  # Unique identifier for the server
STOP_SIGNAL = "STOP"  # Command to stop the server

'''
UDP Server for Logging Communication and Simulating Packet Loss

This server listens for incoming messages from clients, assigns unique client IDs,
logs communication details, and simulates packet loss based on a specified probability.

Key Networking Methods Used:
    - socket.AF_INET: Specifies IPv4 addressing.
    - socket.SOCK_DGRAM: Indicates UDP as the transport protocol.
    - socket.bind(): Binds the server to a specific IP address and port.
    - socket.recvfrom(): Receives data from a client.
    - socket.sendto(): Sends data to a client.
    - random.random(): Generates a random float in the range [0.0, 1.0).
'''

class UDPServer:
    """ 
    UDP server that listens for incoming messages, assigns client IDs, and logs communication.

    Attributes:
        host (str): The IP address or hostname to bind the server.
        port (int): The port number for the server.
        packet_loss (float): Probability (0-1) of simulating packet loss.
        server_socket (socket): The UDP socket for receiving/sending data.
        clients (dict): Maps client addresses to unique numerical IDs.
        running (bool): Controls the server loop.
        log_file (str): The file to log communication records.
    """

    def __init__(self, host="localhost", port=12345, packet_loss=0.05, log_file="udp_log.txt"):
        """
        Initializes the UDP server.

        Args:
            host (str): The IP address or hostname to bind the server. Default is "localhost".
            port (int): The port number for the server. Default is 12345.
            packet_loss (float): Probability (0-1) of simulating packet loss. Default is 0.01.
            log_file (str): The file to log communication records. Default is "udp_log.txt".

        """
        self.host = host
        self.port = port
        self.packet_loss = packet_loss
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket
        self.running = True
        self.client_counter = 1  # Unique client ID counter (C[1], C[2], ...)
        self.log_file = log_file


    def start(self):
        """
        Starts the UDP server, listens for incoming messages, and assigns client IDs.
        """

        # Bind the server to the specified host and port
        self.server_socket.bind((self.host, self.port))
        print(f"UDP Server started on {self.host}:{self.port}...")
    
        # Create (or clear) the log file when the server starts
        with open(self.log_file, "w") as log:
            log.write("UDP Communication Log\n")

        # Handle incoming messages
        self.handle_messages()

    def handle_messages(self):
        """
        Receives and processes messages from clients, logging communication details.
        """
        # Main loop to handle incoming messages
        with open(self.log_file, "a") as log:
            while self.running:
                try:
                    data, addr = self.server_socket.recvfrom(4096)
                except ConnectionResetError:
                    continue  # Ignore and keep running

                message = data.decode().strip() # Decode and remove extra whitespace

                if not message: # Ignore empty messages
                    continue

                sender_id, receiver_id, text = message.split(":", 2)  # Parse message format

                if text == STOP_SIGNAL:  # Check for stop signal
                    self.running = False  # Stop the server
                    break

                if random.random() > self.packet_loss:  # Packet successfully received
                    response = f"Received {text}"
                    self.server_socket.sendto(response.encode(), addr)

                    # Log sent response
                    log.write(f"{SERVER_ID} -> {sender_id}: {response}\n")
                else:
                    # Log lost packet (no response sent)
                    log.write(f"Packet loss: {sender_id} -> {SERVER_ID}: {addr}\n")

        # Server is shutting down
        print("UDP Server shutting down.")
        self.server_socket.close()  # Close the UDP socket