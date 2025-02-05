import socket
import hashlib
import struct

CHUNK_SIZE = 1024

#calculating the checksum
def calculate_checksum(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def start_client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        file_path = input("Enter the file path: ")
        s.sendall(file_path.encode())
        
        # Receiving numbers of checks and checksum
        data = s.recv(1024).decode()
        num_chunks, checksum = data.split(':')
        num_chunks = int(num_chunks)
        
        # Receiving the process chunks with headers
        chunks = [None] * num_chunks
        buffer = b''
        while True:
            data = s.recv(4096)
            if not data:
                break
            buffer += data
            
            
            while len(buffer) >= 8:  # Header size is 8 bytes (4 for seq_num, 4 for length)
                # Extract header
                header = buffer[:8]
                seq_num, chunk_length = struct.unpack('!II', header)  #The Network byte order
                
                # Checking of entire chuck is available
                if len(buffer) < 8 + chunk_length:
                    break  # Wait for more data

                # Extracting chuck data
                chunk_data = buffer[8:8+chunk_length]
                chunks[seq_num] = chunk_data
                
                # Removeing processed bytes from header
                buffer = buffer[8+chunk_length:]

        
         # Reassembling the file
        with open("received_file", "wb") as f:
            for chunk in chunks:
                if chunk is not None:
                    f.write(chunk)
        
        # Verifying the checksum
        received_checksum = calculate_checksum("received_file")
        if received_checksum == checksum:
            print("Transfer Successful")
            print(f"Checksum : {checksum}")
            print(f"Received Checksum: {received_checksum}")
        else:
            print("Transfer Failed: Checksum mismatch")



if __name__ == "__main__":
    start_client()