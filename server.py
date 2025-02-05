import socket
import hashlib
import struct

CHUNK_SIZE = 1024

def calculate_checksum(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def split_file(file_path, chunk_size):
    chunks = []
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            chunks.append(chunk)
    return chunks

def start_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            file_path = conn.recv(1024).decode()
            print(f"Receiving file: {file_path}")
            
            chunks = split_file(file_path, CHUNK_SIZE)
            checksum = calculate_checksum(file_path)
            
            # Send number of chunks and checksum
            conn.sendall(f"{len(chunks)}:{checksum}".encode())
            
            # Send chunks with fixed-length headers
            for i, chunk in enumerate(chunks):
                # Pack sequence number (4 bytes) and chunk length (4 bytes)
                header = struct.pack('!II', i, len(chunk))  # Network byte order
                conn.sendall(header + chunk)
            print("File sent successfully")

        
if __name__ == "__main__":
    start_server()