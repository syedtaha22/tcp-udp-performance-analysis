import socket
import time
import threading
import numpy as np
import csv
import os
import sys


sys.path.append(os.path.abspath('../'))
from tcp_client import TCPClient
from tcp_server import STOP_SIGNAL

NUM_MESSAGES = 100  # Number of messages each client sends
CLIENT_COUNTS = [1, 2, 5, 10, 20, 50]  # Different client loads for testing

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
