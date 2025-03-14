import os
import sys

sys.path.append(os.path.abspath('../../'))
from udp_server import UDPServer

# Run the server if executed as a script
if __name__ == "__main__":
    server = UDPServer()
    server.start()