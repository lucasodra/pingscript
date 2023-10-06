import subprocess
from datetime import datetime
import re

inputFile = input('Enter filename here: ')
filename = str(datetime.now().strftime('%d-%m-%Y %H%M HRS')) + '_whois_output.txt'
print('whois analysis loading...')
# Open the text file containing IP addresses
with open(inputFile, 'r') as textfile:
    # Create or open the output file for country information
    with open(filename, 'w') as outputfile:
        for line in textfile:
            # Remove leading and trailing whitespace from each line
            ip = line.strip()

            # Run the whois command and capture its output
            whois_output = subprocess.check_output(['whois', ip], universal_newlines=True)

            # Search for the country information in the whois output
            country = ''
            city = ''
            orgname = ''
            for whois_line in whois_output.split('\n'):
                if re.search(r'(?i)Country', whois_line):
                    country = whois_line.split(':')[-1].strip()
                elif re.search(r'(?i)City', whois_line):
                    city = whois_line.split(':')[-1].strip()
                elif re.search(r'(?i)OrgName', whois_line):
                    orgname = whois_line.split(':')[-1].strip()
                elif re.search(r'(?i)Org-Name', whois_line):
                    orgname = whois_line.split(':')[-1].strip()

            # Write the IP address and country information to the output file
            outputfile.write(f"IP Address: {ip}, Country: {country}, City: {city}, OrgName: {orgname}\n")   

print("whois extraction completed.")

