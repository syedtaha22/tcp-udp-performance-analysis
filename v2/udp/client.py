import csv
import os
import sys

# Ensure proper module imports
sys.path.append(os.path.abspath('../../'))
from udp_server import STOP_SIGNAL
from udp_client import UDPClient

MESSAGE_COUNTS = [1, 10, 20, 30, 50, 100, 200, 500]  # Different message loads for testing

def run_udp_tests(runs=5):
    """
    Runs UDP performance tests by sending increasing numbers of messages multiple times.
    Records throughput, average latency, and packet loss for analysis.

    Parameters:
        runs (int): Number of times each test is repeated to compute average results.
    """
    results_file = "udp_performance_log.csv"
    
    with open(results_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Num Messages", "Throughput (bytes/s)", "Avg Latency (s)", "Packet Loss (%)"])

        # Initialize accumulators for performance metrics
        total_latency = [0] * len(MESSAGE_COUNTS)
        total_throughput = [0] * len(MESSAGE_COUNTS)
        total_packet_loss = [0] * len(MESSAGE_COUNTS)

        for run in range(1, runs + 1):
            for i, num_messages in enumerate(MESSAGE_COUNTS):
                print(f"Run {run}/{runs} - Testing {num_messages} messages...")
                
                client = UDPClient()
                throughput, avg_latency, packet_loss = client.run(num_messages)
                
                total_latency[i] += avg_latency
                total_throughput[i] += throughput
                total_packet_loss[i] += packet_loss
                
                # Log separator for clarity
                with open(client.log_file, "a") as log:
                    log.write("#" * 100 + "\n")

        # Compute and write average results to CSV
        for i, num_messages in enumerate(MESSAGE_COUNTS):
            writer.writerow([
                num_messages,
                total_throughput[i] / runs,
                total_latency[i] / runs,
                total_packet_loss[i] / runs
            ])
    
    # Send STOP signal to terminate the server
    stop_client = UDPClient()
    stop_client.send_message(STOP_SIGNAL)
    stop_client.socket.close()
    
    print(f"UDP Performance tests completed. Results saved to {results_file}")

if __name__ == "__main__":
    run_udp_tests()