#!/usr/bin/env python3

import requests
import time

BIG_IP_ADDRESS = "f5-big-ip.yourloadbalancer.com"
AUTH_URL = f'https://{BIG_IP_ADDRESS}/mgmt/shared/authn/login'
DATA_GROUP_URL = f'https://{BIG_IP_ADDRESS}/mgmt/tm/ltm/data-group/internal/'

DATAGROUP_NAME = "YOUR-F5-DATAGROUP"

USERNAME_F5 = "f5username"
PASSWORD_F5 = "f5password"


def add_record_datagroup_f5(ip, description, datagroup):
    requests.packages.urllib3.disable_warnings()
    F5_URL = (DATA_GROUP_URL+datagroup)
    current_timestamp = int(time.time())
    headers = {
        'Content-Type': 'application/json',
    }
    params = {
        'options': f"records add {{ {ip} {{ data {description} }} }}"
    }
    data = {
        'name': datagroup
    }

    response = requests.patch(F5_URL, headers=headers, auth=(USERNAME_F5, PASSWORD_F5), params=params, json=data, verify=False)

    if response.status_code == 200:
        return True, datagroup, None
    else:
        error_message = f"Status code {response.status_code}. {response.json()['message']}"
        return False, datagroup, error_message

def delete_record_data_group_f5(ip, datagroup):
    requests.packages.urllib3.disable_warnings()
    F5_URL = (DATA_GROUP_URL+datagroup)
    
    headers = {
        'Content-Type': 'application/json',
    }
    params = {
        'options': f"records delete {{ {ip} }}"
    }
    data = {
        'name': datagroup
    }

    response = requests.patch(F5_URL, headers=headers, auth=(USERNAME_F5, PASSWORD_F5), params=params, json=data, verify=False)

    if response.status_code == 200:
        return True, datagroup, None
    else:
        error_message = f"Status code {response.status_code}. {response.json()['message']}"
        return False, datagroup, error_message


def main():
    # Example data for adding a record
    add_ip = "192.168.1.1"
    add_description = "Example description"
    
    # Add a record
    print(f"Adding record to data group '{DATAGROUP_NAME}'...")
    success, group, error = add_record_datagroup_f5(add_ip, add_description, DATAGROUP_NAME)
    if success:
        print(f"Successfully added record to data group '{group}' with IP '{add_ip}' and description '{add_description}'.")
    else:
        print(f"Failed to add record. Error: {error}")
    
    # Example data for deleting a record
    delete_ip = "192.168.1.1"
    
    # Delete the record
    print(f"Deleting record from data group '{DATAGROUP_NAME}'...")
    success, group, error = delete_record_data_group_f5(delete_ip, DATAGROUP_NAME)
    if success:
        print(f"Successfully deleted record with IP '{delete_ip}' from data group '{group}'.")
    else:
        print(f"Failed to delete record. Error: {error}")

if __name__ == "__main__":
    main()