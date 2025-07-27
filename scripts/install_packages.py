import subprocess

# List of packages to be installed
packages = ['socket', 'logging', 'datetime', 'threading',
            'netifaces', 'queue', 'pyfiglet', 'colorama', 'csv', 'pandas', 'flask']

# Installing packages
for package in packages:
    subprocess.call(['pip3', 'install', package])

