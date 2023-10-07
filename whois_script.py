import subprocess
import pandas as pd
import re
from geopy.geocoders import Nominatim
import time

whois_info = {
    'inetnum': '',
    'netname': '',
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
    'origin': ''
}

geolocator = Nominatim(user_agent="geoapiExercises")
def get_lat_lon(address, country):
    try:
        location = geolocator.geocode(f"{address}, {country}")
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error geocoding {address}, {country}: {e}")
        return None, None

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

df = pd.read_csv("traceroute_output.csv")
unique_ips = set(df['ip'])

whois_data = {ip: get_whois(ip) for ip in unique_ips}

for key in whois_info.keys():
    df[key] = df['ip'].map(lambda x: whois_data[x].get(key, ''))

df.to_csv("whois_output.csv", index=False)
