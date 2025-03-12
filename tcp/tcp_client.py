import socket
import time
import threading
import numpy as np
import csv

'''
TCP Client Load Testing Script

This script tests TCP performance under different levels of client load to analyze 
throughput and latency. It simulates multiple clients connecting to a TCP server, 
sending messages, and measuring network congestion effects.

Test Procedure:
    - Clients establish a connection with the server.
    - Each client sends a predefined number of messages.
    - Round-trip time (latency) and throughput are recorded.
    - The test runs for varying numbers of concurrent clients.
    - Results are logged into a CSV file for analysis.

Key Metrics:
    - **Latency**: Time taken for a message to be acknowledged by the server.
    - **Throughput**: Messages successfully sent per second.

Key Networking Methods Used:
    - socket.AF_INET: Uses IPv4 addressing.
    - socket.SOCK_STREAM: Establishes a TCP connection.
    - socket.sendall(): Ensures complete message transmission.
    - socket.recv(): Receives acknowledgment from the server.
    - threading.Thread: Simulates concurrent client connections.
    - NumPy mean(): Computes average latency and throughput.

'''

NUM_MESSAGES = 100  # Number of messages each client sends
CLIENT_COUNTS = [1, 2, 5, 10, 20, 50]  # Different client loads for testing
SERVER_ID = "S"  # Identifier for the server
STOP_SIGNAL = "STOP"  # Message to signal server shutdown
LOG_FILE = "tcp_log.txt"  # Log file for communication records

class TCPClient:
    '''
    Represents a single TCP client that connects to a server, sends messages, and measures performance.

    Attributes:
        client_id (str): Unique identifier for the client.
        host (str): Server hostname or IP address.
        port (int): Server port number.
        socket (socket): TCP socket for communication.
    '''

    def __init__(self, client_id, host="localhost", port=12345):
        '''
        Initializes a TCP client with a unique identifier.

        Args:
            client_id (int): A numerical identifier for the client.
            host (str, optional): Server hostname (default: "localhost").
            port (int, optional): Server port number (default: 12345).
        '''
        self.client_id = f"C[{client_id}]"  # Clients are represented as C[num]
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket

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

        The message follows the format: "ClientID:ReceiverID:Message".
        '''
        formatted_message = f"{self.client_id}:{receiver_id}:{message}"  # Format message
        self.socket.sendall(formatted_message.encode())  # Send message to the server

        response = self.socket.recv(1024).decode()  # Receive acknowledgment from the server

        # Log communication
        with open(LOG_FILE, "a") as log:
            log.write(f"{self.client_id} -> {SERVER_ID}: {message}\n")
            log.write(f"{SERVER_ID} -> {self.client_id}: {response}\n")

    def run(self, num_messages):
        '''
        Sends multiple messages to the server and records latency and throughput.

        Args:
            num_messages (int): Number of messages to send.

        Returns:
            tuple: (Throughput, Average Latency)
        '''
        latencies = []
        start_time = time.time()  # Start timing the test

        for i in range(num_messages):
            message = f"Message {i} from {self.client_id}"
            t1 = time.time()
            self.send_message(message)
            t2 = time.time()
            latencies.append(t2 - t1)  # Measure round-trip time

        self.socket.close()  # Close the connection

        elapsed_time = time.time() - start_time  # Total elapsed time
        throughput = num_messages / elapsed_time if elapsed_time > 0 else 0  # Messages per second
        avg_latency = np.mean(latencies) if latencies else 0  # Average round-trip time

        return throughput, avg_latency

def run_tcp_tests():
    '''
    Runs performance tests for multiple TCP clients at different levels of concurrency.
    
    The results, including average throughput and latency, are logged into a CSV file.
    '''
    with open("tcp_performance_log.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Num Clients", "Throughput", "Latency"])  # Write CSV header

        for num_clients in CLIENT_COUNTS:
            print(f"Testing {num_clients} TCP clients...")

            results = []
            clients = [TCPClient(i) for i in range(1, num_clients + 1)]  # Create client instances
            threads = []

            # Start each client in a separate thread
            for client in clients:
                client.connect()  # Establish connection
                t = threading.Thread(target=lambda: results.append(client.run(NUM_MESSAGES)))
                t.start()
                threads.append(t)

            # Wait for all clients to finish sending messages
            for t in threads:
                t.join()

            # Compute average throughput and latency across all clients
            avg_throughput = np.mean([r[0] for r in results]) if results else 0
            avg_latency = np.mean([r[1] for r in results]) if results else 0
            writer.writerow([num_clients, avg_throughput, avg_latency])  # Log results to CSV

    # Send STOP signal to the server to terminate its execution
    stop_client = TCPClient(99)  # Use a separate client instance
    stop_client.connect()
    stop_client.send_message(STOP_SIGNAL)  # Send termination signal
    stop_client.socket.close()

    print("TCP Performance tests completed. Results saved to tcp_performance_log.csv")

if __name__ == "__main__":
    run_tcp_tests()  # Start the test process
