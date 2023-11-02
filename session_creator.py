import telethon
from telethon import TelegramClient, events, sync

import os
import dotenv

dotenv.load_dotenv()

# Get API ID and API HASH from .env file
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

# Log in to Telegram and create a session file
# handle 2fa, wrong code, etc.

def create_session(phone_number, api_id, api_hash):
    client = TelegramClient(f"session/{phone_number}", api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone_number)
        client.sign_in(phone_number, input('Enter the code: '))
    client.disconnect()

if __name__ == "__main__":
    create_session(input("Enter phone number: "), api_id, api_hash)
