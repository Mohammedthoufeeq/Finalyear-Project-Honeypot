import pandas as pd
import re
import warnings

warnings.filterwarnings('ignore', message='This pattern has match groups')


def web_analyse():
    # Read data from CSV file
    df = pd.read_csv("web_data/web_data.csv", header=None, names=["IP", "USERNAME", "PASSWORD"])

    # Check for SQL injection with SELECT
    sql_regex = r".*(SELECT).*"
    if (df["USERNAME"].str.contains(sql_regex, flags=re.IGNORECASE)).any() or (
            df["PASSWORD"].str.contains(sql_regex, flags=re.IGNORECASE)).any():
        print("SQL injection with SELECT command has occurred. Attacked IP addresses:")
        print(df.loc[df["USERNAME"].str.contains(sql_regex, flags=re.IGNORECASE) |
                     df["PASSWORD"].str.contains(sql_regex, flags=re.IGNORECASE), "IP"].unique())

    # Check for SQL injection with UNION
    sql_regex = r".*(UNION).*"
    if (df["USERNAME"].str.contains(sql_regex, flags=re.IGNORECASE)).any() or (
            df["PASSWORD"].str.contains(sql_regex, flags=re.IGNORECASE)).any():
        print("SQL injection with UNION command has occurred. Attacked IP addresses:")
        print(df.loc[df["USERNAME"].str.contains(sql_regex, flags=re.IGNORECASE) |
                     df["PASSWORD"].str.contains(sql_regex, flags=re.IGNORECASE), "IP"].unique())

    # Check for SQL injection with CMD
    sql_regex = r".*(CMD).*"
    if (df["USERNAME"].str.contains(sql_regex, flags=re.IGNORECASE)).any() or (
            df["PASSWORD"].str.contains(sql_regex, flags=re.IGNORECASE)).any():
        print("SQL injection with CMD command has occurred. Attacked IP addresses:")
        print(df.loc[df["USERNAME"].str.contains(sql_regex, flags=re.IGNORECASE) |
                     df["PASSWORD"].str.contains(sql_regex, flags=re.IGNORECASE), "IP"].unique())

    # Check for SQL injection without spaces
    sql_regex_no_space = r".*(SELECT|UNION|CMD)[^ ]+.*"
    if (df["USERNAME"].str.contains(sql_regex_no_space, flags=re.IGNORECASE)).any() or (
            df["PASSWORD"].str.contains(sql_regex_no_space, flags=re.IGNORECASE)).any():
        print("SQL injection without spaces has occurred. Attacked IP addresses:")
        print(df.loc[df["USERNAME"].str.contains(sql_regex_no_space, flags=re.IGNORECASE) |
                     df["PASSWORD"].str.contains(sql_regex_no_space, flags=re.IGNORECASE), "IP"].unique())

    # Check for XSS attack
    xss_regex = r'<.*?(script|alert).*?>'
    if (df["USERNAME"].str.contains(xss_regex, flags=re.IGNORECASE)).any() or (
            df["PASSWORD"].str.contains(xss_regex, flags=re.IGNORECASE)).any():
        print("XSS attack has occurred. Attacked IP addresses:")
        print(df.loc[df["USERNAME"].str.contains(xss_regex, flags=re.IGNORECASE) |
                     df["PASSWORD"].str.contains(xss_regex, flags=re.IGNORECASE), "IP"].unique())

    # Check for OS command injection
    cmd_regex = re.compile(r"[;&|`\\<>]")
    if (df["USERNAME"].str.contains(cmd_regex)).any() or (df["PASSWORD"].str.contains(cmd_regex)).any():
        print("OS command injection has occurred. Attacked IP addresses:")
        print(df.loc[df["USERNAME"].str.contains(cmd_regex) | df["PASSWORD"].str.contains(cmd_regex), "IP"].unique())


    # Check if same username/password combination is used more than 5 times from the same IP
    ip_counts = df.groupby(['IP', 'USERNAME', 'PASSWORD']).size()
    if (ip_counts > 5).any():
        print("Repeated login attempts with same username/password combination.")


def ftp_analyse():
    # Read the data into a DataFrame
    df = pd.read_csv('ftp_data/ftp_data.csv', header=None, names=["IP", "PORT", "DATA"])

    # Check if same USER/PASS combination is used more than 5 times from the same IP
    user_pass_counts = df[df["DATA"].str.contains("USER") & df["DATA"].str.contains("PASS")].groupby(
        ['IP', 'DATA']).size()
    if (user_pass_counts > 5).any():
        print("Brute force attack has occurred with same USER/PASS combination.")
        print("Attacked IPs:", user_pass_counts[user_pass_counts > 5].index.get_level_values('IP').unique())

    # Check for SQL injection
    sql_regex = re.compile(r"(?i)\b(OR|UNION|SELECT)\b")
    sql_injection_counts = df[df["DATA"].str.contains(sql_regex)].groupby(
        ['IP', 'DATA']).size()
    if (sql_injection_counts > 0).any():
        print("SQL injection has occurred.")
        print("Attacked IPs:", sql_injection_counts[sql_injection_counts > 0].index.get_level_values('IP').unique())

    # Check for OS command injection
    cmd_regex = re.compile(r"[;&|`\\<>]")
    os_cmd_counts = df[df["DATA"].str.contains(cmd_regex)].groupby(
        ['IP', 'DATA']).size()
    if (os_cmd_counts > 0).any():
        print("OS command injection has occurred.")
        attacked_ips = os_cmd_counts[os_cmd_counts > 0].reset_index()['IP']
        print("Attacked IP addresses: ", attacked_ips.to_list())

# Main program
print("Choose an option:")
print("1. Web Analysis")
print("2. FTP Analysis")
option = input("Enter option number: ")

if option == '1':
    web_analyse()
elif option == '2':
    ftp_analyse()
else:
    print("Invalid option.")
