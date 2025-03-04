## How It Works
Reads IP objects from ip_objects.json and creates them in NSX-T.
Reads groups from group_objects.json, retrieves the corresponding IPs from NSX-T, and creates the group.
Uses REST API (PUT requests) to create/update objects.
Displays success/failure messages for each operation.

_Input File Structure_
1. ip_objects.json (Defines individual IP objects)

make a list for more than one

    {
        "id": "ip-object-1",
        "name": "Web-Servers",
        "description": "Web servers subnet",
        "ip_addresses": ["192.168.1.10", "192.168.1.11"]
    },
    {
        "id": "ip-object-2",
        "name": "DB-Servers",
        "description": "Database servers subnet",
        "ip_addresses": ["10.10.10.5", "10.10.10.6"]
    }    

2. group_objects.json (Defines groups that use IP objects)

make a list for more than one

    {
        "id": "web-db-group",
        "name": "Web and DB Servers",
        "description": "Group containing web and database servers",
        "members": ["ip-object-1", "ip-object-2"]
    }



## 📌 Key Fixes for NSX-T
_Fixed the API URL for IP Sets in NSX T varient → IP_OBJECTS_API_URL now uses /infra/ip-sets/{id}_
_Uses verify=False (disable SSL verification, but consider enabling it in production)_



## Support and troubleshooting
_Enable SSL verification by replacing verify=False with verify='/path/to/cert.pem'._
_Logging and Debugging: Add logging to capture API responses for troubleshooting._







