
# CYB333 Midterm - Part 2: Port Scanner Implementation


import socket
import sys
import time

# Instructor Justin Dennison implemented an object-oriented class (Scanner) rather than loose functions. He explained that storing 
# the target IP and state as instance attributes (self.ip, self.open_ports) encapsulated the data inside the object in memory, which then prevents the need to pass parameters across 
# multiple functions or rely on messy global variables.
class PortScanner:
    # only authorized testing targets 
    AUTHORIZED_TARGETS = ['127.0.0.1', 'localhost', 'scanme.nmap.org']

    def __init__(self, target, timeout=0.5):
        self.raw_target = target
        self.timeout = timeout
        #  Justin initialized an internal empty list (self.open_ports = []) in the constructor to dynamically accumulate open ports during the scan.
        self.open_ports = []
        self.target_ip = self._validate_and_resolve()

    def _validate_and_resolve(self):
        """Validates authorization and resolves domain to IPv4."""
        # Justin emphasized that ethical penetration testing enforces assignment scope boundary to ensure legal and ethical compliance.
        if self.raw_target not in self.AUTHORIZED_TARGETS:
            print(f"[!] Scope Violation: '{self.raw_target}' is not an authorized testing target.")
            print(f"    Authorized targets: {', '.join(self.AUTHORIZED_TARGETS)}")
            sys.exit(1)

        try:
            # Justin noted that low-level socket functions expect clean host strings and IP representations. We can use gethostbyname() to resolve names like 'scanme.nmap.org' 
            # to standard IPv4 dot-notation before connecting.
            resolved_ip = socket.gethostbyname(self.raw_target)
            return resolved_ip
        except socket.gaierror:
            # Justin also encountered and explained 'socket.gaierror' (getaddrinfo error) when passing invalid or unresolvable domain strings to socket connection utilities.
            print(f"[!] Host Resolution Error: Unable to resolve hostname '{self.raw_target}'.")
            sys.exit(1)

    def is_port_open(self, port):
        """
        Tests individual TCP port using connect_ex.
        Returns True if code is 0 (open), False otherwise.
        """
        # Justin explicitly configured socket.AF_INET (IPv4) and socket.SOCK_STREAM (TCP) to define the exact family and transport protocol.
        # Also annoted from our supplemental slides, Networked Programs, Slide 10, demonstrated creating socket.socket(socket.AF_INET, socket.SOCK_STREAM) for standard TCP pipes.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Justin and Daniel demonstrated that default sockets operate in blocking mode, which causes them to hang indefinitely waiting on unresponsive ports. Justin demonstrated calling settimeout() before 
        # attempting connection to keep execution fast and deterministic.
        sock.settimeout(self.timeout)

        # Justin highlights 'connect_ex()' as a critical method. While standard connect() raised an unhandled exception on closed ports, connect_ex() returns 
        # a C-level integer status code. Justin then went on to explain that a return code of 0 indicated success (no error, port is open), while any non-zero value indicates a failure or closed port.
        result_code = sock.connect_ex((self.target_ip, port))

        # Justin stresses here that every socket should be explicitly closed, immediately after checking to release the system descriptor and free network resources.
        sock.close()

        # Returns True if the C-level error code is 0 (open), otherwise False
        return result_code == 0

    def scan_ports(self, start_port, end_port):
        """Iterates through specified port range and records open ports."""
        # Standard TCP port boundary checks (valid ports are 1 through 65535)
        if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535):
            print("[!] Port Error: Ports must fall between 1 and 65535.")
            return []

        if start_port > end_port:
            print("[!] Range Error: Start port cannot be greater than end port.")
            return []

        print(f"\n[*] Initiating scan against: {self.raw_target} ({self.target_ip})")
        print(f"[*] Port Range: {start_port} through {end_port} | Timeout: {self.timeout}s")
        print("-" * 55)

        start_time = time.time()

        # Justin noted that Python's range(a, b) is non-inclusive on the upper boundary, so we iterate through end_port + 1 to ensure the final port is scanned.
        for port in range(start_port, end_port + 1):
            if self.is_port_open(port):
                print(f"  [+] Port {port:<10} [OPEN]")
                self.open_ports.append(port)
            else:
                # Provides detailed closed feedback for targeted scans without cluttering large sweeps
                if (end_port - start_port) <= 20:
                    print(f"  [-] Port {port:<10} [CLOSED]")

        duration = time.time() - start_time
        print("-" * 55)
        # Formats and displays run time similar to the 'timefunc' utility demonstrated in the video series
        print(f"[*] Scan completed in {duration:.2f} seconds.")
        print(f"[*] Discovered Open Ports: {self.open_ports if self.open_ports else 'None'}\n")
        return self.open_ports


def main():
    print("=" * 55)
    print("  CYB333 Security Automation - TCP Port Scanner")
    print("=" * 55)

    # Prompt user for scan parameters
    target_input = input("Enter target host (localhost, 127.0.0.1, or scanme.nmap.org): ").strip()
    
    try:
        # Ports must be converted to numeric integers for range iteration and tuple sockets
        start_p = int(input("Enter starting port: ").strip())
        end_p = int(input("Enter ending port: ").strip())
    except ValueError:
        print("[!] Input Error: Port numbers must be valid integers.")
        sys.exit(1)

    # Initialize scanner and run
    scanner = PortScanner(target=target_input, timeout=0.5)
    scanner.scan_ports(start_p, end_p)


if __name__ == '__main__':
    # Standard entry point guard recommended by Justin throughout the series.
    main()