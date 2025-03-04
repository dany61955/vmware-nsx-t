import requests
import json
from requests.auth import HTTPBasicAuth

# NSX-T Manager Details
NSX_MANAGER = "nsx-manager-ip"
USERNAME = "admin"
PASSWORD = "your-password"

# API URLs (Updated for NSX-T)
GROUPS_API_URL = f"https://{NSX_MANAGER}/policy/api/v1/infra/domains/default/groups"
IP_OBJECTS_API_URL = f"https://{NSX_MANAGER}/policy/api/v1/infra/ip-sets"

# Read input files
def load_json_file(filename):
    with open(filename, "r") as file:
        return json.load(file)

# Function to create IP Sets in NSX-T
def create_ip_sets(ip_sets):
    for ip_set in ip_sets:
        payload = {
            "resource_type": "IPSet",
            "id": ip_set["id"],
            "display_name": ip_set["name"],
            "description": ip_set["description"],
            "ip_addresses": ip_set["ip_addresses"]
        }

        response = requests.put(
            f"{IP_OBJECTS_API_URL}/{ip_set['id']}",
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            verify=False
        )

        if response.status_code in [200, 201]:
            print(f"✅ IP Set '{ip_set['name']}' created successfully!")
        else:
            print(f"❌ Failed to create IP Set '{ip_set['name']}': {response.text}")

# Function to create Groups in NSX-T
def create_groups(groups):
    for group in groups:
        group_payload = {
            "resource_type": "Group",
            "id": group["id"],
            "display_name": group["name"],
            "description": group["description"],
            "expression": [
                {
                    "resource_type": "IPAddressExpression",
                    "ip_addresses": []  # Will be filled dynamically
                }
            ]
        }

        # Fetch IPs for Group Members
        for ip_set_id in group["members"]:
            response = requests.get(
                f"{IP_OBJECTS_API_URL}/{ip_set_id}",
                auth=HTTPBasicAuth(USERNAME, PASSWORD),
                headers={"Accept": "application/json"},
                verify=False
            )
            if response.status_code == 200:
                ip_data = response.json()
                group_payload["expression"][0]["ip_addresses"].extend(ip_data.get("ip_addresses", []))
            else:
                print(f"⚠️ Warning: IP Set '{ip_set_id}' not found!")

        # Create the group
        response = requests.put(
            f"{GROUPS_API_URL}/{group['id']}",
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            headers={"Content-Type": "application/json"},
            data=json.dumps(group_payload),
            verify=False
        )

        if response.status_code in [200, 201]:
            print(f"✅ Group '{group['name']}' created successfully!")
        else:
            print(f"❌ Failed to create Group '{group['name']}': {response.text}")

# Load data from files
ip_sets = load_json_file("ip_objects.json")
groups = load_json_file("group_objects.json")

# Execute creation process
create_ip_sets(ip_sets)
create_groups(groups)
