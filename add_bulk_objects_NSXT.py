import requests
import json
from requests.auth import HTTPBasicAuth

# NSX-T Manager Details
NSX_MANAGER = "nsx-manager-ip"
USERNAME = "admin"
PASSWORD = "your-password"

# API URL for Group Creation
GROUPS_API_URL = f"https://{NSX_MANAGER}/policy/api/v1/infra/domains/default/groups"

# Disable SSL warnings (remove in production)
requests.packages.urllib3.disable_warnings()

# Function to read input file
def load_group_data(filename):
    groups = []
    with open(filename, "r") as file:
        for line in file:
            if ":" in line:
                group_name, ip_list = line.strip().split(":")
                ip_addresses = ip_list.split(",")
                groups.append({"id": group_name.replace(" ", "_"), "name": group_name, "ip_addresses": ip_addresses})
    return groups

# Function to create/update Groups in NSX-T
def create_groups(groups):
    for group in groups:
        group_payload = {
            "resource_type": "Group",
            "id": group["id"],
            "display_name": group["name"],
            "expression": [
                {
                    "resource_type": "IPAddressExpression",
                    "ip_addresses": group["ip_addresses"]
                }
            ]
        }

        response = requests.patch(
            f"{GROUPS_API_URL}/{group['id']}",
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            headers={"Content-Type": "application/json"},
            data=json.dumps(group_payload),
            verify=False
        )

        if response.status_code in [200, 201]:
            print(f"Group '{group['name']}' updated successfully!")
        else:
            print(f"Failed to update Group '{group['name']}': {response.text}")

# Load data from input file
groups = load_group_data("group_data.txt")

# Create/update groups
create_groups(groups)
