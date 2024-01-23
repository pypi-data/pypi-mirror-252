"""
LicScan by @fakerybakery.
License: UPL

VERSION 1.0.0
"""
import argparse
import requests
import json
import requirements
from default_lic_list import default_licenses

def main():
    parser = argparse.ArgumentParser(description="Check your requirements to make sure your requirements have the correct licenses.")
    parser.add_argument("-f", "--file", required=True, help="Path to requirements.txt")
    parser.add_argument("-a", "--allowed", nargs="+", default=default_licenses, help="List of allowed licenses")
    args = parser.parse_args()
    print("IMPORTANT: Licenses are checked by checking if licenses include any of your approved licenses. This may not be accurate. Manual checking is suggested.")
    print("IMPORTANT: YOU ARE RESPONSIBLE FOR YOUR USAGE OF SOFTWARE. THIS SOFTWARE IS NOT INTENDED TO BE A REPLACEMENT FOR NORMAL DUE-DILIGENCE. MAKE SURE TO PERFORM NECESSARY CHECKS. YOU ARE RESPONSIBLE FOR COMPLYING WITH APPLICABLE LAWS AND REGULATIONS.")
    file_path = args.file
    allowed_licenses = args.allowed
    if args.allowed == default_licenses:
        print("WARNING: You may be using the DEFAULT list of licenses.Make sure to check that you are OK with these licenses.")
    not_ok_licenses = 0
    with open(file_path, 'r') as f:
        for req in requirements.parse(f):
            l = requests.get(f'https://pypi.org/pypi/{req.name}/json').json()
            try:
                license = l['info']['license']
                has_ok_license = False
                for lic in allowed_licenses:
                    if lic.strip():
                        if lic in license:
                            has_ok_license = True
                if not has_ok_license:
                    print(f"WARNING: Package {req.name} has NON-APPROVED license {license}")
                    not_ok_licenses += 1
            except:
                print(f"WARNING: Unable to parse license for package {req.name}")
                not_ok_licenses += 1
    if not_ok_licenses == 0:
        print("SUCCESS: All good, all your packages seem to have acceptable licenses! Make sure to manually check the licenses!")
if __name__ == "__main__":
    main()
