
from webex_bot.webex_bot import WebexBot
import subprocess
import re

class EchoBot(WebexBot):
    def __init__(self, teams_bot_token, bot_person_id, room_id):
        super().__init__(teams_bot_token)
        self.teams_bot_token = teams_bot_token
        self.bot_person_id = bot_person_id
        self.room_id = room_id

    def process_incoming_message(self, teams_message, activity):
        # Capture the incoming message
        user_message = teams_message.text.strip()
        sender_id = activity.get("personId")  # ID of the message sender
        
        text = remove_data_digger(user_message)
        print(f"Received: {text}")
        
        # Ignore bot's own messages
        if sender_id == self.bot_person_id:
            print("Ignoring bot's own message")
            return

        # Extract variables
        variables = extract_variables(text)
        print(f"Extracted Variables: {variables}")
        
        # Validate required variables
        query_name = variables.get("initial", "")
        earliest_time = variables.get("from", "")
        latest_time = variables.get("to", "")
        branch_names = variables.get("branch", "")
        
        if not (query_name and earliest_time and latest_time and branch_names):
            print("Error: Missing required parameters!")
            return
        
        # Build the command with quotes around values as needed
        # Build the command with quotes around values as needed
        command = f'python3 test.py --query_names "{query_name}" --earliest_time="{earliest_time}" --latest_time="{latest_time}" --branch_names "{branch_names}"'

        # Print the command for debugging
        print(f"Command to execute: {command}")

        
        # Run the external script
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True, shell=True)
            print("Command executed successfully. Output:")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error executing the command:\n{e.stderr}")
        except Exception as e:
            print(f"Unexpected error: {e}")

def remove_data_digger(text):
    # Replace "DataDigger" with an empty string and return the result
    return text.replace("DataDigger", "")

def extract_variables(text):
    result = {}

    # Pattern for 'initial' (the first value that contains underscores)
    # This pattern will match a string with underscores in it (e.g., USM_Prd_Stage_Statistics_Builds)
    initial_pattern = r"\b[A-Za-z0-9_]+(?:_[A-Za-z0-9_]+)+\b"
    initial_match = re.search(initial_pattern, text)
    if initial_match:
        result["initial"] = initial_match.group(0)

    # Pattern for 'from' (e.g., from -48h)
    from_pattern = r"\bfrom\s+([^\s]+)"
    from_match = re.search(from_pattern, text)
    if from_match:
        result["from"] = from_match.group(1)

    # Pattern for 'to' (e.g., to now)
    to_pattern = r"\bto\s+([^\s]+)"
    to_match = re.search(to_pattern, text)
    if to_match:
        result["to"] = to_match.group(1)

    # Pattern for 'branch' (e.g., branch ims_7_8_main)
    branch_pattern = r"\bbranch\s+([^\s]+)"
    branch_match = re.search(branch_pattern, text)
    if branch_match:
        result["branch"] = branch_match.group(1)

    return result