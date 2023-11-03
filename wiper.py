import os
import dotenv
import telethon
from telethon import TelegramClient, events, sync, functions, errors

dotenv.load_dotenv()

# Get API ID and API HASH from .env file
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

# Go to session folder(there are telethon sessions)
# Log into each session and delete all dms, groups, channels and saved messages.

def wipe_sessions(api_id, api_hash):
    for session in os.listdir("session"):
        # If extension is .session-journal, delete it, continue to next session
        if session.endswith(".session-journal"):
            os.remove(f"session/{session}")
            continue

        print(f"Session: {session}", end=" ")
        client = TelegramClient(f"session/{session}", api_id, api_hash)

        try:
            client.connect()
        except errors.rpcerrorlist.AuthKeyDuplicatedError as e:
            print(f"Session: {session} Error: {e}")
            client.disconnect()
            # Skip to next session
            continue

        try:
            # Delete all dialogs
            for dialog in client.iter_dialogs():
                try:
                    client.delete_dialog(dialog.id, revoke=True)
                except:
                    pass

            # Delete all saved messages
            for message in client.iter_messages("me"):
                try:
                    client.delete_messages("me", message.id)
                except:
                    pass

            # Delete all bots
            for bot in client.iter_dialogs():
                try:
                    if bot.entity.bot:
                        client.delete_dialog(bot.id)
                except:
                    pass

            # Delete all chat folders
            for folder in client(functions.messages.GetDialogFiltersRequest()):
                try:
                    client(functions.messages.UpdateDialogFilterRequest(folder.id))
                except Exception:
                    pass

            # Leave all groups
            for group in client.iter_dialogs():
                try:
                    if group.is_group:
                        client(functions.channels.LeaveChannelRequest(group.id))
                except:
                    pass

        except Exception as e:
            print(f"- Error: {e}")
            client.disconnect()
            continue

        print("- Done")

        client.disconnect()

if __name__ == "__main__":
    wipe_sessions(api_id, api_hash)
