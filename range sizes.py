"""
    Rae Adimer

    This program takes a CheckUser log and outputs a csv with a list of checked range sizes.

    USAGE: 
    Copy log entries manually from the CheckUser log, save as 'checks.txt' in the same directory as this file.
    Note that this outputs two files: one for ipv4, and one for ipv6.
"""

import re
import csv

def get_logs():
    logs = []
    with open('checks.txt', 'r', encoding='utf-8') as f:
        for line in f:
            logs.append(line)
    return logs

def get_addresses(logs):
    ipv4_addresses = []
    ipv6_addresses = []
    for log in logs:
        pattern_ipv4 = r"\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b"
        pattern_ipv6 = r"\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}(?:/\d{1,3})?\b"
        match_ipv4 = re.search(pattern_ipv4, log)
        match_ipv6 = re.search(pattern_ipv6, log)
        if match_ipv4:
            ipv4_addresses.append(match_ipv4.group())
        if match_ipv6:
            ipv6_addresses.append(match_ipv6.group())
    return ipv4_addresses, ipv6_addresses

def get_ipv4_dist(ipv4_addresses):
    ipv4_dist = []
    for string in ipv4_addresses:
        try:
            IP, size = string.split('/')
            ipv4_dist.append(size)
        except:
            ipv4_dist.append('32')
    return ipv4_dist

def get_ipv6_dist(ipv6_addresses):
    ipv6_dist = []
    for string in ipv6_addresses:
        try:
            IP, size = string.split('/')
            ipv6_dist.append(size)
        except:
            ipv4_dist.append('128')
    return ipv6_dist

def export_ipv4(ipv4_dist):
    with open('ipv4_ranges.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for range_size in ipv4_dist:
            writer.writerow([range_size])

def export_ipv6(ipv6_dist):
    with open('ipv6_ranges.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for range_size in ipv6_dist:
            writer.writerow([range_size])

def main():
    logs = get_logs()
    ipv4_addresses, ipv6_addresses = get_addresses(logs)
    ipv4_dist = get_ipv4_dist(ipv4_addresses)
    ipv6_dist = get_ipv6_dist(ipv6_addresses)
    export_ipv4(ipv4_dist)
    export_ipv6(ipv6_dist)

if __name__ == "__main__":
    main()
