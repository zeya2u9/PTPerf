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

api_id = 8254518
api_hash = '7365761666f8a08b4468fa5415fd7fc3'
client = TelegramClient('proxy_data_sender', api_id, api_hash)

#adding flood_sleep_threshold 
#client = TelegramClient('proxy_data_sender', api_id, api_hash, flood_sleep_threshold=1000)


async def main():
    # Getting information about yourself
    ##me = await client.get_me()

    # "me" is an User object. You can pretty-print
    # any Telegram object with the "stringify" method:
    ##print(me.stringify())

    # When you print something, you see a representation of it.
    # You can access all attributes of Telegram objects with
    # the dot operator. For example, to get the username:
    ##username = me.username
    ##print(username)
    ##print(me.phone)
    '''async with aiofiles.open('alexa_100.txt', mode='r') as f:
        async for website in f:
            print(website)
    #f = open('./alexa_1000.txt','r')
    #for website in f:
            #await client.send_message('me', website)
            await client.send_message('n1nj4tor', website + ' ' + str(time.time()))
            time.sleep(7)'''
    #await asyncio.sleep(1)
    #print('Time: ',time.asctime(time.localtime())[11:20])
    print('len(msg): ',len(str(sys.argv[1])))
    try:
        await client.send_message('Camoplus01', str(sys.argv[1]))
    except errors.FloodWaitError as e:
        print('Have to sleep - C2', e.seconds, 'seconds')
        await asyncio.sleep(e.seconds)
        #await client.send_message('Camoplus01', str(sys.argv[1]))
        os.system("python3 proxy_data_sender2.py " + sys.argv[1]) #added new j13-22

    '''# You can print all the dialogs/conversations that you are part of:
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)

    # You can send messages to yourself...
    await client.send_message('me', 'Hello, myself!')
    # ...to some chat ID
    await client.send_message(-100123456, 'Hello, group!')
    # ...to your contacts
    await client.send_message('+34600123123', 'Hello, friend!')
    # ...or even to any username
    await client.send_message('TelethonChat', 'Hello, Telethon!')

    # You can, of course, use markdown in your messages:
    message = await client.send_message(
        'me',
        'This message has **bold**, `code`, __italics__ and '
        'a [nice website](https://example.com)!',
        link_preview=False
    )

    # Sending a message returns the sent message object, which you can use
    print(message.raw_text)

    # You can reply to messages directly if you have a message object
    await message.reply('Cool!')

    # Or send files, songs, documents, albums...
    await client.send_file('me', '/home/me/Pictures/holidays.jpg')

    # You can print the message history of any chat:
    async for message in client.iter_messages('me'):
        print(message.id, message.text)

        # You can download media from messages, too!
        # The method will return the path where the file was saved.
        if message.photo:
            path = await message.download_media()
            print('File saved to', path)  # printed after download is done
'''
with client:
    client.loop.run_until_complete(main())
