import socket
import time
import threading
import numpy as np
import random

from Message import Message
from udp_server import SERVER_ID

'''
UDP Client for Measuring Latency and Throughput

This client establishes a UDP connection with a server, sends a specified number of messages,
and records network performance metrics, including latency and throughput.

Metrics:
    - Latency: Measures the round-trip time for a message to reach the server and return.
    - Throughput: Calculates the number of successfully sent messages per second.

Key Networking Methods Used:
    - socket.AF_INET: Specifies IPv4 addressing.
    - socket.SOCK_DGRAM: Indicates UDP as the transport protocol.
    - socket.sendto(): Sends a message to the server.
    - socket.recvfrom(): Receives the acknowledgment from the server.
    - time.time(): Used for performance measurements.
    - NumPy mean(): Computes the average latency.
'''

class UDPClient:
    """
    Simulates a UDP client that sends messages to a server, records performance metrics,
    and logs communication details.

    Attributes:
        client_id (str): The unique identifier for the client.
        host (str): The server hostname or IP address.
        port (int): The server port number.
        socket (socket): The UDP socket for communication.
        log_file (str): The file to log communication records.
    """

    def __init__(self, client_id: int = 1, host: str = "localhost", port: int = 12345,  log_file: str = "udp_log.txt"):
        """
        Initializes the UDP client with the server details and creates a UDP socket.

        Args:
            host (str): The server hostname or IP address. Defaults to "localhost".
            port (int): The server port number. Defaults to 12345.
            client_id (int): The numerical identifier for the client. Defaults to 1.
            log_file (str): The file to log communication records. Defaults to "udp_log.txt".
        """
        self.client_id = f"C[{client_id}]"  # Clients are represented as C[num]
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
        self.socket.settimeout(0.001) 

        self.log_file = log_file       


    def send_message(self, message, receiver_id=SERVER_ID):
        """
        Sends a message to the server and logs the communication.

        Args:
            message (str): The message content to send.
            receiver_id (str): The identifier of the message recipient.
        
        Returns:
            float: The measured latency for the message.
            int: The number of bytes sent.
        """

        with open(self.log_file, "a") as log:
            formatted_message = (f'{self.client_id}:{receiver_id}:{message}').encode()
            bytes_sent = len(message)

            start = time.time()  # Start time before sending the message
            self.socket.sendto(formatted_message, (self.host, self.port))  # Send message to server
            log.write(f"Client -> {SERVER_ID}: {message}\n")

            try:
                response, _ = self.socket.recvfrom(4096) # Receive response from the server
                latency = time.time() - start # Calculate the round-trip time

                return latency, bytes_sent
            except socket.timeout:
                return None, bytes_sent  # Return None if the message is lost

    def run(self, num_messages):
        """
        Runs the client, sending messages and recording performance metrics.

        Args:
            num_messages (int): The number of messages to send to the server.
        """
        
        latencies = []
        bytes_sent = []
        lost_packets = 0
        start_time = time.time()

        for i in range(num_messages):
            message = Message(i, num_messages, 'UDP')
            latency, bytes = self.send_message(message)
            bytes_sent.append(bytes)  # Track the number of bytes sent

            if latency is None:
                lost_packets += 1  # Packet loss detected
            else:
                latencies.append(latency)  # Store valid latency measurements

        self.socket.close()

        elapsed_time = time.time() - start_time  # Calculate total elapsed time
        throughput = sum(bytes_sent) / elapsed_time if elapsed_time > 0 else 0
        avg_latency = np.mean(latencies) if latencies else 0
        packet_loss = (lost_packets / num_messages) * 100

        return throughput, avg_latency, packet_loss