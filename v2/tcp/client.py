import socket
import time
import csv
import numpy as np

'''
TCP Client Load Testing Script

This script tests TCP performance by sending different numbers of messages from a single client 
to a TCP server. It measures the effect of increasing message load on throughput and latency.

Test Procedure:
    - A single client establishes a connection with the server.
    - It sends messages in increasing amounts (1, 10, 20, 30, ...).
    - Round-trip time (latency) and throughput are recorded for each test.
    - Results are logged into a CSV file for analysis.

Key Metrics:
    - **Latency**: Time taken for a message to be acknowledged by the server.
    - **Throughput**: Messages successfully sent per second.

Key Networking Methods Used:
    - socket.AF_INET: Uses IPv4 addressing.
    - socket.SOCK_STREAM: Establishes a TCP connection.
    - socket.sendall(): Ensures complete message transmission.
    - socket.recv(): Receives acknowledgment from the server.
'''

MESSAGE_COUNTS = [1, 10, 20, 30, 50, 100, 200, 500]  # Different message loads for testing
SERVER_ID = "S"  # Identifier for the server
STOP_SIGNAL = "STOP"  # Message to signal server shutdown
LOG_FILE = "tcp_log.txt"  # Log file for communication records


class TCPClient:
    '''
    Represents a single TCP client that connects to a server, sends messages, and measures performance.

    Attributes:
        host (str): Server hostname or IP address.
        port (int): Server port number.
        socket (socket): TCP socket for communication.
    '''

    def __init__(self, host="localhost", port=12345):
        '''
        Initializes a TCP client.

        Args:
            host (str, optional): Server hostname (default: "localhost").
            port (int, optional): Server port number (default: 12345).
        '''
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

        The message follows the format: "Client:ReceiverID:Message".
        '''
        formatted_message = f"Client:{receiver_id}:{message}"  # Format message
        self.socket.sendall(formatted_message.encode())  # Send message to the server

        response = self.socket.recv(1024).decode()  # Receive acknowledgment from the server

        # Log communication
        with open(LOG_FILE, "a") as log:
            log.write(f"Client -> {SERVER_ID}: {message}\n")
            log.write(f"{SERVER_ID} -> Client: {response}\n")

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
            message = f"Message {i} from Client"
            t1 = time.time()
            self.send_message(message)
            t2 = time.time()
            latencies.append(t2 - t1)  # Measure round-trip time

        self.socket.close()  # Close the connection

        elapsed_time = time.time() - start_time  # Total elapsed time
        throughput = num_messages / elapsed_time if elapsed_time > 0 else 0  # Messages per second
        avg_latency = np.mean(latencies) if latencies else 0  # Average round-trip time

        return throughput, avg_latency


def run_tcp_tests(runs=10):
    '''
    Runs performance tests by sending increasing numbers of messages from a single TCP client.
    
    The results, including average throughput and latency, are logged into a CSV file.
    '''
    with open("tcp_performance_log.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Num Messages", "Avg Throughput", "Avg Latency"])  # Write CSV header

        total_latency = [0 for _ in MESSAGE_COUNTS]  # Store sum of latencies
        total_throughput = [0 for _ in MESSAGE_COUNTS]  # Store sum of throughputs

        for _ in range(runs):
            for i, num_messages in enumerate(MESSAGE_COUNTS):
                print(f"Testing {num_messages} messages... (Run {_+1}/{runs})")

                client = TCPClient()
                client.connect()
                throughput, avg_latency = client.run(num_messages)

                total_latency[i] += avg_latency  # Accumulate latencies
                total_throughput[i] += throughput  # Accumulate throughputs

                with open(LOG_FILE, "a") as log:
                    log.write("#" * 100 + "\n")  # Log separation

        # Compute averages and write to CSV
        for i, num_messages in enumerate(MESSAGE_COUNTS):
            avg_latency = total_latency[i] / runs
            avg_throughput = total_throughput[i] / runs
            writer.writerow([num_messages, avg_throughput, avg_latency])  # Log results to CSV

    # Send STOP signal to the server to terminate its execution
    stop_client = TCPClient()
    stop_client.connect()
    stop_client.send_message(STOP_SIGNAL)  # Send termination signal
    stop_client.socket.close()

    print("TCP Performance tests completed. Results saved to tcp_performance_log.csv")


if __name__ == "__main__":
    run_tcp_tests()  # Start the test process
