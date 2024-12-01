# import requests
# import time
# import warnings
# from tabulate import tabulate

# # Suppress warnings for insecure HTTPS requests
# warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# def load_query(file_path, query_name):
#     """Load a specific query from a file."""
#     with open(file_path, 'r') as file:
#         queries = file.read().splitlines()
    
#     query_found = False
#     query_content = []
    
#     for line in queries:
#         if line.strip() == f"[{query_name}]":
#             query_found = True
#         elif query_found:
#             if line.startswith("[") and line.endswith("]"):
#                 break  # Stop if another query starts
#             query_content.append(line.strip())
    
#     return "\n".join(query_content) if query_content else None

# def load_branches(file_path):
#     """Load branch names from a file and format them for the Splunk query."""
#     with open(file_path, 'r') as file:
#         branches = file.read().splitlines()
#     # Format branch names as Splunk-compatible IN ("branch1", "branch2", ...)
#     return ", ".join(f'"{branch.strip()}"' for branch in branches if branch.strip())

# # File paths
# query_file_path = '/Users/gowe/Desktop/MyWork/SplunkDataNotification/usm_splunk_query_precommit.txt'
# branches_file_path = '/Users/gowe/Desktop/MyWork/SplunkDataNotification/branches.txt'

# # Load branch names
# branch_names = load_branches(branches_file_path)
# if not branch_names:
#     raise ValueError(f"No branch names found in {branches_file_path}")

# # Splunk authentication details
# username = 'gowe'
# password = '06AugDec1996!@'

# # List of queries to execute
# # query_names = ['USM_Pre_Total_Builds', 'USM_Pre_Successful_Builds', 'USM_Pre_Failed_Builds', 'USM_Pre_Unstable_Builds', 'USM_Pre_Aborted_Builds']
# query_names = ['USM_Pre_Build_stats_Table_format']

# # Loop through each query
# for query_name in query_names:
#     search_query_template = load_query(query_file_path, query_name)
#     if not search_query_template:
#         print(f"Query '{query_name}' not found in {query_file_path}")
#         continue
    
#     # Inject branch names into the query
#     search_query = search_query_template.replace("$BRANCH_NAMES", branch_names)
    
#     # Splunk query parameters
#     unique_id = f'sid_{query_name}'
#     post_data = {
#         'id': unique_id,
#         'max_count': '200',
#         'search': search_query,
#         'earliest_time': '-240h',
#         'latest_time': 'now'
#     }
    
#     # Send Splunk search request
#     splunk_search_base_url = f'https://bgl-vms-vm1221:8089/servicesNS/{username}/search/search/jobs'
#     resp = requests.post(splunk_search_base_url, data=post_data, verify=False, auth=(username, password))
    
#     # Check for job creation success
#     if resp.status_code != 201:
#         print(f"Failed to create job for query '{query_name}': {resp.text}")
#         continue
    
#     # Monitor job status
#     is_job_completed = ""
#     while is_job_completed != 'DONE':
#         time.sleep(5)
#         get_data = {'output_mode': 'json'}
#         job_status_base_url = f'https://bgl-vms-vm1221:8089/servicesNS/{username}/search/search/jobs/{unique_id}'
#         resp_job_status = requests.post(job_status_base_url, data=get_data, verify=False, auth=(username, password))
#         resp_job_status_data = resp_job_status.json()
#         is_job_completed = resp_job_status_data.get('entry', [{}])[0].get('content', {}).get('dispatchState', "")
#         print(f"Query '{query_name}': Current Job Status is {is_job_completed}")
    
#     # Fetch and display results
#     splunk_summary_base_url = f'https://bgl-vms-vm1221:8089/servicesNS/{username}/search/search/jobs/{unique_id}/results'
#     splunk_summary_results = requests.get(splunk_summary_base_url, params=get_data, verify=False, auth=(username, password))
#     splunk_summary_data = splunk_summary_results.json()
    
#     print(f"Results for query '{query_name}':")
#     for data in splunk_summary_data.get('results', []):
#         print(data)


import requests
import time
import warnings
from tabulate import tabulate

# Suppress warnings for insecure HTTPS requests
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

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
                break  # Stop if another query starts
            query_content.append(line.strip())
    
    return "\n".join(query_content) if query_content else None

def load_branches(file_path):
    """Load branch names from a file and format them for the Splunk query."""
    with open(file_path, 'r') as file:
        branches = file.read().splitlines()
    # Format branch names as Splunk-compatible IN ("branch1", "branch2", ...)
    return ", ".join(f'"{branch.strip()}"' for branch in branches if branch.strip())

# File paths
query_file_path = '/Users/gowe/Desktop/MyWork/SplunkDataNotification/usm_splunk_query_precommit.txt'
branches_file_path = '/Users/gowe/Desktop/MyWork/SplunkDataNotification/branches.txt'

# Load branch names
branch_names = load_branches(branches_file_path)
if not branch_names:
    raise ValueError(f"No branch names found in {branches_file_path}")

# Splunk authentication details
username = 'gowe'
password = '06AugDec1996!@'

# List of queries to execute
query_names = ['USM_Pre_Stage_Information']

# Loop through each query
for query_name in query_names:
    search_query_template = load_query(query_file_path, query_name)
    if not search_query_template:
        print(f"Query '{query_name}' not found in {query_file_path}")
        continue
    
    # Inject branch names into the query
    search_query = search_query_template.replace("$BRANCH_NAMES", branch_names)
    
    # Splunk query parameters
    unique_id = f'sid_{query_name}'
    post_data = {
        'id': unique_id,
        'max_count': '200',
        'search': search_query,
        'earliest_time': '-240h',
        'latest_time': 'now'
    }
    
    # Send Splunk search request
    splunk_search_base_url = f'https://bgl-vms-vm1221:8089/servicesNS/{username}/search/search/jobs'
    resp = requests.post(splunk_search_base_url, data=post_data, verify=False, auth=(username, password))
    
    # Check for job creation success
    if resp.status_code != 201:
        print(f"Failed to create job for query '{query_name}': {resp.text}")
        continue
    
    # Monitor job status
    is_job_completed = ""
    while is_job_completed != 'DONE':
        time.sleep(5)
        get_data = {'output_mode': 'json'}
        job_status_base_url = f'https://bgl-vms-vm1221:8089/servicesNS/{username}/search/search/jobs/{unique_id}'
        resp_job_status = requests.post(job_status_base_url, data=get_data, verify=False, auth=(username, password))
        resp_job_status_data = resp_job_status.json()
        is_job_completed = resp_job_status_data.get('entry', [{}])[0].get('content', {}).get('dispatchState', "")
        print(f"Query '{query_name}': Current Job Status is {is_job_completed}")
    
    # Fetch and display results
    splunk_summary_base_url = f'https://bgl-vms-vm1221:8089/servicesNS/{username}/search/search/jobs/{unique_id}/results'
    splunk_summary_results = requests.get(splunk_summary_base_url, params=get_data, verify=False, auth=(username, password))
    splunk_summary_data = splunk_summary_results.json()
    
    # Extract data into a table-friendly format
    results = splunk_summary_data.get('results', [])
    if results:
        headers = results[0].keys()  # Use keys of the first result as headers
        rows = [list(result.values()) for result in results]
        print(f"\nResults for query '{query_name}':\n")
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        print(f"No results for query '{query_name}'")
