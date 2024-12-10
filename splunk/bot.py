from send import EchoBot

# Your bot details
teams_bot_token = "NTg0ZTFlOWQtNzUwZi00NDVhLWI4MWYtYjlkM2RjYmFiZWRiOWMyMjI5NDktZTQ0_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
bot_person_id = "Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OLzFkMjAwOGY4LTdhYmYtNGIwYi1iNGZmLTQxNWRiYTU3ZWU2Yw"
room_id = "Y2lzY29zcGFyazovL3VzL1JPT00vZjk4NDI5NDAtMTdmMS0xMWVmLTliNTQtNGI1MDc3MjIzZDlh"

# Initialize and run the bot
bot = EchoBot(teams_bot_token=teams_bot_token, bot_person_id=bot_person_id, room_id=room_id)
bot.run()
