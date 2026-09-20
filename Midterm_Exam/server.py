
# CYB333 Midterm - Part 1: Socket Server Implementation


import socket
import sys

# Definining connection parameters
HOST = '127.0.0.1'  # Localhost binding
PORT = 5000         # Non-privileged port (>1024)

def run_server():
    # Instructor Justin Dennison explained that while socket.socket() has defaults, we should be explicit by defining socket.AF_INET (IPv4 family) and socket.SOCK_STREAM (TCP protocol). 
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allows immediate reuse of the local address/port upon restart
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Justin noted that the network functions such as bind and connect strictly require a single two-item tuple (host, port). The host must be passed as a string, while the port is passed as an integer.
        server_sock.bind((HOST, PORT))
        
        # The instructors also explained that a server must listen for incoming requests before it can evenestablish a two-way communication pipe.
        server_sock.listen(1)
        print(f"[*] Server listening on {HOST}:{PORT}...")

        # Blocking call awaiting an incoming client
        client_conn, client_addr = server_sock.accept()
        print(f"[+] Connection accepted from {client_addr[0]}:{client_addr[1]}")

        # It was explained that .recv() is used to receive data from the client. In the Banner Reading Episode Justin explained that .recv() took a buffer length in bytes (our code here is 1024) and 
        # returns raw byte data across the wire.
        data = client_conn.recv(1024)
        if data:
            # As covered in both our Python 3 book and the video series, incoming network data arrives as raw bytes and must be decoded to native string characters to read or print cleanly.
            message = data.decode('utf-8')
            print(f"[>] Received from client: '{message}'")

            # Before pushing text back through the socket pipe, the string must be converted into bytes using .encode(), since TCP streams handle binary data.
            response = f"ACK: Server received '{message}'".encode('utf-8')
            client_conn.sendall(response)
            print("[<] Response sent back to client.")

        # Justin repeatedly stressed to us that the importance of explicitly calling .close() on connections to prevent hanging descriptors and cleanly exit the program.
        client_conn.close()
        print("[-] Client connection closed cleanly.")

    except socket.error as err:
        print(f"[!] Socket error encountered: {err}", file=sys.stderr)
    except KeyboardInterrupt:
        print("\n[!] Server manually terminated.")
    finally:
        # Releases the listening socket
        server_sock.close()
        print("[*] Server socket released.")

if __name__ == '__main__':
    # Justin recommended wrapping our executable code in an 'if __name__ == "__main__":' guard so the script can be cleanly imported into other security modules without automatically 
    # firing execution or creating unwanted connections.
    run_server()