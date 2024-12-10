import argparse
import requests
import time
import warnings
from tabulate import tabulate

# Suppress warnings for insecure HTTPS requests
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# Query files mapping
QUERY_FILES = {
    "precommit": "/Users/gowe/Desktop/MyWork/SplunkDataNotification/usm_splunk_query_precommit_dynamic_values.txt",
    "production": "/Users/gowe/Desktop/MyWork/SplunkDataNotification/usm_splunk_query_production_dynamic_values.txt"
}
BRANCHES_FILE = "/Users/gowe/Desktop/MyWork/SplunkDataNotification/USM_IMS_Branches.txt"
SPLUNK_USERNAME = "gowe"
SPLUNK_PASSWORD = "06AugDec1996!@"
ACCESS_TOKEN = "NTg0ZTFlOWQtNzUwZi00NDVhLWI4MWYtYjlkM2RjYmFiZWRiOWMyMjI5NDktZTQ0_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
ROOM_ID = "Y2lzY29zcGFyazovL3VzL1JPT00vZjk4NDI5NDAtMTdmMS0xMWVmLTliNTQtNGI1MDc3MjIzZDlh"

def load_query(query_name):
    """Load a specific query from the appropriate file."""
    for query_type, file_path in QUERY_FILES.items():
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
        
        if query_content:
            print(f"Query '{query_name}' found in {query_type} file.")
            return "\n".join(query_content)
    
    return None

def load_branches(file_path):
    """Load branch names from a file and format them for the Splunk query."""
    with open(file_path, 'r') as file:
        branches = file.read().splitlines()
    # Format branch names as Splunk-compatible IN ("branch1", "branch2", ...)
    return ", ".join(f'"{branch.strip()}"' for branch in branches if branch.strip())

def send_message_to_bot(header, message):
    """Send a formatted message to the bot."""
    url = "https://api.ciscospark.com/v1/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    # Send the header first (e.g., query title)
    response = requests.post(url, headers=headers, json={"roomId": ROOM_ID, "markdown": header})
    if response.status_code != 200:
        print(f"Failed to send header: {response.text}")
    # Then send the body in chunks
    chunk_size = 7000  # Limit to Webex's constraints
    body_lines = message.split("\n")
    chunk = "```\n"  # Start markdown block
    for line in body_lines:
        if len(chunk) + len(line) + 1 > chunk_size:
            # Close the table block before sending
            if not chunk.endswith("\n```"):
                chunk += "\n```"
            response = requests.post(url, headers=headers, json={"roomId": ROOM_ID, "markdown": chunk})
            if response.status_code != 200:
                print(f"Failed to send chunk: {response.text}")
            chunk = "```\n"  # Reset for the next chunk
        chunk += line + "\n"
    if chunk.strip():  # Send any remaining content
        if not chunk.endswith("\n```"):
            chunk += "\n```"
        response = requests.post(url, headers=headers, json={"roomId": ROOM_ID, "markdown": chunk})
        if response.status_code != 200:
            print(f"Failed to send final chunk: {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Splunk queries with dynamic arguments")
    parser.add_argument("--query_names", nargs='+', required=True, help="List of query names to execute")
    parser.add_argument("--earliest_time", required=True, help="Earliest time for the query")
    parser.add_argument("--latest_time", required=True, help="Latest time for the query")
    parser.add_argument("--branch_names", nargs='*', help="List of branch names to include in the query")

    args = parser.parse_args()

    # Load branch names
    if args.branch_names:
        # If branch names are passed via command line, use them
        branch_names = ", ".join(f'"{branch.strip()}"' for branch in args.branch_names if branch.strip())
    else:
        # If no branch names are passed, load from the file
        branch_names = load_branches(BRANCHES_FILE)
        if not branch_names:
            raise ValueError(f"No branch names found in {BRANCHES_FILE}")

    # Loop through each query
    for query_name in args.query_names:
        search_query_template = load_query(query_name)
        if not search_query_template:
            header = f"### Splunk Query Results:\n\n**Query '{query_name}' not found in either file**"
            send_message_to_bot(header, "")
            continue
        
        # Inject branch names into the query
        search_query = search_query_template.replace("$BRANCH_NAMES", branch_names)
        
        # Splunk query parameters
        unique_id = f'sid_{query_name}'
        post_data = {
            'id': unique_id,
            'max_count': '200',
            'search': search_query,
            'earliest_time': args.earliest_time,
            'latest_time': args.latest_time
        }
        
        # Send Splunk search request
        splunk_search_base_url = f'https://bgl-vms-vm1221:8089/servicesNS/{SPLUNK_USERNAME}/search/search/jobs'
        resp = requests.post(splunk_search_base_url, data=post_data, verify=False, auth=(SPLUNK_USERNAME, SPLUNK_PASSWORD))
        
        if resp.status_code != 201:
            header = f"### Splunk Query Results:\n\n**Failed to create job for query '{query_name}':** {resp.text}"
            send_message_to_bot(header, "")
            continue
        
        # Monitor job status
        is_job_completed = ""
        while is_job_completed != 'DONE':
            time.sleep(5)
            get_data = {'output_mode': 'json'}
            job_status_base_url = f'https://bgl-vms-vm1221:8089/servicesNS/{SPLUNK_USERNAME}/search/search/jobs/{unique_id}'
            resp_job_status = requests.post(job_status_base_url, data=get_data, verify=False, auth=(SPLUNK_USERNAME, SPLUNK_PASSWORD))
            resp_job_status_data = resp_job_status.json()
            is_job_completed = resp_job_status_data.get('entry', [{}])[0].get('content', {}).get('dispatchState', "")
            print(f"Query '{query_name}': Current Job Status is {is_job_completed}")
        
        # Fetch and display results
        splunk_summary_base_url = f'https://bgl-vms-vm1221:8089/servicesNS/{SPLUNK_USERNAME}/search/search/jobs/{unique_id}/results'
        splunk_summary_results = requests.get(splunk_summary_base_url, params=get_data, verify=False, auth=(SPLUNK_USERNAME, SPLUNK_PASSWORD))
        splunk_summary_data = splunk_summary_results.json()
        
        results = splunk_summary_data.get('results', [])
        if results:
            headers = results[0].keys()  # Use keys of the first result as headers
            rows = [list(result.values()) for result in results]
            header = f"### Splunk Query Results:\n\n**Results for query '{query_name}':**"
            body = tabulate(rows, headers=headers, tablefmt="grid")
            send_message_to_bot(header, body)
        else:
            header = f"### Splunk Query Results:\n\n**Results for query '{query_name}':**"
            body = "No results found"
            send_message_to_bot(header, body)

# python3 send.py --query_names "USM_Production_Stage_Statistics_Builds" --earliest_time="-48h" --latest_time="now" --branch_names "USM/IMS_7_8_MAIN"
# python3 send.py --query_names "USM_Production_Total_Builds" --earliest_time="-48h" --latest_time="now" --branch_names "USM/IMS_7_8_MAIN"
# python3 send.py --query_names "USM_Production_Stage_Statistics_Builds" --earliest_time="-48h" --latest_time="now" --branch_names "USM/IMS_7_8_MAIN" "USM/IMS_7_6_MAIN"
