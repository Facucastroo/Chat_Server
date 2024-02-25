<header>

  # Chat_Server
  _Chat server, with Python socket_
</header>

### This code is an implementation of a basic multi-threaded chat using Python's built-in `socket module` and `tkinter` for the GUI. 

# Here's breakdown of the code 

### SERVER.PY
_The server is designed to accept multiple client connections, broadcast messages from one client to all other clients, and handle each client in a separate to improve concurrency._
1. **Imports:** The code imports the necessary modules - `socket, threading, and ipaddress`. 


2. **Constants:** The FORMAT constant is defined as `"utf-8"`, which is used for encoding and decoding messages.


3. **Global variables:** Two empty lists, connections and names, are created to store active connections and client names, respectively.

4. **Server initialization:** A socket object, server, is created using the `socket.socket()` function with the `AF_INET and SOCK_STREAM parameters`. This creates a TCP/IP socket.
   

5. **Server function**: The Server function takes a `HOST` and `PORT` as arguments, binds the server to the specified address and port, and starts listening for incoming connections. When a client connects, the server sends a message asking for the client's name, receives the name, and adds the client's name and connection to the respective lists. The server then broadcasts a welcome message to all connected clients and starts a new thread to handle the client's communication.
   
6. **Starting the chat server:** The startChat function initializes the server by creating a `new thread to run the Server function`.

7. **Client handling:** The `handle function` handles each client's communication in a separate thread. It receives messages from the client, broadcasts them to all connected clients, and removes the client's connection when they disconnect or an error occurs.
   
8. **Broadcasting messages:** The `broadcast function` sends a message to all connected clients. go through the list of connections with a for loop and send a message
      
9. **Removing connections:** The `remove_connection` function removes a client's connection from the list of active connections. go through the list of connections with a for loop and remove connection and close socket


### CLIENT.PY
_simple chat client using the Tkinter for the graphical user interface (GUI) and the socket library for creating a connection to a server. The chat client allows a user to log in with their name, send messages to other connected users, and view messages from the server in a scrollable text box._

***The code defines a `Chat class` that creates the GUI window and its components. When a Chat object is created, it takes in the host and port of the server as arguments. The __init__ method initializes the socket connection to the server and creates a new Tkinter window. It then starts a new thread to call the login_user method, which creates a login screen for the user to enter their name.***

1.  **The login_user method** `creates a new Tkinter window` for the login screen and adds a text entry field for the user's name. It also creates a `CONTINUE` button that calls the Enter_Chat method with the user's name when clicked.

2.  The **Enter_Chat method** destroys the login window and `calls the chat method` with the user's name. It also starts a new thread to call the receive method, which listens for incoming messages from the server.

3.  The **chat method** `creates` the main chat window and its components. It sets the title, size, and background color of the window, and adds a label for the user's name, a text box for displaying messages, a frame for holding the message entry field and send button, and an entry field for the user to enter messages. It also creates a scrollbar for the text box and disables the text box.

4.  The **sendButton method** is called when the user clicks the "Send" button. It gets the message from the entry field, disables the entry field, and starts a new thread to call the sendMessage method.

5.  The **sendMessage method** `sends` the message to the server. It first formats the message with the user's name and current time, then encodes the message as bytes and sends it to the server using the socket connection.

6.  The **receive method** is called in a separate thread when the user connects to the server. It `listens for incoming messages` from the server and enables the text box when a message is received. It then inserts the message into the text box and scrolls to the end of the text box. If an `error` occurs, it `closes the socket connection` and breaks out of the loop.

### GUI.PY

_This code is a graphical user interface (GUI) application for the chat program written in Python using the tkinter library. This app consists of three frames: Main, Create_server and Enter_server_

_the ctypes library to set the process DPI awareness to system aware._

1. `The APP class is the main class` that creates the GUI application and manages the different frames. It uses the tkinter library to create the GUI components. The APP class has a dictionary called all_frames that stores instances of all frames. The show_frame method shows a specific frame by raising it to the top of the stack.

2. The **Main frame** is the `initial screen` that appears when the application starts. It has a label "CHAT SERVER" and two buttons: "CREATE SERVER" and "ENTER A SERVER". When the user clicks on either button, the corresponding frame is displayed.

3. The **Create_server** frame allows the user to `create a new chat server` by specifying the host and port number. It has corresponding text entry fields for the user to input the values. It also has a "CREATE" button that starts the chat server with the specified host and port when clicked.

4. The **Enter_server** frame allows the user to `enter an existing chat server` by specifying the host and port number. It has corresponding text entry fields for the user to input the values. It also has an "ENTER" button that starts a chat client with the specified host and port when clicked.

_ The code uses the ipaddress module to validate the host input as a valid IP address. If the host input is invalid, an error message is displayed. If the host input is valid, the chat server or client is started with the specified host and port._

## Overall, all this code provides a simple and user-friendly GUI for a chat program that allows users to create and enter chat servers, implementing with sockets, threadings and GUI.
