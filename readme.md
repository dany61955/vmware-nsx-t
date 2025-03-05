## How It Works
Reads groups from group_data.txt, from NSX-T, and creates the group.
Uses REST API (PUT requests) to create/update objects.
Displays success/failure messages for each operation.

_Input File Structure_
1. group_data.txt (Defines the group details)
group_name:x.x.x.x,y.y.y.y

eg.
Web_Servers:192.168.1.10,192.168.1.11

DB_Servers:10.10.10.5,10.10.10.6


## Key Fixes for NSX-T
_Uses verify=False (disable SSL verification, but consider enabling it in production)_
_Enable SSL verification by replacing verify=False with verify='/path/to/cert.pem'._


## Support and troubleshooting
_Logging and Debugging: Add logging to capture API responses for troubleshooting._







