import json
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events, utils

# Read secrets from telegram_secrets.json
with open('telegram_secrets.json') as f:
  cookies = json.load(f)
api_id = cookies['api_id']
api_hash = cookies['api_hash']
token = cookies['token']

phone_number = cookies['phone_number'] # phone number to receive otp
receivers = cookies['receivers']

def send_message(message):
    # Create a telegram session and assign it to a variable client
    client = TelegramClient('session', api_id, api_hash)
    client.connect()

    # In case of script ran first time it will ask either to input token or otp sent to number or sent or your telegram id
    if not client.is_user_authorized():
        client.send_code_request(phone_number)
        # Signing in the client
        client.sign_in(phone_number, input('Enter the code: '))

    try:
        for receiver in receivers:
            # Set receiver user_id and access_hash
            # To get userid and access hash: client.get_input_entity('@username')
            receiverUser = InputPeerUser(receiver['user_id'], receiver['access_hash'])

            # Send message using telegram client
            client.send_message(receiverUser, message)
    except Exception as e:
        # there may be many error coming in while like peer error, wwrong access_hash, flood_error, etc
        print(e)

    # Disconnecting the telegram session
    client.disconnect()
