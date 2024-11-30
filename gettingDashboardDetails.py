import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

# Define Splunk connection details
SPLUNK_URL = 'https://bgl-vms-vm1221:8089'  # Your Splunk REST API URL (with port 8089)
SPLUNK_USER = 'gowe'  # Your Splunk username
SPLUNK_PASS = '06AugDec1996!@'  # Your Splunk password
API_ENDPOINT = '/servicesNS/admin/search/data/ui/views'  # Endpoint to get dashboard details

# Send GET request to the API to fetch dashboards metadata
response = requests.get(
    SPLUNK_URL + API_ENDPOINT,
    auth=HTTPBasicAuth(SPLUNK_USER, SPLUNK_PASS),
    verify=False  # Set to True if you want to verify SSL certificates
)

# Check if the request was successful
if response.status_code == 200:
    print("Response received successfully!")

    # Print the first 1000 characters of the raw XML response for inspection
    print("Raw Response:")
    print(response.text[:1000])  # Print the first 1000 characters for inspection

    try:
        # Parse the raw XML response
        root = ET.fromstring(response.text)

        # Check the totalResults to understand how many dashboards there are
        total_results = root.find('.//{http://a9.com/-/spec/opensearch/1.1/}totalResults')
        if total_results is not None:
            print("Total Results:", total_results.text)
        
        # Find all dashboard entries in the XML response
        dashboards = root.findall('.//{http://www.w3.org/2005/Atom}entry')
        print("Total number of dashboards:", len(dashboards))

        # Iterate through the dashboards and print out dashboard titles
        for dashboard in dashboards:
            title = dashboard.find('.//{http://www.w3.org/2005/Atom}title')  # Find the title of each dashboard
            if title is not None:
                print("Dashboard title:", title.text)
            else:
                print("No title found for a dashboard.")

    except Exception as e:
        print(f"Error parsing XML: {e}")
else:
    print("Failed to fetch dashboards. Status code:", response.status_code)
    print("Response:", response.text)
