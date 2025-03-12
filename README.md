# **TCP vs. UDP Performance Analysis**  

## **Overview**  
This project compares **TCP and UDP performance** using client-server communication. The system evaluates **latency, throughput, and packet loss** by running two different test setups:  
1. **TCP and UDP multi-client tests** (located in `tcp/` and `udp/`)  
2. **TCP and UDP single-client tests with increasing message counts** (located in `v2/tcp/` and `v2/udp/`)  

Additionally, a Jupyter Notebook (`plot.ipynb`) is provided for **visualizing the results**.  

---

## **What are TCP and UDP?**  

### **TCP (Transmission Control Protocol)**  
TCP is a **connection-oriented** protocol that ensures **reliable communication** between a client and server. It establishes a **three-way handshake** before data transmission and guarantees data integrity through **acknowledgments and retransmissions**. TCP is widely used in applications that require **high reliability**, such as:  
- Web browsing (**HTTP/HTTPS**)  
- File transfers (**FTP, SFTP**)  
- Email (**SMTP, IMAP, POP3**)  
- Remote access (**SSH**)  

### **UDP (User Datagram Protocol)**  
UDP is a **connectionless** protocol that sends data **without establishing a persistent connection**. It is **faster than TCP** but does **not guarantee reliability**, making it suitable for time-sensitive applications like:  
- **Video streaming** (YouTube, Netflix, Twitch)  
- **Online gaming**  
- **VoIP** (Zoom, Skype, WhatsApp calls)  
- **DNS lookups**  

---

## **How TCP and UDP Work in Python**  

Python provides the `socket` library to implement **TCP and UDP communication**. Below is a high-level overview of how both protocols work in a **client-server model**.  

### **TCP Communication Steps**  
1. **Server Setup:**  
   - Create a TCP socket using `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`.  
   - Bind the socket to an IP and port using `socket.bind()`.  
   - Listen for incoming connections using `socket.listen()`.  
   - Accept connections using `socket.accept()`.  
   - Read/write data using `socket.recv()` and `socket.sendall()`.  
   - Close the connection using `socket.close()`.  

2. **Client Setup:**  
   - Create a TCP socket.  
   - Connect to the server using `socket.connect()`.  
   - Send messages using `socket.sendall()`.  
   - Receive acknowledgments using `socket.recv()`.  
   - Close the connection.  

### **UDP Communication Steps**  
1. **Server Setup:**  
   - Create a UDP socket using `socket.socket(socket.AF_INET, socket.SOCK_DGRAM)`.  
   - Bind the socket to an IP and port using `socket.bind()`.  
   - Receive data using `socket.recvfrom()`.  
   - Send responses using `socket.sendto()`.  

2. **Client Setup:**  
   - Create a UDP socket.  
   - Send data using `socket.sendto()`.  
   - Receive responses using `socket.recvfrom()`.  
   - Close the socket.  

---

## **Project Structure**  

- **`tcp/` and `udp/`** → Contain **multi-client tests** for TCP and UDP. Each client sends messages independently, allowing performance testing with multiple concurrent connections.  
- **`v2/tcp/` and `v2/udp/`** → Contain the **newer tests**, where a **single client sends an increasing number of messages** instead of multiple clients. This version provides a better **per-message performance comparison** between TCP and UDP.  
- **`old/`** → Stores the **original implementation** of the tests before improvements.  
- **`plot.ipynb`** → Analyzes and visualizes **TCP vs. UDP performance** based on collected data.  

---

## **Running the TCP and UDP Tests**  

To evaluate **TCP and UDP performance**, the **server and client must be run separately** in different terminal windows.  

### **Multi-Client Tests (`tcp/` and `udp/`)**  
This version tests how well TCP and UDP handle **multiple clients**.  

#### **Running the TCP Multi-Client Test**  
1. Start the TCP server:  
   ```bash
   python tcp/tcp_server.py
   ```  
2. Run the TCP client (spawns multiple clients):  
   ```bash
   python tcp/tcp_client.py
   ```  

#### **Running the UDP Multi-Client Test**  
1. Start the UDP server:  
   ```bash
   python udp/udp_server.py
   ```  
2. Run the UDP client (spawns multiple clients):  
   ```bash
   python udp/udp_client.py
   ```  

---

### **Single-Client, Increasing Messages Tests (`v2/tcp/` and `v2/udp/`)**  
This version tests how TCP and UDP **handle an increasing number of messages** from a **single client**.  

#### **Running the TCP Message Count Test**  
1. Start the TCP server:  
   ```bash
   python v2/tcp/server.py
   ```  
2. Run the TCP client (sends increasing messages per test run):  
   ```bash
   python v2/tcp/client.py
   ```  

#### **Running the UDP Message Count Test**  
1. Start the UDP server:  
   ```bash
   python v2/udp/server.py
   ```  
2. Run the UDP client (sends increasing messages per test run):  
   ```bash
   python v2/udp/client.py
   ```  

---

## **Visualizing the Results**  

After running the tests, you can analyze the results using **Jupyter Notebook**:  
```bash
jupyter notebook plot.ipynb
```  
This notebook reads **TCP and UDP performance logs**, processes the data, and **generates graphs** comparing **latency, throughput, and packet loss**.  

---

## **Key Features**  

### **Multi-Client Tests (`tcp/` and `udp/`)**  
- **TCP Server** → Handles multiple client connections concurrently.  
- **UDP Server** → Simulates packet loss by randomly dropping packets.  
- **TCP Clients** → Measure round-trip time and throughput.  
- **UDP Clients** → Track message delivery success and latency.  

### **Single-Client Increasing Messages Tests (`v2/tcp/` and `v2/udp/`)**  
- **Tests network behavior as message count increases.**  
- **Records average latency, throughput, and packet loss.**  
- **Provides a per-message performance comparison between TCP and UDP.**  

---

## **Performance Metrics**  

| Metric       | Definition                                   |
|-------------|---------------------------------------------|
| **Latency**  | Time taken for a message acknowledgment.  |
| **Throughput** | Messages successfully sent per second.  |
| **Packet Loss (UDP)** | Percentage of lost messages.  |

---

## **Observations**  

| Aspect          | TCP                                 | UDP                                 |
|-----------------|-------------------------------------|-------------------------------------|
| **Latency**     | Higher due to connection overhead   | Lower, as there is no handshake     |
| **Throughput**  | Lower due to acknowledgments        | Higher, as it sends without waiting |
| **Reliability** | Ensured via retransmission          | Packets may be lost                 |
| **Use Cases**   | Web browsing, file transfers        | VoIP, gaming, streaming             |

---

## **References**  
- Python socket programming: [Python Docs](https://docs.python.org/3/library/socket.html)  
- Python socket programming tutorial: [Real Python](https://realpython.com/python-sockets/)  
- Transmission Control Protocol (TCP): [Wikipedia](https://en.wikipedia.org/wiki/Transmission_Control_Protocol)  
- User Datagram Protocol (UDP): [Wikipedia](https://en.wikipedia.org/wiki/User_Datagram_Protocol)  
- TCP vs. UDP: Key Differences and Use Cases: [Cloudflare Learning Center](https://www.cloudflare.com/learning/ddos/glossary/user-datagram-protocol-udp/)  
- Socket Programming for Beginners: [GeeksforGeeks](https://www.geeksforgeeks.org/socket-programming-cc/)  