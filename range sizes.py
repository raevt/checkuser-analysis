"""
    Rae Adimer

    This program takes a CheckUser log and outputs a csv with a list of checked range sizes.

    USAGE: 
    Copy log entries manually from the CheckUser log, save as 'checks.txt' in the same directory as this file.
    Note that this outputs two files: one for ipv4, and one for ipv6.
"""

import re
import os
import csv

def get_logs():
    with open('checks.txt', 'r', encoding='utf-8') as f:
        logs = f.read().splitlines()
    return logs

def get_addresses(logs):
    # Setup a dict to hold both lists for easier handling
    addresses = {
        "ipv4": [],
        "ipv6": [],
    }

    # Define the regex once instead of in the loop
    pattern_ipv4 = r"\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b"
    pattern_ipv6 = r"\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}(?:/\d{1,3})?\b"

    for log in logs:
        # Iterate through the log handling matches as they occur
        # and skipping places there were no matches after saying something.
        if re.search(pattern_ipv4, log):
            # Save the match so we can split it
            item = re.search(pattern_ipv4, log).group()

            # Split on the first '/' encountered
            try:
                _ip, cidr = item.split('/', 1)
            except ValueError:
                # If no cidr found, default to smallest.
                cidr = "32"
            
            # Add the range to list
            addresses['ipv4'].append(cidr)

        elif re.search(pattern_ipv6, log):
            # Save the match so we can split it
            item = re.search(pattern_ipv6, log).group()

            # Split on the first '/' encountered
            try:
                _ip, cidr = item.split('/', 1)
            except ValueError:
                # If no cidr found, default to smallest.
                cidr = "128"

            # Add the range to list
            addresses['ipv6'].append(cidr)
        else:
            continue
    
    return addresses


def export_ips(cidr):  
    # There are two keys in the dict, ipv4 and ipv6
    # Write each type to a separate file
    for v in cidr:
        with open(f"{v}_ranges.csv", "w", newline='') as csv_file:
            writer = csv.writer(csv_file)
            for rng in cidr[v]:
                writer.writerow([rng])

def main():
    # First, check and make sure neither file exists already
    if (
        os.path.exists("./ipv4_ranges.csv")
        or os.path.exists("./ipv6_ranges.csv")
    ):
        print("Output files already exist! Remove and try again...")
        raise SystemExit()
    
    # Do the magic
    export_ips(get_addresses(get_logs()))

if __name__ == "__main__":
    main()
