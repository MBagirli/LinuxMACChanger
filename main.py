#!usr/bin/env python

import optparse
import subprocess
import re

def getting_user_input():
    parse = optparse.OptionParser()
    parse.add_option("-i", "--interface", dest="interface", help="[-] Interface to change its MAC address")
    parse.add_option("-m", "--mac", dest="mac", help="[-] New MAC address")
    (option, argument) = parse.parse_args()
    if not option.interface:
        parse.error("[!] Provide an interface to change the MAC address; for more information, use the --help command")
    elif not option.mac:
        parse.error("[!] Enter the new MAC address; for more information, use the --help command")
    else:
        return option

def changing_the_mac(interface, mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["ifconfig", interface, "up"])

def getting_the_mac(interface):
    ifconfig_info = subprocess.check_output(["ifconfig", interface])
    my_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_info))
    if my_mac:
        return my_mac.group(0)
    else:
        print("[!] Could not read MAC address.")



options = getting_user_input()
current_mac = getting_the_mac(options.interface)
print(f"[-] Your current MAC address: {current_mac}")
changing_the_mac(options.interface, options.mac)
current_mac = getting_the_mac(options.interface)
if current_mac == options.mac:
    print(f"[+] MAC address successfully changed to: {options.mac}")
else:
    print(f"[!] MAC address not changed")
