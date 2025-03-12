import socket
import random

'''
UDP Server for Receiving Messages

This server listens for incoming UDP messages on a specified port, logs received data, 
and simulates packet loss before sending acknowledgments.

Key Features:
    - Listens on localhost at port 12346.
    - Decodes received messages and logs them.
    - Simulates 10% packet loss.
    - Stops execution when it receives the "STOP" message.
    - Sends an acknowledgment back to the client for successfully received messages.

Key Networking Methods Used:
    - socket.AF_INET: Specifies IPv4 addressing.
    - socket.SOCK_DGRAM: Indicates UDP as the transport protocol.
    - socket.recvfrom(): Receives data from a client along with the sender's address.
    - socket.sendto(): Sends a response to the client.
'''

class UDPServer:
    '''
    A UDP server that receives messages, logs them, and simulates packet loss.
    
    Attributes:
        server (socket): A UDP socket for communication.
    '''

    def __init__(self):
        '''
        Initializes the UDP server by creating a socket and binding it to a port.
        '''
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
        self.server.bind(("localhost", 12346))  # Bind the server to localhost on port 12346

    def receive_messages(self):
        '''
        Listens for incoming UDP messages, logs them, and sends acknowledgments.

        - If a message is "STOP", logging stops, and the server shuts down.
        - Simulates 10% packet loss before sending an acknowledgment.
        '''
        with open("udp_log.txt", "w") as log:  # Open the log file in write mode
            while True:
                data, addr = self.server.recvfrom(1024)  # Receive data from the client
                message = data.decode()  # Decode the received data

                if message == "STOP":  # Stop execution if the received message is "STOP"
                    log.write("Received: STOP\n")
                    break

                if random.random() > 0.1:  # Simulate 10% packet loss (90% chance of response)
                    self.server.sendto(b"Received: " + data, addr)  # Send acknowledgment to the client
                    log.write(f"Received: {message}\n")  # Write the received message to the log file

        self.server.close()  # Close the server socket after execution stops

if __name__ == "__main__":
    server = UDPServer()  # Create a UDP server instance
    server.receive_messages()  # Start receiving messages
