import subprocess
from datetime import datetime

print('Starting traceroute...')
# Run traceroute to www.google.com with a timeout for each hop and store the output in a file
traceroute_process = subprocess.Popen(['traceroute', '-w', '1', 'www.google.com'], stdout=subprocess.PIPE)
tracerouteFileName = str(datetime.now().strftime('%d-%m-%Y %H%M HRS')) + '_traceroute.output.txt'
ipFileName = str(datetime.now().strftime('%d-%m-%Y %H%M HRS')) + '_ip_address.output.txt'

print('Writing to ', tracerouteFileName)
with open(tracerouteFileName, 'wb') as output_file:
    lineCount = 0
    while True:

        line = traceroute_process.stdout.readline()
        lineCount += 1
        if not line:
            break

        output_file.write(line)
        output_file.flush()  # Flush the output to the file immediately
    print('Traceroute Completed')
    print('{} number of lines processed.'.format(lineCount))

print('Writing to ', ipFileName)
# Extract IP addresses from the traceroute output and save them to a file
with open(tracerouteFileName, 'r') as input_file, open(ipFileName, 'w') as output_file:
    count = 0
    for line in input_file:
        columnNo = 0
        # Assuming that IP addresses are in the second column, separated by spaces
        columns = line.strip().split()
        for columnNo, column in enumerate(columns):
            if column[0] == '(':
                ip_address = columns[columnNo]
                break
            columnNo += 1
        if (ip_address[0] != '*'):
            if (ip_address[0] == '('):
                ip_address = ip_address.replace('(', '').replace(')', '')
            output_file.write(ip_address + '\n')
            count += 1
    print('IP address extraction completed.')
    print('{} number of IP addresses'.format(count))
