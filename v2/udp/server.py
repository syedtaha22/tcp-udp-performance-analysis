import socket
import random
import time

'''
UDP Server for Performance Testing

This script implements a UDP server that handles a single client sending an increasing number 
of messages. It logs communication, records timestamps, and simulates packet loss.

Key Features:
    - Handles a single client sending multiple messages.
    - Logs communication timestamps for latency analysis.
    - Simulates packet loss before responding to clients.
    - Gracefully shuts down when receiving the "STOP" message.

Networking Concepts:
    - socket.AF_INET: Uses IPv4 addressing.
    - socket.SOCK_DGRAM: Uses UDP as the transport protocol.
    - socket.recvfrom(): Receives data from a client along with the sender's address.
    - socket.sendto(): Sends a response to the client.
'''

SERVER_ID = "S"  # Identifier for the server in logs
STOP_SIGNAL = "STOP"  # Message to signal server shutdown
LOG_FILE = "udp_log.txt"  # Log file for communication records


class UDPServer:
    """A UDP server that handles a single client sending multiple messages."""

    def __init__(self, host="localhost", port=12345, packet_loss=0.1):
        """
        Initializes the UDP server.

        Parameters:
        - host (str): The IP address or hostname to bind the server.
        - port (int): The port number for the server.
        - packet_loss (float): Probability (0-1) of simulating packet loss.
        """
        self.host = host
        self.port = port
        self.packet_loss = packet_loss
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket
        self.running = True  # Server running flag

    def start(self):
        """Starts the UDP server, listens for incoming messages, and processes them sequentially."""
        
        # Bind the server to the specified host and port
        self.server_socket.bind((self.host, self.port))
        print(f"UDP Server started on {self.host}:{self.port}...")

        # Create (or clear) the log file when the server starts
        with open(LOG_FILE, "w") as log:
            log.write("UDP Communication Log\n")

        # Main loop to handle incoming messages
        while self.running:
            try:
                # Receive message from the client (up to 1024 bytes)
                data, addr = self.server_socket.recvfrom(1024)
                message = data.decode().strip()  # Decode and remove extra whitespace

                # Ignore empty messages
                if not message:
                    continue

                # Check for stop signal
                if message == STOP_SIGNAL:
                    self.running = False
                    break  # Exit the loop to stop the server

                # Handle the received message
                self.handle_message(message, addr)

            except Exception as e:
                print(f"Server error: {e}")

        # Server is shutting down
        print("UDP Server shutting down.")
        self.server_socket.close()  # Close the UDP socket

    def handle_message(self, message, addr):
        """
        Processes a received message, logs communication, and simulates packet loss.

        Parameters:
        - message (str): The received message from the client.
        - addr (tuple): The address (IP, port) of the client.
        """
        sender_id, receiver_id, text = message.split(":", 2)  # Parse message format

        if text == STOP_SIGNAL:
            # Log and acknowledge the stop signal
            with open(LOG_FILE, "a") as log:
                log.write(f"{sender_id} sent STOP. Server shutting down.\n")
            self.server_socket.sendto(b"Server shutting down...", addr)
            self.running = False
            return

        # Log received message with timestamp
        with open(LOG_FILE, "a") as log:
            log.write(f"{sender_id} -> {SERVER_ID}: {text}\n")

        # Simulate packet loss
        if random.random() > self.packet_loss:  # Packet successfully received
            response = f"Received '{text}'"
            self.server_socket.sendto(response.encode(), addr)  # Send response

            # Log sent response
            with open(LOG_FILE, "a") as log:
                log.write(f"{SERVER_ID} -> {sender_id}: {response}\n")
        else:
            # Log lost packet (no response sent)
            with open(LOG_FILE, "a") as log:
                log.write(f"{SERVER_ID} -> {sender_id}: Packet lost\n")


# Run the server if executed as a script
if __name__ == "__main__":
    server = UDPServer()
    server.start()
