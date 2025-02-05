# Real-time-file-transfer

This project implements a real-time file transfer system using a client-server architecture. The system allows a client to upload a file to a server, which splits the file into smaller chunks, transmits them back to the client, and verifies the integrity of the file using checksums.

Features :

1. File Splitting: The server splits the file into fixed-size chunks (default: 1024 bytes).

2. Checksum Verification: The server calculates a checksum (MD5) for the file and sends it to the client. The client verifies the integrity of the reassembled file.

3. Fixed-Length Headers: Uses fixed-length binary headers to avoid ambiguity in parsing sequence numbers and chunk data.

4. Error Handling: Robust handling of chunk transmission and reassembly.


Requirements : 

1. Python 3.x

2. hashlib and socket libraries (included in Python's standard library).


Repository Structure :

real-time-file-transfer/
├── server.py              # Server-side code
├── client.py              # Client-side code
├── README.md              # Project documentation
└── data.txt               # Example file for testing


Running the Code :

Step 1: Start the Server
Open a terminal and navigate to the repository directory.
Run the server: python3 server.py

Step 2: Start the Client
Open a new terminal and navigate to the repository directory.
Run the Client : python3 client.py

Step 3: Verify the Output
The server will split the file into chunks, calculate the checksum, and send the chunks to the client.
The client will reassemble the file, calculate the checksum, and verify its integrity.
If the transfer is successful, the client will print Transfer Successful. Otherwise, it will print Transfer Failed: Checksum mismatch.

Example Workflow :

1. Server Output: 
Server listening on 127.0.0.1:65432
Connected by ('127.0.0.1', 12345)
Receiving file: data.txt
Number of chunks: 1
Sending chunk 0 of size 27
File sent successfully

2. Client Output:
Enter the file path: data.txt
Received chunk 0 of size 27
Transfer Successful

3. Verify the Received File:
The client will create a file named received_file in the same directory.
Compare received_file with the original data.txt to ensure they match.





