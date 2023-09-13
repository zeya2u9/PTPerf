from telethon import TelegramClient, errors
import time
import aiofiles
import asyncio
import sys
import os

# Remember to use your own values from my.telegram.org!

api_id = <API-ID3>
api_hash = '<API-HASH3>'
client = TelegramClient('proxy_data_sender', api_id, api_hash)

async def main():
    print('len(msg): ',len(str(sys.argv[1])), 'file_name: ', str(sys.argv[1]))
    try:       
        await client.send_file('<username2>', str(sys.argv[1]))
    except errors.FloodWaitError as e:
        print('Have to sleep - C4', e.seconds, 'seconds')
        await asyncio.sleep(e.seconds)
        await client.send_file('<username2>', str(sys.argv[1]))

with client:
    client.loop.run_until_complete(main())
