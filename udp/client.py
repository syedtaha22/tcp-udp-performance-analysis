import threading
import numpy as np
import csv
import os
import sys

sys.path.append(os.path.abspath('../'))
from udp_client import UDPClient
from udp_server import STOP_SIGNAL

# Configuration
NUM_MESSAGES = 100  # Number of messages each client sends
CLIENT_COUNTS = [1, 2, 5, 10, 20, 50]  # Different client loads for testing

def run_udp_tests():
    """Runs UDP performance tests with different numbers of clients and logs results to a CSV file."""
    with open("udp_performance_log.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Num Clients", "Throughput (bytes/s)", "Latency (s)", "Packet Loss (%)"])

        for num_clients in CLIENT_COUNTS:
            print(f"Testing {num_clients} UDP clients...")
            
            results = []
            clients = [UDPClient(i) for i in range(1, num_clients + 1)]
            threads = []

            # Start each client in a separate thread
            for client in clients:
                t = threading.Thread(target=lambda: results.append(client.run(NUM_MESSAGES)))
                t.start()
                threads.append(t)

            # Wait for all threads to complete
            for t in threads:
                t.join()

            # Compute average performance metrics
            avg_throughput = np.mean([r[0] for r in results])
            avg_latency = np.mean([r[1] for r in results])
            avg_packet_loss = np.mean([r[2] for r in results])

            writer.writerow([num_clients, avg_throughput, avg_latency, avg_packet_loss])

    # Send STOP signal to terminate the UDP server
    stop_client = UDPClient(99)
    stop_client.send_message(STOP_SIGNAL)
    stop_client.socket.close()

    print("UDP Performance tests completed. Results saved to udp_performance_log.csv")

if __name__ == "__main__":
    run_udp_tests()