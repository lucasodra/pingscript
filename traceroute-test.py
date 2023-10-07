import subprocess
import re
import csv
import datetime

vpn = "Singapore"
with open("target.csv", "r") as file:
    websites = [line.strip() for line in file]

results = []

for website in websites:
    try:
        cmd_output = subprocess.check_output(['traceroute', '-w', '5', '-m', '100', website], universal_newlines=True, stderr=subprocess.STDOUT)

        current_hop = None
        sub_hop = 0
        for line in cmd_output.split("\n"):
            print("=====")
            print(line)

            if line.startswith("traceroute:") or line.startswith("traceroute to") or line.strip() == "* * *":
                continue
            # match = re.match(r"\s*(\d+)\s+((?:\d{1,3}\.){3}\d{1,3})\s+\((?:\d{1,3}\.){3}\d{1,3}\)\s+([\d\.]+)\s+ms(?:\s+([\d\.]+)?\s*ms?)?(?:\s+([\d\.]+)?\s*ms?)?", line)
            # match = re.match(r"\s*(\d+)\s+((?:\d{1,3}\.){3}\d{1,3}).*\((?:\d{1,3}\.){3}\d{1,3}\)\s+([\d\.]+)\s+ms(?:\s+([\d\.]+)?\s*ms?)?(?:\s+([\d\.]+)?\s*ms?)?", line)
            # match = re.match(r"\s*(\d+)\s+.*\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)\s+([\d\.]+)\s+ms(?:\s+([\d\.]+)?\s*ms?)?(?:\s+([\d\.]+)?\s*ms?)?", line)
            # match = re.match(r"\s*(\d+)?\s*.*\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)\s+([\d\.]+)\s+ms(?:\s+([\d\.]+)?\s*ms?)?(?:\s+([\d\.]+)?\s*ms?)?", line)
            match = re.match(r"\s*(\d+)?\s+.*\s?\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)\s+([\d\.]+)\s+ms(?:\s+([\d\.]+)?\s*ms?)?(?:\s+([\d\.]+)?\s*ms?)?", line)

            if match:
                print("Captured Groups:", match.groups())

                if match.group(1):
                    print("match1")
                    hop = match.group(1)
                    current_hop = hop
                    sub_hop = 0
                else:
                    print("match2")
                    sub_hop += 1
                    hop = f"{current_hop}-{sub_hop}"

                ip = match.group(2)
                speed1 = match.group(3)
                speed2 = match.group(4) if match.group(4) else ""
                speed3 = match.group(5) if match.group(5) else ""

                print([website, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), hop, vpn, ip, speed1, speed2, speed3])
                results.append([website, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), hop, vpn, ip, speed1, speed2, speed3])

    except subprocess.CalledProcessError as e:
        print(f"Error executing traceroute for {website}: {str(e)}")

with open("traceroute_output.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['website','datetime', 'hop', 'vpn', 'ip', 'speed1', 'speed2', 'speed3'])
    writer.writerows(results)
