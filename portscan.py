import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ip", required=True, help="Target IP address")
parser.add_argument("-p", "--port", required=True, help="Port or port range (e.g., 80 or 20-80)")
parser.add_argument("-t", "--threads", required=False, help="Number of threads")
args = parser.parse_args()

IP = args.ip
port_arg = args.port

# Determine ports to scan
if '-' in port_arg:
    start_port, end_port = map(int, port_arg.split('-'))
    ports = range(start_port, end_port + 1)
else:
    ports = [int(port_arg)]

# Convert threads argument to int if provided
if args.threads:
    try:
        MAX_THREADS = int(args.threads)
    except ValueError:
        print("Invalid value for --threads. Please provide an integer.")
        exit(1)
else:
    MAX_THREADS = 100  # Default value

def check_port(IP, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    res = s.connect_ex((IP, port))
    s.close()
    return port if res == 0 else None

def main():
    open_ports = []

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(check_port, IP, port) for port in ports]

        for future in as_completed(futures):
            port = future.result()
            if port is not None:
                open_ports.append(port)

    print("Open ports:", sorted(open_ports))

if __name__ == "__main__":
    main()
