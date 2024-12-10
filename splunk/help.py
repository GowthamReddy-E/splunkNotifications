import argparse
import requests

# Webex API details
ACCESS_TOKEN = "NTg0ZTFlOWQtNzUwZi00NDVhLWI4MWYtYjlkM2RjYmFiZWRiOWMyMjI5NDktZTQ0_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
ROOM_ID = "Y2lzY29zcGFyazovL3VzL1JPT00vZjk4NDI5NDAtMTdmMS0xMWVmLTliNTQtNGI1MDc3MjIzZDlh"

def send_message_to_webex(message):
    """Send the content as a message to the Webex room."""
    url = "https://api.ciscospark.com/v1/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Send the message to Webex room
    response = requests.post(url, headers=headers, json={
        "roomId": ROOM_ID,
        "text": message
    })

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.text}")

def read_file(file_path):
    """Read the content of a file."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Send text file content to Webex room.")
    parser.add_argument("file_path", help="Path to the text file")

    args = parser.parse_args()

    # Read the file content
    file_content = read_file(args.file_path)
    
    if file_content:
        # Send the content to Webex
        send_message_to_webex(file_content)
    else:
        print("No content to send.")

# python3 -u send_txt_to_webex.py /Users/gowe/Desktop/MyWork/SplunkDataNotification/splunk/help.txt