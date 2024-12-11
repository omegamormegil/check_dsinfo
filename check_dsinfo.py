#!/usr/bin/env python3
"""
check_dsinfo
============
A simple utility to check configuration of Mirantis Container Runtime or the docker engine by comparing the output of `docker info` to a whitelist. 

Author: Nathan Jones
Email: njones@mirantis.com
============
check_dsinfo.py

This script checks Docker configurations against a YAML whitelist file. 
It identifies and reports configurations that are not in the whitelist, 
helping to ensure Docker setups meet required standards.

Usage:
- Run with two arguments: 
  python check_dsinfo.py <docker_info_output_file> <whitelist_file>
- Where <docker_info_output_file> is the output of 'docker info' saved to a text file,
  and <whitelist_file> is the path to 'docker_info_whitelist.yaml'.
- Output will list any configurations not in the whitelist.
"""

import sys
import argparse
import yaml
import re

def read_whitelist(file_path):
    """
    Read the YAML whitelist configurations from a file.

    :param file_path: Path to the YAML whitelist file
    :return: Dictionary where keys are configuration names and values are lists of allowed settings
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def check_docker_config(docker_info_file, whitelist):
    """
    Check Docker info against the whitelist and report discrepancies, ignoring lines that don't match expected format.

    :param docker_info_file: Path to the file containing docker info output
    :param whitelist: Dictionary of allowed configurations
    :return: List of non-whitelisted configurations
    """
    violations = []
    with open(docker_info_file, 'r') as file:
        for line in file:
            match = re.match(r'(\w+.*?\w)\s*:\s*(.*)', line.strip())
            if match:
                key, value = match.groups()
                key = key.strip().lower()
                value = value.strip().lower()
                if key in whitelist:
                    if value not in map(str.lower, whitelist[key]):
                        violations.append(line.strip())
                else:
                    violations.append(line.strip())
            # Here, if no match is found, the line is simply ignored
    return violations

def main():
    parser = argparse.ArgumentParser(description="Check Docker configuration against whitelist.")
    parser.add_argument('docker_info_file', help='Path to Docker info text file')
    parser.add_argument('whitelist_file', help='Path to whitelist YAML file')
    args = parser.parse_args()

    try:
        whitelist = read_whitelist(args.whitelist_file)
    except yaml.YAMLError as e:
        print(f"Error reading YAML whitelist file: {e}")
        sys.exit(1)

    violations = check_docker_config(args.docker_info_file, whitelist)

    if violations:
        print("The following Docker configurations are not in the whitelist:")
        for violation in violations:
            print(violation)
    else:
        print("All Docker configurations are within the whitelist.")

if __name__ == "__main__":
    main()
