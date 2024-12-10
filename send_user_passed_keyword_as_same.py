from webex_bot.webex_bot import WebexBot
import requests

class EchoBot(WebexBot):
    def __init__(self, teams_bot_token, bot_person_id, room_id):
        # Initialize the parent WebexBot class
        super().__init__(teams_bot_token)
        
        # Explicitly set the token on the current class instance
        self.teams_bot_token = teams_bot_token  # Add this line to ensure token is set properly
        
        self.bot_person_id = bot_person_id  # Set bot_person_id as required
        self.room_id = room_id  # Set the room_id to send messages
        self.teams_api_url = "https://webexapis.com/v1/messages"

    def process_incoming_message(self, teams_message, activity):
        # teams_message is the expected argument passed to this method
        user_message = teams_message.text.strip()  # Capture the incoming message
        print(f"Received: {user_message}")

        # Don't let the bot reply to its own messages
        if activity.get('personId') == self.bot_person_id:
            return

        # Send the message to the specified room_id using Webex Teams API
        if self.room_id:
            self.send_message(self.room_id, user_message)  # Send the same message back to the specified room
        else:
            print("No roomId specified")

    def send_message(self, room_id, message):
        headers = {
            "Authorization": f"Bearer {self.teams_bot_token}",  # Use the bot's access token here
            "Content-Type": "application/json"
        }
        data = {
            "roomId": room_id,
            "text": message
        }
        response = requests.post(self.teams_api_url, headers=headers, json=data)
        
        if response.status_code == 200:
            print(f"Message sent successfully to room {room_id}")
        else:
            print(f"Failed to send message: {response.status_code}, {response.text}")

# Define the bot token, person ID, and room ID
teams_bot_token = "NTg0ZTFlOWQtNzUwZi00NDVhLWI4MWYtYjlkM2RjYmFiZWRiOWMyMjI5NDktZTQ0_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
bot_person_id = "Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OLzFkMjAwOGY4LTdhYmYtNGIwYi1iNGZmLTQxNWRiYTU3ZWU2Yw"
ROOM_ID = "Y2lzY29zcGFyazovL3VzL1JPT00vZjk4NDI5NDAtMTdmMS0xMWVmLTliNTQtNGI1MDc3MjIzZDlh"  # Your room ID

# Initialize the bot with the required parameters
bot = EchoBot(teams_bot_token=teams_bot_token, bot_person_id=bot_person_id, room_id=ROOM_ID)

# Run the bot
bot.run()
