import subprocess
import csv
import re
from datetime import datetime

def ping_website(website):
    try:
        response = subprocess.check_output(['ping', '-c', '4', website], stderr=subprocess.STDOUT, universal_newlines=True)
        return response
    except subprocess.CalledProcessError as e:
        return e.output

def parse_ping_output(output):
    results = []
    pattern = r'(?P<bytes>\d+) bytes from (?P<ip>\S+): icmp_seq=\d+ ttl=(?P<ttl>\d+) time=(?P<time>\S+) ms'
    matches = re.findall(pattern, output)

    for match in matches:
        results.append({
            'ip': match[1],
            'ttl': match[2],
            'time': match[3]
        })
    return results

def ping(vpn):
    # ################
    # UPDATE THIS ONLY
    # ################
    vpnCountry = vpn

    with open('target.csv', 'r') as file:
        reader = csv.reader(file)
        websites = [row[0] for row in reader]

    output_file = 'ping_results.csv'

    with open(output_file, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        #writer.writerow(['vpn', 'datetime', 'website', 'ip', 'ttl', 'time'])

        for website in websites:
            current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            output = ping_website(website)
            parsed_results = parse_ping_output(output)
            for result in parsed_results:
                writer.writerow([vpnCountry, current_datetime, website, result['ip'], result['ttl'], result['time']])

    print(f"Results saved to {output_file}")
