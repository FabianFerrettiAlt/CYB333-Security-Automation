
# CYB333 Midterm - Part 1: Socket Client Implementation


import socket
import sys

# Target destination settings
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

def run_client(message="Hello from CYB333 Client!"):
    # Instructor Justin Dennison pointed out that socket.socket(socket.AF_INET, socket.SOCK_STREAM) creates an unconnected socket object in memory that acts as a low-level C API abstraction layer.
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Justin and Daniel demonstrated that default sockets operated in blocking mode, which cause operations to sometimes hang indefinitely if the endpoint is unresponsive. 
    # Justin showed us how to look up 'settimeout' in the Python docs to set an explicit timeout window.
    client_sock.settimeout(5.0)

    try:
        print(f"[*] Attempting connection to {SERVER_HOST}:{SERVER_PORT}...")
        
        # Justin emphasized that when connecting to a server, we should be explicit about the destination.He explained that we must pass the destination as an immutable tuple (host, port). 
        # He also explained that if we enter an invalid host format or an IP as a raw number without quotes, Python's underlying socket library will fail with a parse or GAI error.
        client_sock.connect((SERVER_HOST, SERVER_PORT))
        print(f"[+] Connected successfully to {SERVER_HOST}:{SERVER_PORT}")

        # Network sockets cannot transmit native Python strings directly; they must be converted to bytes using .encode('utf-8') before sending.
        print(f"[<] Sending message: '{message}'")
        client_sock.sendall(message.encode('utf-8'))

        # Justin demonstrated using .recv(1024) to retrieve response bytes returned from the remote end of the connection.
        response_data = client_sock.recv(1024)
        if response_data:
            # Decodes the incoming byte stream back into a readable string
            response_msg = response_data.decode('utf-8')
            print(f"[>] Server response: '{response_msg}'")
        else:
            print("[!] Server closed connection before sending data.")

    # Both instructors Justin and Daniel note here that attempting to connect to a port/host that is closed or inactive causes Python to throw an error/exception instead of completing. 
    except ConnectionRefusedError:
        print("[!] Connection Failed: Server is not running or port is closed.", file=sys.stderr)
    except socket.timeout:
        print("[!] Connection Failed: Operation timed out.", file=sys.stderr)
    except socket.error as err:
        print(f"[!] General Socket Error: {err}", file=sys.stderr)
    finally:
        # Justin advised us that every created socket should have an explicit .close() call when operations finish to free network resources cleanly.
        client_sock.close()
        print("[-] Client socket closed.")

if __name__ == '__main__':
    # Using the standard entry guard recommended by Justin throughout the series.
    msg = sys.argv[1] if len(sys.argv) > 1 else "Hello from CYB333 Client!"
    run_client(msg)