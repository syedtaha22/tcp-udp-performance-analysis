import socket
import time
import numpy as np

from Message import Message
from tcp_server import SERVER_ID

'''
TCP Client for Measuring Latency and Throughput

This client establishes a TCP connection with a server, sends a specified number of messages,
and records network performance metrics, including latency and throughput.

Metrics:
    - Latency: Measures the round-trip time for a message to reach the server and return.
    - Throughput: Calculates the number of successfully sent messages per second.

Key Networking Methods Used:
    - socket.AF_INET: Specifies IPv4 addressing.
    - socket.SOCK_STREAM: Indicates TCP as the transport protocol.
    - socket.socket(): Creates a TCP socket for communication.
    - socket.connect(): Establishes a connection to the server.
    - socket.sendall(): Sends a message to the server.
    - socket.recv(): Receives the acknowledgment from the server.
    - time.time(): Used for performance measurements.
    - NumPy mean(): Computes the average latency.
'''


class TCPClient:
    '''
    Represents a single TCP client that connects to a server, sends messages, and measures performance.

    Attributes:
        client_id (str): Unique identifier for the client.
        host (str): Server hostname or IP address.
        port (int): Server port number.
        socket (socket): TCP socket for communication.
        log_file (str): File to log communication records.
    '''

    def __init__(self, client_id: int = 1, host: str = "localhost", port: int = 12345,  log_file: str = "tcp_log.txt"):
        '''
        Initializes a TCP client with a unique identifier.

        Args:
            host (str, optional): Server hostname (default: "localhost").
            port (int, optional): Server port number (default: 12345).
            client_id (int, optional): A numerical identifier for the client (default: 1).
            log_file (str, optional): File to log communication records (default: "tcp_log.txt").
        '''
        self.client_id = f"C[{client_id}]"  # Clients are represented as C[num]
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
        self.log_file = log_file

    def connect(self):
        '''
        Establishes a connection to the TCP server.
        '''
        self.socket.connect((self.host, self.port))

    def send_message(self, message, receiver_id=SERVER_ID):
        '''
        Sends a message to the server and logs communication.

        Args:
            message (str): The message content.
            receiver_id (str, optional): The recipient (default: SERVER_ID).
        
        Returns:
            float: The measured latency for the message.
            int: The number of bytes sent.

        The message follows the format: "ClientID:ReceiverID:Message".
        '''
        with open(self.log_file, "a") as log:
            formatted_message = (f'{self.client_id}:{receiver_id}:{message}').encode() # Format message
            bytes_sent = len(message)

            start = time.time()  # Start time before sending the message
            self.socket.sendall(formatted_message)  # Send message to the server
            response = self.socket.recv(2048).decode()  # Receive acknowledgment from the server
            latency = time.time() - start  # Measure round-trip time    
            
            # Log communication  
            log.write(f"{self.client_id} -> {SERVER_ID}: {message}\n")

            # Return latency and bytes sent
            return latency, bytes_sent

    def run(self, num_messages):
        '''
        Sends multiple messages to the server and records latency and throughput.

        Args:
            num_messages (int): Number of messages to send.

        Returns:
            tuple: (Throughput, Average Latency)
        '''
        latencies = []
        bytes_sent = []
        start_time = time.time()  # Start timing the test

        for i in range(num_messages):
            message = Message(i, num_messages, 'TCP', self.client_id)
            
            latency, bytes = self.send_message(message)
            latencies.append(latency)
            bytes_sent.append(bytes)  # Track the number of bytes sent
        self.socket.close()  # Close the connection

        elapsed_time = time.time() - start_time  # Total elapsed time
        throughput = sum(bytes_sent) / elapsed_time if elapsed_time > 0 else 0  # Bytes per second
        avg_latency = np.mean(latencies) if latencies else 0  # Average round-trip time

        return throughput, avg_latency

