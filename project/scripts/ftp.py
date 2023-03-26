import socket
import logging
import datetime
import threading
import netifaces as ni
import queue
from pyfiglet import Figlet
from colorama import Fore, Style
import csv
import subprocess
import re
import pandas as pd
import os


# Define the file path for the log file
log_dir = "ftp_log"
log_file = os.path.join(log_dir, "ftp.log")

# Check if the log directory exists and create it if it does not
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure logging to use the log file
logging.basicConfig(filename=log_file, level=logging.INFO)

# Initialize a thread-safe queue to store the log data
log_queue = queue.Queue()


class FTPHoneypot:
    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.get_host()
        if self.check_port(self.port):
            print(f"Port {self.port} is already in use.")
            return
        self.bind()
        self.sock.listen(5)
        
    def check_port(self, port):
        output = subprocess.run(["netstat", "-lnp"], stdout=subprocess.PIPE)
        output_str = output.stdout.decode()
        data = output_str.split("\n")
        data = [i.split() for i in data]
        #df=["Proto","Recv-Q","Send-Q","Local Address","Foreign Address","State","PID/Program name","column8","column9","column10"]
        #print(df)
        if f":{port} " in output_str:
            print(Fore.BLUE + Style.BRIGHT + f"Port {port} is in use." + Style.RESET_ALL)
            return True
        else:
            print(Fore.BLUE + Style.BRIGHT + f"Port {port} is not in use." + Style.RESET_ALL)
            print(Fore.BLUE + Style.BRIGHT + "Server Started" + Style.RESET_ALL)
            return False


    def get_host(self):
        interfaces = ni.interfaces()
        ip_list = []
        for i in interfaces:
            if i == 'lo':
                continue
            ifaddresses = ni.ifaddresses(i)
            ip_list.append(ifaddresses[ni.AF_INET][0]['addr'])
        print(Fore.BLUE + Style.BRIGHT + "Select an IP address to use for the honeypot:" + Style.RESET_ALL)
        for i, ip in enumerate(ip_list):
            print(Fore.YELLOW + Style.BRIGHT + f"{i + 1}. {ip}" + Style.RESET_ALL)
        choice = input()
        self.host = ip_list[int(choice) - 1]
        print(Fore.BLUE + Style.BRIGHT + f'Honeypot listening on {self.host}:{self.port}' + Style.RESET_ALL)

    def bind(self):
        try:
            self.sock.bind((self.host, self.port))
        except socket.error as e:
            if e.errno == 98:
                print(Fore.RED + f"Error: {self.host}:{self.port} is already in use." + Style.RESET_ALL)
            else:
                print("An error occurred while trying to bind the socket:", e)

    def write_to_file(self, ip, port, data):
        # Define the file path for the CSV file
        dir_path = "ftp_data"
        file_path = os.path.join(dir_path, "ftp_data.csv")

        # Check if the data directory exists and create it if it does not
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Open the CSV file in append mode
        with open(file_path, "a", newline='') as f:
            # Create a CSV writer object
            writer = csv.writer(f)
            # Write the data as a new row in the CSV file
            writer.writerow([ip, port, data])

    def check_credentials(self, username, password):
        valid_credentials = {'admin': 'password', 'user': '123456'}
        if username in valid_credentials and valid_credentials[username] == password:
            return True
        else:
            return False
   
    def handle_client(self, client, addr):
        self.write_to_file(addr[0], self.port, 'CONNECTED')
        client.send(b"220 Welcome to the FTP server.\r\n")
        while True:            
            data = client.recv(1024).decode('utf-8')
            self.write_to_file(addr[0], self.port, data)
            if not data:
                break
            elif data.strip().upper() == 'QUIT':
                client.send(b"221 Goodbye.\r\n")
                client.close()
                break
            elif data.strip().upper().startswith('USER'):
                self.write_to_file(addr[0], self.port, data)
                # Get the username from the data
                match = re.match("USER (\w+)", data)
                if match:
                    username = match.groups()[0]
                    client.send(b"331 Please specify the password.\r\n")
                else:
                    client.send(b"502 Command not implemented.\r\n")
                
                
            elif data.strip().upper().startswith('PASS'):
                match = re.match("PASS (\w+)", data)
                if match:
                    password = match.groups()[0]
                    if self.check_credentials(username, password):
                        client.send(b"230 Login successful.\r\n")
                    else:
                        client.send(b"530 Invalid username or password.\r\n")
                else:
                    client.send(b"502 Command not implemented.\r\n")
            else:
                client.send(b"502 Command not implemented.\r\n")

                    

    def listen(self):
        while True:
            client, addr = self.sock.accept()
            client.send(b"220 (FTB Database Records)\r\n")
            client.send(b"Avaliable Commands USER <username> and PASS <password>\r\n")
            self.client_handler = threading.Thread(target=self.handle_client, args=(client, addr))
            self.client_handler.start()
            logging.info(f'{datetime.datetime.now()} : Connection from {addr} on port {self.port}')


try:
    # use this code to start the honeypot
    honeypot = FTPHoneypot(21)
    honeypot.listen()


except KeyboardInterrupt:
    print(Fore.BLUE + Style.BRIGHT + "Exiting Framework" + Style.RESET_ALL)
