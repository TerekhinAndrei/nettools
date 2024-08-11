from modules.ip_scanner import IPScanner
from modules.http_requests import get

# Define IP ranges
public_ip_ranges = [
    ("1.0.0.0", "9.255.255.255"),
    ("11.0.0.0", "126.255.255.255"),
    ("128.0.0.0", "223.255.255.255")
]

current_ip_ranges = [
    ("1.2.253.170", "9.255.255.255"),
    ("11.0.0.0", "126.255.255.255"),
    ("128.0.0.0", "223.255.255.255")
]


def scan_public_ranges(ranges):
    for start_ip, end_ip in ranges:
        web_scanner = IPScanner(start_ip,end_ip,http_request=get)
        packet_sender = web_scanner.send_syn_packet
        response_handler = web_scanner.handle_scan_response
        print(f"Scanning range from {start_ip} to {end_ip}")
        web_scanner.scan_range(start_ip, end_ip,packet_sender,response_handler)


if __name__ == '__main__':
    scan_public_ranges(current_ip_ranges)