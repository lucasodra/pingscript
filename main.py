import time
from traceroute_script import traceroute
from whois_script import whois
from ping_script import ping

def main():
    # Define the code you want to run every hour here
    print("Running ping, traceroute and whois script...")
    vpn = input('Enter the country you are searching from: ')

    # Set the interval in seconds (1 hour = 3600 seconds)
    interval = 3600

    while True:
        # Call your function
        traceroute(vpn)
        whois()
        ping(vpn)
        
        # Sleep for the specified interval
        time.sleep(interval)

if __name__ == '__main__':
    main()