from telethon import TelegramClient, errors
import time
import aiofiles
import asyncio
import sys
import os

# Remember to use your own values from my.telegram.org!
'''api_id = 1247726
api_hash = '6b2355ef124a58b86f7a5719dc6f8be1'
client = TelegramClient('proxy_data_sender', api_id, api_hash)'''

api_id = 8389047
api_hash = 'f4768916a66c6d2203c834431fed3091'
#client = TelegramClient('proxy_data_sender', api_id, api_hash)

#adding flood_sleep_threshold 
client = TelegramClient('proxy_data_sender2', api_id, api_hash)

async def main():
    print('len(msg): ',len(str(sys.argv[1])))
    try:
        await client.send_message('Camoplus02', str(sys.argv[1]))
    except errors.FloodWaitError as e:
        print('Have to sleep - C3', e.seconds, 'seconds')
        await asyncio.sleep(e.seconds)
        await client.send_message('Camoplus02', str(sys.argv[1]))

with client:
    client.loop.run_until_complete(main())
