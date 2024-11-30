# import requests
# import time

# unique_id = 'sid0001'
# username = 'gowe'
# password = '06AugDec1996!@'
# search_query = '''search index="jenkins" event_tag="build_summary" sourcetype="json:jenkins" 
# host="jenkins.service.ntd.ciscolabs.com" job_name="USM/*" metadata.branchName IN ("IMS_7_8_MAIN")
# | fillnull value="-" metadata.branchName
# | search metadata.branchName IN ("IMS_7_8_MAIN")
# | stats count as total_builds'''

# post_data = {
#     'id': unique_id,
#     'max_count': '200',
#     'search': search_query,
#     'earliest_time': '-24h',
#     'latest_time': 'now'
# }

# splunk_search_base_url = 'https://bgl-vms-vm1221:8089/servicesNS/{}/search/search/jobs'.format(username)
# resp = requests.post(splunk_search_base_url, data=post_data, verify=False, auth=(username, password))
# print(resp.text)

# is_job_completed = ""

# while is_job_completed != 'DONE':
#     time.sleep(5)
#     get_data = {'output_mode': 'json'}
#     job_status_base_url = 'https://bgl-vms-vm1221:8089/servicesNS/{}/search/search/jobs/{}'.format(username, unique_id)
#     resp_job_status = requests.post(job_status_base_url, data=get_data, verify=False, auth=(username, password))
#     resp_job_status_data = resp_job_status.json()
#     is_job_completed = resp_job_status_data['entry'][0]['content']['dispatchState']
#     print("Current Job Status is {}".format(is_job_completed))

# splunk_summary_base_url = 'https://bgl-vms-vm1221:8089/servicesNS/{}/search/search/jobs/{}/results'.format(username, unique_id)
# splunk_summary_results = requests.get(splunk_summary_base_url, params=get_data, verify=False, auth=(username, password))
# splunk_summary_data = splunk_summary_results.json()

# for data in splunk_summary_data['results']:
#     print(data)



import requests
import time

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

unique_id = 'sid0001'
username = 'gowe'
password = '06AugDec1996!@'
query_file_path = '/Users/gowe/Desktop/MyWork/SplunkDataNotification/splunk_query.txt'  # Path to the file containing all queries

# Specify the query to load
query_name = 'Table_format'
search_query = load_query(query_file_path, query_name)

if not search_query:
    raise ValueError(f"Query '{query_name}' not found in {query_file_path}")

post_data = {
    'id': unique_id,
    'max_count': '200',
    'search': search_query,
    'earliest_time': '-24h',
    'latest_time': 'now'
}

splunk_search_base_url = f'https://bgl-vms-vm1221:8089/servicesNS/{username}/search/search/jobs'
resp = requests.post(splunk_search_base_url, data=post_data, verify=False, auth=(username, password))
# print(resp.text)

is_job_completed = ""

while is_job_completed != 'DONE':
    time.sleep(5)
    get_data = {'output_mode': 'json'}
    job_status_base_url = f'https://bgl-vms-vm1221:8089/servicesNS/{username}/search/search/jobs/{unique_id}'
    resp_job_status = requests.post(job_status_base_url, data=get_data, verify=False, auth=(username, password))
    resp_job_status_data = resp_job_status.json()
    is_job_completed = resp_job_status_data.get('entry', [{}])[0].get('content', {}).get('dispatchState', "")
    # print("Current Job Status is {}".format(is_job_completed))

splunk_summary_base_url = f'https://bgl-vms-vm1221:8089/servicesNS/{username}/search/search/jobs/{unique_id}/results'
splunk_summary_results = requests.get(splunk_summary_base_url, params=get_data, verify=False, auth=(username, password))
splunk_summary_data = splunk_summary_results.json()

for data in splunk_summary_data.get('results', []):
    print(data)
