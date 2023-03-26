import pandas as pd
import re

def ftp_analyze(filename):
    df = pd.read_csv(filename, header=None, names=['IP', 'PORT', 'DATA'])

    # Check for brute force attacks
    ip_counts = df['IP'].value_counts()
    if ip_counts.max() > 5:
        print(f"Brute force attack has occurred from IP: {ip_counts.idxmax()}")
        for ip, count in ip_counts.iteritems():
            if count > 5:
                repeated_logins = df[df['IP'] == ip]['DATA'].str.extract(r'USER\s+(\w+)\s+PASS\s+(\w+)', flags=re.IGNORECASE)
                if repeated_logins.notnull().all(axis=1).sum() > 5:
                    print(f"Repeated login attempts from IP {ip} with same username/password combination.")
                    break

    # Check for SQL injection attacks
    sql_regex = r'(?:DROP\s+(?:TABLE|DATABASE)|INSERT\s+INTO\s+.*\s+VALUES|SELECT\s+.+\s+FROM|UPDATE\s+.+\s+SET)'
    sql_counts = df[df['DATA'].str.contains(sql_regex, flags=re.IGNORECASE)]['IP'].value_counts()
    if sql_counts.max() > 5:
        print(f"SQL injection attack has occurred from IP: {sql_counts.idxmax()}")

    # Check for OS command injection attacks
    os_regex = r'(?:;\s*(?:cat|ls|ps|rm|echo|cp|mv|kill|mkdir|rmdir|uname|whoami|id))'
    os_counts = df[df['DATA'].str.contains(os_regex, flags=re.IGNORECASE)]['IP'].value_counts()
    if os_counts.max() > 5:
        print(f"OS command injection attack has occurred from IP: {os_counts.idxmax()}")

# Example usage
ftp_analyze('ftp_data.csv')

