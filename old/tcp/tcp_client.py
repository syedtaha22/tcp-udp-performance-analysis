import socket
import time
import numpy as np

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
    - socket.sendall(): Ensures complete transmission of data.
    - socket.recv(): Receives the acknowledgment from the server.
    - time.time(): Used for performance measurements.
    - NumPy mean(): Computes the average latency.
'''

class TCPClient:
    '''
    A TCP client that connects to a server, sends messages, and measures latency and throughput.
    
    Attributes:
        client (socket): A TCP socket for communication.
        latencies (list): A list to store the latency of each message.
        throughput (float): The calculated message throughput.
    '''
    
    def __init__(self):
        '''
        Initializes the TCP client by creating a socket and connecting to the server.
        '''
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
        self.client.connect(("localhost", 12345))  # Connect to the server at localhost on port 12345
        self.latencies = []  # Stores message latencies
        self.throughput = 0  # Stores throughput value

    def send_message(self, message):
        '''
        Sends a message to the server and records the round-trip time (latency).

        Parameters:
            message (str): The message to be sent to the server.

        Returns:
            float: The measured latency for the message.
        '''
        t1 = time.time()  # Start time before sending the message
        self.client.sendall(message.encode())  # Send the message to the server
        self.client.recv(1024)  # Wait for an acknowledgment response
        return time.time() - t1  # Calculate and return latency

    def run(self, num_messages=100):
        '''
        Sends multiple messages to the server, records latencies, and computes throughput.

        Parameters:
            num_messages (int, optional): The total number of messages to send. Default is 100.
        '''
        self.latencies = []  # Reset latencies list
        start_time = time.time()  # Record the start time

        for i in range(num_messages):
            message = f"Message {i}"  # Generate a unique message
            self.latencies.append(self.send_message(message))  # Send message and store its latency
        
        self.client.close()  # Close the TCP connection after all messages are sent

        elapsed_time = time.time() - start_time  # Compute total elapsed time
        self.throughput = num_messages / elapsed_time if elapsed_time > 0 else 0  # Calculate throughput

    def log_metrics(self):
        '''
        Logs the average latency and throughput to a log file and prints them.
        '''
        avg_latency = np.mean(self.latencies) if self.latencies else 0  # Compute average latency
        
        # Append metrics to a log file
        with open("tcp_log.txt", "a") as log:
            log.write(f"Average Latency: {avg_latency:.6f}s\n")
            log.write(f"Throughput: {self.throughput:.2f} msgs/s\n")

if __name__ == "__main__":
    client = TCPClient()  # Create a TCP client instance
    client.run(1000)  # Send 1000 messages
    client.log_metrics()  # Log results
