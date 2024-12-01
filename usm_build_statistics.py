import requests
import time
from timeframepayload import get_timeframe_payload
import commondata
from tabulate import tabulate
import warnings
import argparse

# Suppress warnings for insecure HTTPS requests
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# Setup argument parsing
parser = argparse.ArgumentParser(description='Run the Splunk query and process results.')
parser.add_argument('query_name', type=str, help='The name of the query to run')
args = parser.parse_args()

# File paths
query_file_path = '/Users/gowe/Desktop/MyWork/SplunkDataNotification/usm_splunk_query_precommit.txt'
branches_file_path = '/Users/gowe/Desktop/MyWork/SplunkDataNotification/branches.txt'

def load_query(file_path, query_name):
    """Load a specific query from a file."""
    with open(file_path, 'r') as file:
        queries = file.read().splitlines()
    
    query_found = False
    query_content = []
    
    for line in queries:
        if line.strip() == f"[{query_name}]":
            query_found = True
        elif query_found:
            if line.startswith("[") and line.endswith("]"):
                break
            query_content.append(line.strip())
    
    return "\n".join(query_content) if query_content else None

def load_branches(file_path):
    """Load branch names from a file and format them for the Splunk query."""
    with open(file_path, 'r') as file:
        branches = file.read().splitlines()
    return ", ".join(f'"{branch.strip()}"' for branch in branches if branch.strip())

# Load the query and branch names
search_query_template = load_query(query_file_path, args.query_name)
branch_names = load_branches(branches_file_path)

if not search_query_template:
    raise ValueError(f"Query '{args.query_name}' not found in {query_file_path}")
if not branch_names:
    raise ValueError(f"No branch names found in {branches_file_path}")

# Inject branch names into the query
search_query = search_query_template.replace("$BRANCH_NAMES", branch_names)

# Splunk query parameters
unique_id = 'sid0001'

# Prepare the payload
post_data = get_timeframe_payload(unique_id, search_query)

# Send Splunk search request
splunk_search_base_url = f'{commondata.SPLUNK_BASE_URL}/servicesNS/{commondata.USERNAME}/search/search/jobs'
resp = requests.post(splunk_search_base_url, data=post_data, verify=False, auth=(commondata.USERNAME, commondata.PASSWORD))

# Monitor job status
is_job_completed = ""
while is_job_completed != 'DONE':
    time.sleep(5)
    get_data = {'output_mode': 'json'}
    job_status_base_url = f'{commondata.SPLUNK_BASE_URL}/servicesNS/{commondata.USERNAME}/search/search/jobs/{unique_id}'
    resp_job_status = requests.post(job_status_base_url, data=get_data, verify=False, auth=(commondata.USERNAME, commondata.PASSWORD))
    resp_job_status_data = resp_job_status.json()
    is_job_completed = resp_job_status_data.get('entry', [{}])[0].get('content', {}).get('dispatchState', "")

# Fetch results without extra XML
splunk_summary_base_url = f'{commondata.SPLUNK_BASE_URL}/servicesNS/{commondata.USERNAME}/search/search/jobs/{unique_id}/results'
splunk_summary_results = requests.get(splunk_summary_base_url, params=get_data, verify=False, auth=(commondata.USERNAME, commondata.PASSWORD))
splunk_summary_data = splunk_summary_results.json()

# Store the table in a variable
headers = ['Branch', 'Total Builds', 'Successful Builds', 'Failed Builds', 'Aborted Builds', 'Unstable Builds', 'Aborted %', 'Failed or Unstable%', 'Average Build Duration']
table_data = []

for data in splunk_summary_data.get('results', []):
    row = [
        data.get('Branch'),
        data.get('Total Builds'),
        data.get('Successful Builds'),
        data.get('Failed Builds'),
        data.get('Aborted Builds'),
        data.get('Unstable Builds'),
        data.get('Aborted %'),
        data.get('Failed or Unstable%'),
        data.get('Average Build Duration')
    ]
    table_data.append(row)

# Store the formatted table in a variable
table_output = tabulate(table_data, headers=headers, tablefmt="pretty")

# You can now use table_output variable wherever you need the table
print(table_output)
