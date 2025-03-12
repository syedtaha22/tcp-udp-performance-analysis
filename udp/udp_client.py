import socket
import time
import threading
import numpy as np
import csv

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


NUM_MESSAGES = 100 # Number of messages to send per client
CLIENT_COUNTS = [1, 2, 5, 10, 20, 50] # Different client loads for testing
SERVER_ID = "S" # Identifier for the server
STOP_SIGNAL = "STOP" # Message to signal server shutdown
LOG_FILE = "udp_log.txt" # Log file for communication records


class UDPClient:
    """
    Simulates a UDP client that sends messages to a server, records performance metrics,
    and logs communication details.
    """

    def __init__(self, client_id, host="localhost", port=12345):

        self.client_id = f"C[{client_id}]"  # Clients are represented as C[num]
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket

        # Increase the receive buffer size to handle high-speed packets
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
        self.latencies = []
        self.lost_packets = 0

    def send_message(self, message, receiver_id=SERVER_ID):
        """Sends a message to the server and logs the communication."""
        formatted_message = f"{self.client_id}:{receiver_id}:{message}" # Format message
        
        t1 = time.time()  # Start time before sending the message
        self.socket.sendto(formatted_message.encode(), (self.host, self.port))  # Send message to the server

        with open(LOG_FILE, "a") as log:
            log.write(f"{self.client_id} -> {SERVER_ID}: {message}\n")

        try:
            self.socket.settimeout(0.05)  # Set a timeout for receiving the response
            response, _ = self.socket.recvfrom(1024)
            self.latencies.append(time.time() - t1)  # Calculate and store the latency
            with open(LOG_FILE, "a") as log:
                log.write(f"{SERVER_ID} -> {self.client_id}: {response.decode()}\n")
        except socket.timeout:
            self.lost_packets += 1  # Increment lost packet count if timeout occurs
            self.latencies.append(0)  # Store zero latency for lost packets


    def run(self, num_messages):
        """Runs the client, sending messages and recording performance metrics."""
        
        start_time = time.time()

        for i in range(num_messages):
            message = f"Message {i} from {self.client_id}"
            self.send_message(message)
        self.socket.close()

        elapsed_time = time.time() - start_time # Calculate total elapsed time
        throughput = (num_messages - self.lost_packets) / elapsed_time if elapsed_time > 0 else 0
        avg_latency = np.mean(self.latencies) if self.latencies else 0
        packet_loss = (self.lost_packets / num_messages) * 100

        return throughput, avg_latency, packet_loss


def run_udp_tests():
    """Runs UDP performance tests with different numbers of clients."""
    with open("udp_performance_log.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Num Clients", "Throughput", "Latency", "Packet Loss (%)"])

        for num_clients in CLIENT_COUNTS:
            print(f"Testing {num_clients} UDP clients...")

            results = []
            clients = [ UDPClient(i) for i in range(1, num_clients + 1) ]
            threads = []

            # Start each client in a separate thread
            for client in clients:
                t = threading.Thread(target=lambda: results.append(client.run(NUM_MESSAGES)))
                t.start()
                threads.append(t)

            # Wait for all threads to complete
            for t in threads:
                t.join()

            avg_throughput = np.mean([r[0] for r in results])
            avg_latency = np.mean([r[1] for r in results])
            avg_packet_loss = np.mean([r[2] for r in results])

            writer.writerow([num_clients, avg_throughput, avg_latency, avg_packet_loss]) # Write results to CSV

    # Send STOP signal to the server to terminate
    stop_client = UDPClient(99) # Create a dummy client for sending the STOP signal
    stop_client.send_message(STOP_SIGNAL) # Send the STOP signal
    stop_client.socket.close()

    print("UDP Performance tests completed. Results saved to udp_performance_log.csv")


if __name__ == "__main__":
    run_udp_tests()
