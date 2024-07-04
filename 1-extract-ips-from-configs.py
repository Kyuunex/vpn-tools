#!/usr/bin/env python3
# import json
import os

from OVPN import OVPN

CONFIG_DIR = "userdata/Provider_server_configs"
SAVE_FILE = "userdata/provider_ips.txt"

all_ips = []
all_ips_dict = {}


def extract(config_file, title=None):
    a = OVPN(config_file)
    for ip in set(a.ip_addresses):
        if not all_ips_dict.get(ip):
            all_ips_dict[ip] = []
        all_ips_dict[ip].append(title)
        all_ips.append(ip)


def export():
    output_buffer = ""
    for ip in all_ips:
        output_buffer += ip + "\n"

    output_file = open(SAVE_FILE, "w")
    output_file.write(output_buffer)
    output_file.close()


if __name__ == '__main__':
    for current_file in os.listdir(CONFIG_DIR):
        if current_file.endswith(".ovpn"):
            extract(CONFIG_DIR + "/" + current_file, current_file)

    all_ips = list(set(all_ips))
    all_ips.sort()
    export()
    # export_json()

