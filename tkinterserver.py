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

def connect_to_client():
    global client_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Server started.")
    try:
        host = socket.gethostname()
        server_socket.bind((host, 1235))
        server_socket.listen()
        print("Waiting for the client to connect...")
        client_socket, address = server_socket.accept()  # returns tuple[socket, _RetAddress]
        name = client_socket.recv(1024).decode()
        print("Connected with:", address, name)
        receive_thread = Thread(target=receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
    except Exception as e:
        print("Error in connecting to client:", e)

def receive_messages():
    global client_socket
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

# Database connection
mydatabase = m.connect(host="localhost", user="root", password="root", database="xyz")
cursor = mydatabase.cursor()

# Tkinter setup
root = tk.Tk()
root.title("Server")

# Header label
header_label = tk.Label(root, text="Server Console", font=("Arial", 18, "bold"), pady=10)
header_label.pack()

# Connect button
connect_button = tk.Button(root, text="Start Server", command=connect_to_client, bg="#4CAF50", fg="white", padx=20, pady=10)
connect_button.pack()

# Message entry
message_entry = tk.Entry(root, width=50, font=("Arial", 12))
message_entry.pack()

# Send button
send_button = tk.Button(root, text="Send", command=send_message, bg="#008CBA", fg="white", padx=20, pady=10)
send_button.pack()

# Chat text area
chat_text = tk.Text(root, width=60, height=20, font=("Arial", 12))
chat_text.pack()

# Exit button
exit_button = tk.Button(root, text="Exit", bg="red", fg="white", command=root.destroy, padx=20, pady=10)
exit_button.pack()

root.mainloop()
