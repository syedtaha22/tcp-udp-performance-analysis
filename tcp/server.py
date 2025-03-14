import os
import sys

sys.path.append(os.path.abspath('../'))
from tcp_server import TCPServer

if __name__ == "__main__":
    server = TCPServer()
    server.start()  # Launch the server