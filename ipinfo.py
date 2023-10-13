import csv
import subprocess
import json
import re

def ipinfo(ip_address):
    try:
        cmd_output = subprocess.check_output(['curl', '-s', f'https://ipinfo.io/{ip_address}'], universal_newlines=True, stderr=subprocess.STDOUT)
        print(cmd_output)

        # Use regular expressions to extract the JSON portion from the output
        json_match = re.search(r'{\s*"ip":.+}', cmd_output, re.DOTALL)
        
        if json_match:
            # Extract and parse the JSON data
            json_data = json_match.group(0)
            ip_info = json.loads(json_data)

            # Split the "loc" value into latitude and longitude
            loc = ip_info.get('loc', '')
            lat, lon = loc.split(',')

            # Append JSON information to the same row
            ip_info = {
                "city": ip_info.get('city', ''),
                "region": ip_info.get('region', ''),
                "country": ip_info.get('country', ''),
                "lat": lat,
                "lon": lon,
                "org": ip_info.get('org', ''),
                "timezone": ip_info.get('timezone', '')
            }
            return ip_info

    except json.JSONDecodeError as e:
        print(f'Error parsing JSON for {ip_address}: {e}')
    except Exception as e:
        print(f'Error fetching IP info for {ip_address}: {str(e)}')

def main():
    with open("traceroute_output.csv", "r") as file:
        websites = [line.strip().split(',') for line in file]
        
        # Create a new CSV file for the updated data
        with open("traceroute_output_updated.csv", "w", newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Write headers to the new file
            headers = ["website", "datetime", "hop", "vpn", "ip", "speed1", "speed2", "speed3",
                       "city", "region", "country", "lat", "lon", "org", "timezone"]
            csv_writer.writerow(headers)

            # Iterate through every website and get their IP address
            for website in websites:
                ip_address = website[4]
                if ip_address != 'ip':
                    ip_info = ipinfo(ip_address)
                    website.extend(ip_info.values())  # Append JSON info to the row
                    csv_writer.writerow(website)

if __name__ == '__main__':
    main()
