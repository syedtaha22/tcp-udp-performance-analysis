import socket
import time
import numpy as np

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
    '''
    A UDP client that sends messages to a server and measures latency and throughput.
    
    Attributes:
        client (socket): A UDP socket for communication.
        latencies (list): A list to store the latency of each message.
        lost_packets (int): The number of lost packets during communication.
        throughput (float): The calculated message throughput.
    '''
    
    def __init__(self):
        '''
        Initializes the UDP client by creating a socket.
        '''
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
        self.latencies = []  # Stores message latencies
        self.lost_packets = 0  # Stores the number of lost packets
        self.throughput = 0  # Stores throughput value

    def send_message(self, message):
        '''
        Sends a message to the server and records the round-trip time (latency).

        Parameters:
            message (str): The message to be sent to the server.
        '''
        t1 = time.time()  # Start time before sending the message
        self.client.sendto(message.encode(), ("localhost", 12346))  # Send the message to the server
        try:
            self.client.settimeout(0.1)  # Set a timeout for receiving the response
            self.client.recvfrom(1024)  # Wait for an acknowledgment response
            self.latencies.append(time.time() - t1)  # Calculate and store the latency
        except socket.timeout:
            self.lost_packets += 1  # Increment lost packets if the message is not received

    def run(self, num_messages=100):
        '''
        Sends multiple messages to the server, records latencies, and computes throughput.

        Parameters:
            num_messages (int): The number of messages to send to the server.
        '''
        start_time = time.time()  # Start time for measuring throughput

        for i in range(num_messages):
            message = f"Message {i}"  # Create a message
            self.send_message(message)  # Send the message to the server
        self.client.sendto(b"STOP", ("localhost", 12346))  # Send STOP signal to terminate the server
        self.client.close()  # Close the UDP connection

        # Calculate the throughput by dividing the number of messages sent by the time taken to send them
        self.throughput = (num_messages - self.lost_packets) / (time.time() - start_time)

    def log_metrics(self):
        '''
        Logs the average latency, packet loss, and throughput to a file.
        '''
        with open("udp_log.txt", "a") as log:
            log.write(f"Average Latency: {np.mean(self.latencies):.6f}s\n")
            log.write(f"Packet Loss: {self.lost_packets}%\n")
            log.write(f"Throughput: {self.throughput:.2f} msgs/sec\n")



if __name__ == "__main__":
    client = UDPClient()  # Initialize the UDP client
    client.run(1000)  # Send 1000 messages to the server
    client.log_metrics()  # Log the performance metrics to a file