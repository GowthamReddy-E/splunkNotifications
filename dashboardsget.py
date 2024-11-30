import requests
import time

unique_id = 'sid0001'
username = 'gowe'
password = '06AugDec1996!@'
search_query = '''search index="jenkins" event_tag="build_summary" sourcetype="json:jenkins" 
host="jenkins.service.ntd.ciscolabs.com" job_name="USM/*" metadata.branchName IN ("IMS_7_8_MAIN")
| fillnull value="-" metadata.branchName
| search metadata.branchName IN ("IMS_7_8_MAIN")
| stats count as total_builds'''

post_data = {
    'id': unique_id,
    'max_count': '200',
    'search': search_query,
    'earliest_time': '-24h',
    'latest_time': 'now'
}

splunk_search_base_url = 'https://bgl-vms-vm1221:8089/servicesNS/{}/search/search/jobs'.format(username)
resp = requests.post(splunk_search_base_url, data=post_data, verify=False, auth=(username, password))
print(resp.text)

is_job_completed = ""

while is_job_completed != 'DONE':
    time.sleep(5)
    get_data = {'output_mode': 'json'}
    job_status_base_url = 'https://bgl-vms-vm1221:8089/servicesNS/{}/search/search/jobs/{}'.format(username, unique_id)
    resp_job_status = requests.post(job_status_base_url, data=get_data, verify=False, auth=(username, password))
    resp_job_status_data = resp_job_status.json()
    is_job_completed = resp_job_status_data['entry'][0]['content']['dispatchState']
    print("Current Job Status is {}".format(is_job_completed))

splunk_summary_base_url = 'https://bgl-vms-vm1221:8089/servicesNS/{}/search/search/jobs/{}/results'.format(username, unique_id)
splunk_summary_results = requests.get(splunk_summary_base_url, params=get_data, verify=False, auth=(username, password))
splunk_summary_data = splunk_summary_results.json()

for data in splunk_summary_data['results']:
    print(data)
