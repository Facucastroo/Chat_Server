import tkinter as tk
import  threading,socket,datetime


FORMAT = "utf-8"
   
""" This class creates the Chat GUI window and its components."""
class Chat(tk.Tk):
   
    def __init__(self,host,port):
       
        self.host = host
        self.port = port
          
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr1=(self.host,self.port)
        try:
            self.client.connect(addr1)
        except Exception as e:
            print(f"{e}")
            raise
        else:
            self.Window = tk.Tk()
            self.Window.withdraw()
            threading.Thread(target=self.login_user()).start()
            self.Window.mainloop()
            
    def login_user(self):
       # This creates a new toplevel window for the login screen.
       self.login = tk.Tk()
       
       self.login.title("Login")
       self.login.resizable(width=False, height=False)
       self.login.configure(width=400, height=400,bg="white")
       
       self.LabelLoggin = tk.Label(self.login, text="LOGIN", justify=tk.CENTER, font="Helvetica 14 bold",bg="white")
       self.LabelLoggin.grid(row=0,column=0,columnspan=2,padx=5,pady=20)
    
       
       self.labelName = tk.Label(self.login, text="NAME: ", font="Helvetica 12")
       self.labelName.grid(row=1,column=0,padx=5,pady=20)

       self.entryName = tk.Entry(self.login, font="Helvetica 14")
       self.entryName.grid(row=1,column=1,padx=5,pady=20)
       self.entryName.focus()

       # This creates a button for the user to continue to the chat screen.
       self.Next = tk.Button(self.login, text="CONTINUE", font="Helvetica 14 bold", command=lambda:[self.Enter_Chat(self.entryName.get()),self.login.destroy()])
       self.Next.grid(row=2,column=0,columnspan=2,pady=20)
    
       
   # This method is called when the user clicks the 'CONTINUE' button.
   # It destroys the login window and calls the 'chat' method with the user's name.
    def Enter_Chat(self, name):
       self.chat_text(name)
       threading.Thread(target=self.receive).start()

   # This method creates the chat window and its components.
    def chat_text(self, name):
       
        self.name = name

        # This deiconifies the main window and sets its title, size, and background color.
        self.Window.deiconify()
        self.Window.title(f"{self.host}:{self.port}")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=500, height=580, bg="black")

        # This creates a label for displaying the user's name.
        self.labelHead = tk.Label(self.Window, bg="gray",fg="black",text=self.name,font="Helvetica 14 bold", pady=5)
        self.labelHead.grid(row= 0,column=0)

        # This creates a text widget for displaying messages.
        self.text = tk.Text(self.Window, bg="black",fg="white", padx=5, pady=5)
        self.text.grid(row= 1,column=0)

        # This creates a frame for holding the message entry field and send button.
        self.labelBottom = tk.Label(self.Window, bg="gray", height=80)
        self.labelBottom.grid(row= 2,column=0)

        # This creates an entry field for the user to enter messages.
        self.entryMsg = tk.Entry(self.labelBottom,width=40, bg="white")
        self.entryMsg.grid(row=3,column=0)
        self.entryMsg.focus()

        # This creates a button for the user to send messages.
        self.buttonMsg = tk.Button(self.labelBottom, text="Send", bg="gray", command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.grid(row= 3,column=1)

   # This method is called when the user clicks the 'Send' button.
   # It gets the message from the entry field, disables the entry field, and calls the 'sendMessage' method.
    def sendButton(self, msg):
       self.text.config(state=tk.DISABLED)
       self.msg = msg
       self.entryMsg.delete(0, tk.END)
       threading.Thread(target=self.sendMessage).start()

   # This method is called in a separate thread when the user clicks the 'Send' button.
   # It sends the message to the server.
    def sendMessage(self):
       DATE=datetime.datetime.now()
       DATE=DATE.strftime("%X")
       self.text.config(state=tk.DISABLED)
       while True:
           message = (f"{self.name}({DATE}): {self.msg}")
           self.client.send(message.encode(FORMAT))
           break

   # This method is called in a separate thread when the user connects to the server.
   # It receives messages from the server and enables the text widget.
    def receive(self):
       while True:
           try:
               message = self.client.recv(1024).decode(FORMAT)

               if message == 'NAME':
                   self.client.send(self.name.encode(FORMAT))
               else:
                   self.text.config(state=tk.NORMAL)
                   self.text.insert(tk.END, message+"\n\n")

                   self.text.config(state=tk.DISABLED)
                   self.text.see(tk.END)
           except:
               print("An error occurred!")
               self.client.close()
               break