#!/usr/bin/env python3
# add_dsinfo_to_whitelist.py
# This script is intended to update or merge new Docker info configurations 
# into the existing whitelist file 'docker_info_whitelist.yaml'. 
# It can be used to dynamically add new configurations detected in a Docker environment.
#
# Usage (not implemented, conceptual):
# - Run with arguments:
#   python add_dsinfo_to_whitelist.py <new_docker_info_file> <existing_whitelist_file> <output_whitelist_file>
# - Where <new_docker_info_file> is a file with new Docker configurations,
#   <existing_whitelist_file> is the current whitelist, and 
#   <output_whitelist_file> is where the updated whitelist will be saved.

import yaml
import re
import argparse
import sys

def read_whitelist(file_path):
    """
    Read the YAML whitelist configurations from a file.

    :param file_path: Path to the YAML whitelist file
    :return: Dictionary where keys are configuration names and values are lists of allowed settings
    """
    with open(file_path, 'r') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(f"Error reading YAML file: {e}")
            sys.exit(1)

def add_to_whitelist(whitelist, key, value):
    """
    Add or update a configuration in the whitelist.

    :param whitelist: Dictionary of current whitelist configurations
    :param key: Configuration key
    :param value: Configuration value to add or update
    """
    if key not in whitelist:
        whitelist[key] = []
    if value not in whitelist[key]:
        whitelist[key].append(value)

def update_whitelist_with_docker_info(whitelist, docker_info_path):
    """
    Update the whitelist with configurations from Docker info.

    :param whitelist: Dictionary of current whitelist configurations
    :param docker_info_path: Path to the docker info text file
    """
    with open(docker_info_path, 'r') as file:
        for line in file:
            # Using regex to match lines like "Key: Value"
            match = re.match(r'\s*(\w+.*?\w)\s*:\s*(.*)', line.strip())
            if match:
                key, value = match.groups()
                key = key.strip().lower()
                value = value.strip().lower()
                add_to_whitelist(whitelist, key, value)
            # Special handling for nested structures
            elif 'Engine:' in line or 'containerd:' in line or 'runc:' in line or 'docker-init:' in line:
                # Here we could handle nested structures but for simplicity, we'll treat them as top-level
                key = line.split(':')[0].strip().lower()
                value = 'present'  # Mark as present since we're not going into detailed nested parsing
                add_to_whitelist(whitelist, key, value)

def write_whitelist(whitelist, file_path):
    """
    Write the updated whitelist back to a YAML file.

    :param whitelist: Dictionary of whitelist configurations
    :param file_path: Path where to write the updated YAML file
    """
    with open(file_path, 'w') as file:
        yaml.dump(whitelist, file, default_flow_style=False, sort_keys=False)

def main():
    parser = argparse.ArgumentParser(description="Update docker whitelist with docker info.")
    parser.add_argument('docker_info_file', help='Path to Docker info text file')
    parser.add_argument('whitelist_file', help='Path to whitelist YAML file')
    args = parser.parse_args()

    whitelist = read_whitelist(args.whitelist_file)
    update_whitelist_with_docker_info(whitelist, args.docker_info_file)
    write_whitelist(whitelist, args.whitelist_file)

if __name__ == "__main__":
    main()
