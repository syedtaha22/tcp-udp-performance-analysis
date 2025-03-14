import csv
import os
import sys

sys.path.append(os.path.abspath('../../'))
from tcp_client import TCPClient
from tcp_server import STOP_SIGNAL

# Different message loads for testing
MESSAGE_COUNTS = [1, 10, 20, 30, 50, 100, 200, 500]  

def run_tcp_tests(runs=10):
    """
    Runs performance tests by sending increasing numbers of messages from a single TCP client.

    The results, including average throughput and latency, are logged into a CSV file.

    Args:
        runs (int): The number of test runs to perform (default is 10).
    """
    with open("tcp_performance_log.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Num Messages", "Throughput (bytes/s)", "Avg Latency (s)"])

        total_latency = [0] * len(MESSAGE_COUNTS)  # Sum of latencies
        total_throughput = [0] * len(MESSAGE_COUNTS)  # Sum of throughputs

        for run in range(1, runs + 1):
            for i, num_messages in enumerate(MESSAGE_COUNTS):
                print(f"Testing {num_messages} messages... (Run {run}/{runs})")

                client = TCPClient()
                client.connect()
                throughput, avg_latency = client.run(num_messages)

                total_latency[i] += avg_latency
                total_throughput[i] += throughput

                with open(client.log_file, "a") as log:
                    log.write("#" * 100 + "\n")  # Log separation

        # Compute averages and write to CSV
        for i, num_messages in enumerate(MESSAGE_COUNTS):
            avg_latency = total_latency[i] / runs
            avg_throughput = total_throughput[i] / runs
            writer.writerow([num_messages, avg_throughput, avg_latency])

    # Send STOP signal to terminate the server
    stop_client = TCPClient()
    stop_client.connect()
    stop_client.send_message(STOP_SIGNAL)
    stop_client.socket.close()

    print("TCP Performance tests completed. Results saved to tcp_performance_log.csv")

if __name__ == "__main__":
    run_tcp_tests()
