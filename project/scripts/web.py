import csv
import os
import logging
from flask import Flask, render_template, request, redirect, session
import netifaces as ni
from pyfiglet import Figlet
from colorama import Fore, Style


class Honeypot:
    def __init__(self, port):
        self.port = port
        self.app = Flask(__name__)
        self.get_host()
        self.run()

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

    def write_to_file(self, ip, username, password):
        # Check if the folder exists, if not create it
        if not os.path.exists('web_data'):
            os.makedirs('web_data')
        file_path = os.path.join('web_data', 'web_data.csv')
        with open(file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([ip, username, password])

    def run(self):
                # setup logging
        if not os.path.exists('web_log'):
            os.makedirs('web_log')
        log_file = os.path.join('web_log', 'web.log')
        logging.basicConfig(filename=log_file, level=logging.WARNING)
        # Flask routes and other code
        @self.app.route('/')
        def index():
            return render_template('index.html')


        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')
                # Log the payloads
                logging.warning(f"Username: {username}, Password: {password}")
                self.write_to_file(request.remote_addr, username, password)  # Write to the file
                # Simulating a successful login
                if 'admin' in username and 'password' in password:
                    session['username'] = username
                    return redirect('/confidential')
                else:
                    return "Invalid credentials"
            return render_template('login.html')

        @self.app.route('/confidential')
        def confidential():
            if 'username' in session:
                return render_template('confidential.html', username=session['username'])
            else:
                return redirect('/login')

        self.app.secret_key = 'secret'
        self.app.run(host=self.host, port=self.port)

try:
    if __name__ == '__main__':
        honeypot = Honeypot(80)
except KeyboardInterrupt:
    print(Fore.BLUE + Style.BRIGHT + "Exiting Framework" + Style.RESET_ALL)