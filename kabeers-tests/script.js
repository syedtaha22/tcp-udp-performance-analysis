const net = require('net');
const dgram = require('dgram');
const fs = require('fs');
const { performance } = require('perf_hooks');

// Configuration
const TCP_PORT = 5000;
const UDP_PORT = 5001;
const BUFFER_SIZE = 1024;
const MESSAGE = 'a'.repeat(BUFFER_SIZE);

// Helper function to write results to CSV
function writeToCSV(filename, data) {
    const header = "Num Clients,Throughput (bytes/s),Latency (ms)\n";
    const rows = data.map(row => row.join(',')).join('\n');
    fs.writeFileSync(filename, header + rows, 'utf8');
}

// TCP Server
function startTCPServer() {
    const server = net.createServer((socket) => {
        const start = performance.now();
        socket.on('data', (data) => {
            const end = performance.now();
            const latency = end - start;
            const throughput = data.length / (latency / 1000);
            console.log(`TCP - Throughput: ${throughput} bytes/s, Latency: ${latency} ms`);
            writeToCSV('tcp_results.csv', [[1, throughput, latency]]);
            socket.write(data); // Echo back the data
        });
    });

    server.listen(TCP_PORT, '0.0.0.0', () => {
        console.log(`TCP Server listening on port ${TCP_PORT}`);
    });
}

// TCP Client
function startTCPClient() {
    const client = new net.Socket();
    const start = performance.now();

    client.connect(TCP_PORT, '127.0.0.1', () => {
        client.write(MESSAGE);
    });

    client.on('data', (data) => {
        const end = performance.now();
        const latency = end - start;
        const throughput = data.length / (latency / 1000);
        console.log(`TCP Client - Throughput: ${throughput} bytes/s, Latency: ${latency} ms`);
        client.destroy();
    });
}

// UDP Server
function startUDPServer() {
    const server = dgram.createSocket('udp4');

    server.on('message', (msg, rinfo) => {
        const start = performance.now();
        server.send(msg, rinfo.port, rinfo.address, () => {
            const end = performance.now();
            const latency = end - start;
            const throughput = msg.length / (latency / 1000);
            console.log(`UDP - Throughput: ${throughput} bytes/s, Latency: ${latency} ms`);
            writeToCSV('udp_results.csv', [[1, throughput, latency]]);
        });
    });

    server.bind(UDP_PORT, '0.0.0.0', () => {
        console.log(`UDP Server listening on port ${UDP_PORT}`);
    });
}

// UDP Client
function startUDPClient() {
    const client = dgram.createSocket('udp4');
    const start = performance.now();

    client.send(MESSAGE, UDP_PORT, '127.0.0.1', (err) => {
        if (err) {
            console.error('UDP Client - Error sending message:', err);
            client.close();
            return;
        }

        client.on('message', (msg) => {
            const end = performance.now();
            const latency = end - start;
            const throughput = msg.length / (latency / 1000);
            console.log(`UDP Client - Throughput: ${throughput} bytes/s, Latency: ${latency} ms`);
            client.close();
        });
    });
}

// Main function
function main() {
    const [command] = process.argv.slice(2);

    switch (command) {
        case 'tcp-server':
            startTCPServer();
            break;
        case 'tcp-client':
            startTCPClient();
            break;
        case 'udp-server':
            startUDPServer();
            break;
        case 'udp-client':
            startUDPClient();
            break;
        default:
            console.log('Usage: node net_test.js <command>');
            console.log('Commands: tcp-server, tcp-client, udp-server, udp-client');
            break;
    }
}

main();