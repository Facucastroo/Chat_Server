
import socket,threading,ipaddress

# Define the format for encoding and decoding messages
FORMAT = "utf-8"

# Initialize lists for storing active connections and names
connections, names = [], []

# Create a socket object
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def Server(HOST,PORT):
    # Try to bind the server to the specified host and port
    try:
        addr=str(ipaddress.ip_address(HOST)),PORT
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(addr)
    # If an error occurs, print the error message and raise the exception
    except Exception as e:
        print(f"An error ocurred!:{e}")
        raise
    # If the server is successfully bound, start listening for incoming connections
    else:
        server.listen(9)
        print(f"Server: Listening in {HOST}:{PORT}")
        server_running = True
        # Start an infinite loop to handle incoming connections
        while server_running:
            print('waiting connection ...')
            conn, addr = server.accept()
            # Send a message to the client requesting their name
            conn.send("NAME".encode(FORMAT))
            # Receive the client's name and decode it
            name = conn.recv(2048).decode(FORMAT)
            # Add the client's name and connection to the respective lists
            names.append(name)
            connections.append(conn)
            print(f"Name is :{name}")
            # Broadcast a welcome message to all connected clients
            broadcast(f"{name} Welcome! ".encode(FORMAT))
            # Send a confirmation message to the client
            conn.send('Connection successful!'.encode(FORMAT))
            # Start a new thread to handle the client's communication
            threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
        server.close()
            
def startChat(HOST,PORT):
    # Start a new thread to run the server
    threading.Thread(target=Server, args=(HOST,PORT)).start()

def handle(connection, address):
    # Print the address of the client that just connected
    print(f"new connection {address}")
    # Start an infinite loop to handle the client's messages
    while True:
        try:
            # Receive a message from the client
            msg = connection.recv(1024)
            # If a message was received, decode it and print it
            if msg:
                print(f'{address[0]}:{address[1]} - {msg.decode()}')
                broadcast(msg)
            # If no message was received, the client disconnected
            else:
                remove_connection(connection)
                print(f"Left Chat {address}")
                break
        # If an error occurs while handling the client's message, print the error message and remove the client's connection
        except Exception as e:
            print(f'Error to handle user connection: {e}')
            remove_connection(connection)
            connection.close()
            break
    # Close the connection with the client
    connection.close()

'''# Define a function to broadcast a message to all connected clients'''
def broadcast(message):
    # Iterate over all active connections
    for client_conn in connections:
        # Try to send the message to the client
        try:
            client_conn.send(message)
        # If an error occurs, print the error message and remove the client's connection
        except Exception as e:
            print(f'Error broadcasting message: {e}')
            remove_connection(client_conn)

'''Define a function to remove a client's connection from the list of active connections'''
def remove_connection(conn):
    # If the connection is in the list of active connections, close it and remove it from the list
    if conn in connections:
        conn.close()
        connections.remove(conn)


