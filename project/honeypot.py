import os
from pyfiglet import Figlet
from colorama import Fore, Style


try:
    print(Fore.YELLOW + Style.BRIGHT + '##########################################################' + Style.RESET_ALL)
    f = Figlet(font='big')
    banner = f.renderText('Honeypot Framework')
    print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)

    print(
        Fore.YELLOW + '------' + Fore.GREEN + Style.BRIGHT + 'Honeypot Framework 1.0' + Fore.YELLOW + Fore.RED + '    @MohamedThoufeeq' + Fore.YELLOW + '------' + Style.RESET_ALL)

    print(Fore.YELLOW + Style.BRIGHT + '##########################################################' + Style.RESET_ALL)
    print(Fore.BLUE + Style.BRIGHT + "Please select a Service to run:" + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "0. Install Dependencies (pip packages) " + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "1. FTP Honeypot" + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "2. Web Honeypot" + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "3. FTP Honeypot Analyse" + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "4. Exit" + Style.RESET_ALL)

    choice = input(Fore.BLUE + Style.BRIGHT + "Enter your choice: " + Style.RESET_ALL)
    folder = "scripts"
    if choice == "1":
        os.system(f"python {folder}/ftp.py")
    elif choice == "2":
        os.system(f"python {folder}/web.py")
    elif choice == "3":
        os.system(f"python analyse.py")
    elif choice == "0":
        os.system(f"python {folder}/install_packages.py")
    elif choice == "4":
        print(Fore.BLUE + Style.BRIGHT + "Exiting Framework" + Style.RESET_ALL)
    else:
        print(Fore.RED + Style.BRIGHT + "Invalid choice. Please select a valid option." + Style.RESET_ALL)
except KeyboardInterrupt:
    print(Fore.BLUE + Style.BRIGHT + "Exiting Framework" + Style.RESET_ALL)


