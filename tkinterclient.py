import tkinter as tk
from threading import Thread
import socket
import mysql.connector as m

def send_message():
    message = message_entry.get()
    try:
        client_socket.send(bytes(message, 'utf-8'))
        chat_text.insert(tk.END, message + "\n")
        cursor.execute("INSERT INTO mess (c1) VALUES (%s)", (message,))
        mydatabase.commit()
        if message == 'stop':
            root.quit()  # Quit the Tkinter application if 'stop' is sent
    except Exception as e:
        print("Error sending data:", e)

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                chat_text.insert(tk.END, message + "\n")
                cursor.execute("INSERT INTO mess (c1) VALUES (%s)", (message,))
                mydatabase.commit()
        except Exception as e:
            print("Error receiving data:", e)
            break

def connect_to_server():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host = '192.168.1.224'
        client_socket.connect((host, 1235))
        client_name = name_entry.get()
        client_socket.send(bytes(client_name, 'utf-8'))
        chat_text.insert(tk.END, client_socket.recv(1024).decode() + "\n")
        chat_text.insert(tk.END, "Let's have a chat with the server\n")
        receive_thread = Thread(target=receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
    except Exception as e:
        print("Error connecting to server:", e)

# Database connection
mydatabase = m.connect(host="localhost", user="root", password="root", database="xyz")
cursor = mydatabase.cursor()

# Tkinter setup
root = tk.Tk()
root.title("Chat Client")

name_label = tk.Label(root, text="Enter your name:")
name_label.pack()

name_entry = tk.Entry(root)
name_entry.pack()

connect_button = tk.Button(root, text="Connect", command=connect_to_server)
connect_button.pack()

message_entry = tk.Entry(root)
message_entry.pack()

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

chat_text = tk.Text(root)
chat_text.pack()

yip=tk.Button(root,text="Exit",bg="red", command=root.destroy)
yip.pack()

root.mainloop()
