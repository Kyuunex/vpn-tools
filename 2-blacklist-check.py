#!/usr/bin/env python3
import ipaddress

IP_BLACKLIST_FILES = [
    "userdata/blacklists/ipv4.txt",
    "userdata/blacklists/vpn-or-datacenter-ipv4-ranges.txt"
]

VPN_PROVIDER_IP_ADDRESSES = "userdata/provider_ips.txt"
SAVE_FILE = "userdata/not_banned_ips.txt"

vpn_provider_ip_list = []  # Service IP addresses to check against a blacklist
blacklisted_ip_ranges = []  # Blacklisted IP ranges
blacklisted_provider_ips = []
safe_ip_addresses = []  # End result, non blacklisted IP addresses

print("Loading the lists")
with open(VPN_PROVIDER_IP_ADDRESSES, "r") as read_file:
    for vpn_ip_str in read_file.readlines():
        vpn_provider_ip_list.append(vpn_ip_str.strip())

for IP_BLACKLIST_FILE in IP_BLACKLIST_FILES:
    with open(IP_BLACKLIST_FILE, "r") as read_file:
        for blacklisted_ip_range_str in read_file.readlines():
            blacklisted_ip_ranges.append(blacklisted_ip_range_str.strip())

blacklisted_ip_ranges = list(set(blacklisted_ip_ranges))

print("Checking ips...")
for blacklisted_ip_range_str in blacklisted_ip_ranges:
    blacklisted_ip_network = ipaddress.IPv4Network(blacklisted_ip_range_str)
    for ip_str in vpn_provider_ip_list:
        if ipaddress.IPv4Address(ip_str) in blacklisted_ip_network:
            blacklisted_provider_ips.append(ip_str)

print("Exporting")
output_buffer = ""
for ip in list(set(vpn_provider_ip_list) - set(blacklisted_provider_ips)):
    output_buffer += str(ip) + "\n"

output_file = open(SAVE_FILE, "w")
output_file.write(output_buffer)
output_file.close()

print("Done")
