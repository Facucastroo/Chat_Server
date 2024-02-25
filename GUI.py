# This line imports the 'ctypes' module and assigns the 'windll' attribute to a variable called 'windll'.
# This is used to set the process DPI awareness to system aware.
try:
   from ctypes import windll
   windll.shcore.SetProcessDpiAwareness(1)
except:
   pass

import tkinter as tk
from tkinter import ttk,messagebox
import tkinter.font as font
import  ipaddress,client
from server import startChat

# This line sets the format for encoding and decoding messages to 'utf-8'.
FORMAT = "utf-8"

""" This class creates the main window of the GUI application """
class APP(tk.Tk):
   def __init__(self,*args,**kwargs):
       super().__init__(*args,**kwargs)
       self.configure(bg = "black")
       # This line sets the font of the default font to size 12 and underline to True.
       font.nametofont("TkDefaultFont").configure(size = 12, underline = True)
       self.title("CHAT")
       self.columnconfigure( 0, weight = 1 )
       self.rowconfigure(0, weight = 1)
       # This creates a frame for holding all other frames.
       main_container = tk.Frame( self ,bg = "white")
       main_container.grid( padx = 40, pady = 50 , sticky = "nsew")
       # This creates a dictionary for storing all frames.
       self.all_frames = dict()
       # This loop creates instances of all frames and adds them to the dictionary.
       for F in (Main, Create_server, Enter_server):
           frame = F( main_container , self)
           self.all_frames[F] = frame
           frame.grid(row = 0, column = 0, sticky = "nsew")
       # This shows the first frame (Main).
       self.show_frame( Main )
       
   # This method shows a specific frame by raising it to the top of the stack.
   def show_frame(self,container):
       frame = self.all_frames[container]
       frame.tkraise()

   
""" This class creates the main frame of the GUI application."""
class Main(tk.Frame):
   def __init__(self, container, controller,*args, **kwargs):
       super().__init__(container, *args, **kwargs)
       
       #################### GRAPHIC STRUCTURE OF THE FRAME ####################

       self.configure(bg = "gray")
       L_1 = tk.Label( self, text = "CHAT SERVER", font="Helvetica 14 bold",bg = "black",fg = "blue",justify=tk.CENTER )
       L_1.grid(row = 0, column = 0, pady=10,columnspan=2)
       L_2 = tk.Label( self, text = "",bg = "gray" )
       L_2.grid(row = 2, column = 0, sticky = "n")
       B_C = ttk.Button( self, text = "CREATE SERVER", command = lambda:controller.show_frame( Create_server ) )
       B_C.grid(row = 3, column = 0,padx=25)
       B_E = ttk.Button( self, text = "ENTER A SERVER", command = lambda:controller.show_frame(Enter_server ) )
       B_E.grid(row = 3, column = 2)

""" This class creates the frame for creating a new server."""
class Create_server(tk.Frame):
    def __init__(self, container, controller,*args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.configure(bg = "gray")  

        self.HOST = tk.StringVar()
        self.PORT = tk.IntVar()

        #################### GRAPHIC STRUCTURE OF THE FRAME ####################

        L_1 = tk.Label( self, text = "CREATE SERVER", font="Helvetica 14 bold",bg = "black",fg = "blue",justify=tk.CENTER)
        L_1.grid(row = 0, column = 0, columnspan=2, pady=10, sticky = "n")
        L_2 = tk.Label( self, text = "HOST: ",font = ("Times New Roman",12),bg = "gray" )
        L_2.grid(row = 1, column = 0, sticky = "w")
        L_3 = tk.Label( self, text = "PORT: ", font = ("Times New Roman",12),bg = "gray" )
        L_3.grid(row = 2, column = 0, sticky = "w")
       
        self.E_Host = ttk.Entry( self, textvariable = self.HOST )
        self.E_Host.focus()
        self.E_Host.grid(row = 1, column = 1, padx = 5)
        self.E_Port = ttk.Entry( self, textvariable = self.PORT )
        self.E_Port.focus()
        self.E_Port.grid(row = 2, column = 1, padx = 5)

        B_C = ttk.Button(self, text = "CREATE", command = lambda:start_server(self.HOST.get(),self.PORT.get()))
        B_C.grid(row = 1, column = 3, rowspan=2, padx = 5)
        B_Back = ttk.Button(self, text = "BACK", command = lambda:controller.show_frame(Main))
        B_Back.grid(row = 3, column = 1, padx = 5, pady=10)

        #################### FUNCTIONS ####################
        
        def start_server(host,port):
            # Check if the host is valid IP address
            try:
                ipaddress.ip_address(host)
                # If it is, start the chat server with the given host and port
                startChat(host,port)
            # If an exception occurs during the IP address check or any problem
            except Exception as e:
                print(f"An error ocurred:{e}")
                # Display an error message using a message box
                messagebox.showerror("showerror", f"Error{e}")
            else:
                # Display a success message using a message box
                messagebox.showinfo("SERVER", f"Server Created in {self.HOST.get()}:{self.PORT.get()}")


""" This class creates the frame for enter in a server."""           
class Enter_server(tk.Frame):
    def __init__(self, container, controller,*args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.HOST = tk.StringVar()
        self.PORT = tk.IntVar()
        
        #################### GRAPHIC STRUCTURE OF THE FRAME ####################
        self.configure(bg = "gray")
        L_1 = tk.Label( self, text = "ENTER SERVER", font="Helvetica 14 bold",bg = "black",fg = "blue" )
        L_1.grid(row = 0, column = 0, columnspan=2, pady=10, sticky = "n")
        L_2 = tk.Label( self, text = "HOST: ", font = ("Times New Roman",12),bg = "gray" )
        L_2.grid(row = 1, column = 0, sticky = "w")
        L_3 = tk.Label( self, text = "PORT: ", font = ("Times New Roman",12),bg = "gray" )
        L_3.grid(row = 2, column = 0, sticky = "w")
       
        
        self.E_1 = ttk.Entry( self, textvariable = self.HOST )
        self.E_1.focus()
        self.E_1.grid(row = 1, column = 1, padx = 5)
        self.E_2 = ttk.Entry( self, textvariable = self.PORT )
        self.E_2.focus()
        self.E_2.grid(row = 2, column = 1, padx = 5)
        
        # create instance for chat, enter the server, the chat
        B_E = ttk.Button(self, text = "ENTER", command = lambda:Enter_chat(self.HOST.get(),self.PORT.get()))
        B_E.grid(row = 1, column = 3, rowspan=2, padx = 5)
        B_Back = ttk.Button(self, text = "BACK", command = lambda:controller.show_frame(Main))
        B_Back.grid(row = 3, column = 1, padx = 5, pady=10)

        #################### FUNCTIONS ####################

        def Enter_chat(HOST,PORT):
            try:
                host=str(ipaddress.ip_address(HOST))
                client.Chat(host,int(PORT))
            except Exception as e:
                print
                messagebox.showerror("showerror", f"Error{e}")
       
root = APP()

root.mainloop()
       