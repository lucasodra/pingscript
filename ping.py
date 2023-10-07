import subprocess
import csv
import re

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

def main():
    websites = ['craftwills.com', 'amazon.sg', 'shopee.sg', 'lazada.sg']
    output_file = 'ping_results.csv'

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Website', 'IP Address', 'TTL', 'Time (ms)'])

        for website in websites:
            output = ping_website(website)
            parsed_results = parse_ping_output(output)
            for result in parsed_results:
                writer.writerow([website, result['ip'], result['ttl'], result['time']])

    print(f"Results saved to {output_file}")

if __name__ == '__main__':
    main()
