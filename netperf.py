import socket
import argparse
import time

def server_mode(port, buffer_size):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(1)
    print(f"Server listening on port {port}")

    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    start_time = time.time()
    total_received = 0

    while True:
        data = conn.recv(buffer_size)
        if not data:
            break
        total_received += len(data)

    conn.close()
    server_socket.close()

    end_time = time.time()
    elapsed_time = end_time - start_time
    transfer_speed = total_received / elapsed_time / (1024 * 1024)  # in MB/s

    print(f"Data received: {total_received / (1024 * 1024)} MB")
    print(f"Time taken: {elapsed_time} seconds")
    print(f"Transfer speed: {transfer_speed:.2f} MB/s")

def client_mode(host, port, buffer_size, data_size):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    data = b'a' * buffer_size
    total_sent = 0

    start_time = time.time()

    while total_sent < data_size * 1024 * 1024:
        sent = client_socket.send(data)
        if sent == 0:
            break
        total_sent += sent

    client_socket.close()

    end_time = time.time()
    elapsed_time = end_time - start_time
    transfer_speed = total_sent / elapsed_time / (1024 * 1024)  # in MB/s

    print(f"Data sent: {total_sent / (1024 * 1024)} MB")
    print(f"Time taken: {elapsed_time} seconds")
    print(f"Transfer speed: {transfer_speed:.2f} MB/s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Network Throughput Measurement')
    parser.add_argument('-m', '--mode', choices=['server', 'client'], required=True, help='Select mode: server or client')
    parser.add_argument('-a', '--address', required=True, help='Remote address (client) or listening address (server)')
    parser.add_argument('-p', '--port', type=int, required=True, help='Remote port (client) or listening port (server)')
    parser.add_argument('-b', '--buffer-size', type=int, default=1024, help='TCP buffer size')
    parser.add_argument('-d', '--data-size', type=int, default=100, help='Amount of data to send in megabytes')

    args = parser.parse_args()

    if args.mode == 'server':
        server_mode(args.port, args.buffer_size)
    elif args.mode == 'client':
        client_mode(args.address, args.port, args.buffer_size, args.data_size)
