import subprocess
import pandas as pd
import re

whois_info = {
    'type': '',
    'netrange': '',
    'cidr': '',
    'inetnum': '',
    'netname': '',
    'nethandle': '',
    'parent': '',
    'nettype': '',
    'originas': '',
    'organization': '',
    'regdate': '',
    'updated': '',
    'ref': '',
    'orgid': '',
    'descr': '',
    'country': '',
    'admin-c': '',
    'tech-c': '',
    'abuse-c': '',
    'status': '',
    'remarks': '',
    'mnt-by': '',
    'mnt-lower': '',
    'mnt-routes': '',
    'mnt-irt': '',
    'last-modified': '',
    'address': '',
    'e-mail': '',
    'phone': '',
    'fax-no': '',
    'nic-hdl': '',
    'route': '',
    'origin': '',
    'stateprov': '',
    'postalcode': '',
    'comment': '',
    'Country': '',
    'city': '',
    'City': '',
    'orgname': '',
    'orgName': '',
    'org-name': '',
    'OrgName': ''
}

def get_whois(ip):
    data = whois_info.copy()

    try:
        cmd = ['whois', ip]
        whois_output = subprocess.check_output(cmd, universal_newlines=True)
        
        for key in data.keys():
            match = re.search(rf'{key}:\s+(.+)', whois_output, re.IGNORECASE)
            if match:
                data[key] = match.group(1).strip()

        return data
    except subprocess.CalledProcessError as e:
        print(f"Error fetching WHOIS for {ip}: {e}")
        return data

def whois():
    df = pd.read_csv("traceroute_output.csv")
    unique_ips = set(df['ip'])

    whois_data = {ip: get_whois(ip) for ip in unique_ips}

    for key in whois_info.keys():
        df[key] = df['ip'].map(lambda x: whois_data[x].get(key, ''))

    df.to_csv("whois_output.csv", index=False)
