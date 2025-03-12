import socket
import time
import numpy as np
import csv

'''
UDP Client for Measuring Latency, Throughput, and Packet Loss

This client sends an increasing number of messages to a UDP server and records network 
performance metrics, including latency, throughput, and packet loss.

Metrics:
    - Latency: Measures round-trip time for a message to reach the server and return.
    - Throughput: Calculates the number of successfully sent messages per second.
    - Packet Loss: Measures the percentage of lost messages.

Key Networking Methods Used:
    - socket.AF_INET: Specifies IPv4 addressing.
    - socket.SOCK_DGRAM: Uses UDP as the transport protocol.
    - socket.sendto(): Sends a message to the server.
    - socket.recvfrom(): Receives the acknowledgment from the server.
    - time.time(): Used for performance measurements.
    - NumPy mean(): Computes average latency.
'''

MESSAGE_COUNTS = [1, 10, 20, 30, 50, 100, 200, 500]  # Different message loads for testing
SERVER_ID = "S"  # Identifier for the server
STOP_SIGNAL = "STOP"  # Message to signal server shutdown
LOG_FILE = "udp_log.txt"  # Log file for communication records


class UDPClient:
    """
    Simulates a UDP client that sends messages to a server, records performance metrics,
    and logs communication details.
    """

    def __init__(self, host="localhost", port=12345):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket

        # Increase the receive buffer size to handle high-speed packets
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
        self.socket.settimeout(0.00001)  # Set a timeout for receiving the response

    def send_message(self, message, receiver_id=SERVER_ID):
        formatted_message = f"Client:{receiver_id}:{message}"  # Format message
        self.socket.sendall(formatted_message.encode())  # Send message to the server

        response = self.socket.recv(1024).decode()  # Receive acknowledgment from the server

        # Log communication
        with open(LOG_FILE, "a") as log:
            log.write(f"Client -> {SERVER_ID}: {message}\n")
            log.write(f"{SERVER_ID} -> Client: {response}\n")

    def send_message(self, message, receiver_id=SERVER_ID):
        """Sends a message to the server and logs the communication."""
        formatted_message = f"Client:{receiver_id}:{message}"  # Format message

        t1 = time.time()  # Start time before sending the message
        self.socket.sendto(formatted_message.encode(), (self.host, self.port))  # Send message to server

        try:
            response, _ = self.socket.recvfrom(1024)
            latency = time.time() - t1  # Measure round-trip time
            with open(LOG_FILE, "a") as log:
                log.write(f"Client -> {SERVER_ID}: {message}\n")
                log.write(f"{SERVER_ID} -> Client: {response.decode()}\n")
            return latency  # Return measured latency
        except socket.timeout:
            return None  # Indicate that the packet was lost

    def run(self, num_messages):
        """Runs the client, sending messages and recording performance metrics."""
        
        latencies = []
        lost_packets = 0
        start_time = time.time()

        for i in range(num_messages):
            message = f"Message {i} from Client"
            latency = self.send_message(message)

            if latency is None:
                lost_packets += 1  # Packet loss detected
            else:
                latencies.append(latency)  # Store valid latency measurements

        self.socket.close()

        elapsed_time = time.time() - start_time  # Calculate total elapsed time
        throughput = (num_messages - lost_packets) / elapsed_time if elapsed_time > 0 else 0
        avg_latency = np.mean(latencies) if latencies else 0
        packet_loss = (lost_packets / num_messages) * 100

        return throughput, avg_latency, packet_loss


def run_udp_tests(runs=5):
    """Runs UDP performance tests by sending increasing numbers of messages multiple times and averaging the results."""
    with open("udp_performance_log.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Num Messages", "Avg Throughput", "Avg Latency", "Avg Packet Loss (%)"])

        total_latency = [0 for _ in MESSAGE_COUNTS]  # Store sum of latencies
        total_throughput = [0 for _ in MESSAGE_COUNTS]  # Store sum of throughputs
        total_packet_loss = [0 for _ in MESSAGE_COUNTS]  # Store sum of packet losses

        for _ in range(runs):
            for i, num_messages in enumerate(MESSAGE_COUNTS):
                print(f"Testing {num_messages} messages... (Run {_+1}/{runs})")

                client = UDPClient()
                throughput, avg_latency, packet_loss = client.run(num_messages)

                total_latency[i] += avg_latency  # Accumulate latencies
                total_throughput[i] += throughput  # Accumulate throughputs
                total_packet_loss[i] += packet_loss  # Accumulate packet loss

                with open(LOG_FILE, "a") as log:
                    log.write("#" * 100 + "\n")  # Log separation

        # Compute averages and write to CSV
        for i, num_messages in enumerate(MESSAGE_COUNTS):
            avg_latency = total_latency[i] / runs
            avg_throughput = total_throughput[i] / runs
            avg_packet_loss = total_packet_loss[i] / runs
            writer.writerow([num_messages, avg_throughput, avg_latency, avg_packet_loss])  # Log results to CSV

    # Send STOP signal to the server to terminate
    stop_client = UDPClient()
    stop_client.send_message(STOP_SIGNAL)
    stop_client.socket.close()

    print("UDP Performance tests completed. Results saved to udp_performance_log.csv")



if __name__ == "__main__":
    run_udp_tests()
