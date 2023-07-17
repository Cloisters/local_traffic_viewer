Local Traffic Viewer

Local Traffic Viewer is a Python script that allows users to scan their home network to find active IP addresses along with their system owner (hostname) and HTTP response codes. It provides a graphical user interface (GUI) that displays the results in a table-like format.

Features:

Scans the local network to find active IP addresses.
Retrieves the system owner (hostname) for each active IP address.
Performs a simple ping to check if an IP address is online.
Retrieves HTTP response codes from web servers on the network.
Updates the GUI with the scan results in real-time.
Displays IP addresses in a green background if online, and red if offline.
Provides a progress bar to show the progress of the scan.
Requirements:

Python 3
tkinter library
concurrent.futures library
socket library
os library
requests library
How to Use:

Ensure you have Python 3 and the required libraries installed.
Clone the repository or download the local_traffic_viewer.py file.
Run the script using python local_traffic_viewer.py.
The GUI will open, and you can click the "Scan Network" button to start the scanning process.
The table will be populated with the active IP addresses, system owners, and HTTP response codes (if applicable) in real-time.
Note:

The script uses concurrent execution to speed up the scanning process.
The scan may take a few seconds to complete depending on the network size and the number of online devices.
HTTP response codes will be "N/A" for devices that are not web servers or don't respond within a timeout.
Example Output:


Copy code
+----------------+----------------+---------------+
|   IP Address   |  System Owner  | Response Code |
+----------------+----------------+---------------+
| 192.168.0.1    | Router         | 200           |
| 192.168.0.100  | MyComputer     | N/A           |
| 192.168.0.101  | MyPhone        | 200           |
| 192.168.0.102  | Printer        | N/A           |
| 192.168.0.103  | N/A            | N/A           |
+----------------+----------------+---------------+
Note:
The table content and the actual response codes will vary based on the devices connected to your local network.

Feel free to use and modify this script to suit your needs. It can be a useful tool for network diagnostics and monitoring the devices connected to your home network.
