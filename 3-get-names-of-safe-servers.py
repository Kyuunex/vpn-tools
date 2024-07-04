#!/usr/bin/env python3
import json
import os

from OVPN import OVPN

CONFIG_DIR = "userdata/Provider_server_configs"
SAFE_FILE = "userdata/not_banned_ips.txt"

SAVE_FILE_JSON = "userdata/not_banned_ips.json"

all_ips = []
all_ips_dict = {}
ip_whitelist = []
safe_ips = []

with open(SAFE_FILE, "r") as read_file:
    file_lines = read_file.readlines()
    for line in file_lines:
        safe_ips.append(line.strip())


def extract(config_file, title=None):
    a = OVPN(config_file)
    for ip in set(a.ip_addresses):
        if ip not in safe_ips:
            continue

        if not all_ips_dict.get(ip):
            all_ips_dict[ip] = []
        all_ips_dict[ip].append(title)
        all_ips.append(ip)


def export_json():
    output_file = open(SAVE_FILE_JSON, "w")
    output_file.write(json.dumps(all_ips_dict, indent=2))
    output_file.close()


if __name__ == '__main__':
    for current_file in os.listdir(CONFIG_DIR):
        if current_file.endswith(".ovpn"):
            extract(CONFIG_DIR + "/" + current_file, current_file)

    all_ips = list(set(all_ips))
    all_ips.sort()
    export_json()


