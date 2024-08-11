import ipaddress

from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr1, send

class IPScanner:
    def __init__(self, start_ip, end_ip, http_request):
        self.current_ip = None
        self.http_request = http_request

    def scan(self, ip):
        try:
            pkt = IP(dst=ip) / TCP(dport=80, flags="S")
            resp = sr1(pkt, timeout=1, verbose=0)
            if resp is None:
                return None  # Changed from False to None
            if resp.haslayer(TCP) and resp.getlayer(TCP).flags == 0x12:
                send(IP(dst=ip) / TCP(dport=80, flags="R"), verbose=0)
                return resp
            return None  # Changed from False to None
        except Exception as e:
            print(f"Error scanning {ip}: {e}")
            return None

    def scan_range(self, start_ip, end_ip, packet_sender=None, answer_handler=None):
        try:
            # Convert IP range to ipaddress objects
            start = ipaddress.ip_address(start_ip)
            end = ipaddress.ip_address(end_ip)

            # Ensure start_ip is less than or equal to end_ip
            if start > end:
                raise ValueError("start_ip must be less than or equal to end_ip")

            # Generate IP range and scan each IP
            current_ip = start
            while current_ip <= end:
                ip_str = str(current_ip)
                self.current_ip = ip_str
                response = self.scan(ip_str)
                if response:
                    if answer_handler:
                        answer_handler(ip_str, response)  # Call the answer handler with IP and response
                    if packet_sender:
                        packet_sender(ip_str)  # Call the packet sender if provided
                else:
                    print(f"{ip_str} is down or port 80 is closed")

                # Move to the next IP address
                current_ip += 1
        except Exception as e:
            print(f"Error in scan_range: {e}")

    def send_syn_packet(self, ip):
        # Construct the IP and TCP packet
        ip_packet = IP(dst=ip)
        tcp_packet = TCP(dport=80, flags="S")
        packet = ip_packet / tcp_packet

        # Send the packet and wait for a response
        response = sr1(packet, timeout=2, verbose=0)

        # Check and interpret the response
        if response is None:
            print(f"No response from {ip}")
        elif response.haslayer(TCP):
            if response.getlayer(TCP).flags == 0x12:  # SYN-ACK
                print(f"Port 80 is open on {ip}")
                # Send a RST packet to close the connection
                rst_packet = IP(dst=ip) / TCP(dport=80, flags="R")
                send(rst_packet, verbose=0)
            elif response.getlayer(TCP).flags == 0x14:  # RST-ACK
                print(f"Port 80 is closed on {ip}")
            else:
                print(f"Unexpected response: {response.summary()}")
        else:
            print(f"Unexpected response: {response.summary()}")

    def handle_scan_response(self, ip, response):
        if response is None:
            print(f"No response from {ip}")
            return

        print(f"Response from {ip}:")
        print(response.summary())

        if response.haslayer(TCP):
            self.http_request(ip)
            tcp_layer = response.getlayer(TCP)
            flags = tcp_layer.flags
            if flags == 0x12:  # SYN-ACK
                print(f"Port 80 is open (SYN-ACK received)")
            elif flags == 0x14:  # RST-ACK
                print(f"Port 80 is closed (RST-ACK received)")
            else:
                print(f"Unexpected TCP flags: {flags:02x}")
        else:
            print(f"Unexpected response: {response.summary()}")
