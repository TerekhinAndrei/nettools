import socket


def check_port(ip, port, timeout=5):
    """Check if a specific port is open on the given IP address."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except socket.error as e:
        print(f"Socket error: {e}")
        return False


def scan_ports_range(ip, start_port, end_port):
    """Scan a range of ports on the given IP address."""
    open_ports = []
    for port in range(start_port, end_port + 1):
        print(f"Checking port {port}...")
        if check_port(ip, port):
            open_ports.append(port)
    return open_ports

def scan_ports(ip, ports):
    """Scan specific ports on the given IP address."""
    open_ports = []
    for port in ports:
        print(f"Checking port {port}...")
        if check_port(ip, port):
            open_ports.append(port)
    return open_ports


if __name__ == "__main__":
    ip_address = "1.0.195.101"  # Replace with the IP address you want to scan
    start_port = 8080  # Starting port number
    end_port = 8081  # Ending port number
    ports_to_scan = [80,8080,443,25,110,143,22,21,3389,53,67,68]

    open_ports = scan_ports(ip_address, ports_to_scan)
    if open_ports:
        print(f"Open ports on {ip_address}: {open_ports}")
    else:
        print(f"No open ports found on {ip_address} within the range {start_port}-{end_port}.")
