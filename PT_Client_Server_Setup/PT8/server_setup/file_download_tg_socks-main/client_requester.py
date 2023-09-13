from telethon import TelegramClient
import time
import aiofiles
import asyncio
import sys

# Remember to use your own values from my.telegram.org!
#api_id = 1182520
#api_hash = 'cf9d9db47f3c77dc922d59fc8e9a9050'
#client = TelegramClient('client_requester', api_id, api_hash)
api_id = 15994260
api_hash = '5c648eb445ab137289cbb4d03c0ea072'
client = TelegramClient('/root/pTesting/file_download_tg_socks-main/client_requester', api_id, api_hash)
#client = TelegramClient('client_requester', api_id, api_hash, flood_sleep_threshold=1500)

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

    #await client.send_message('CamoZeya', str(sys.argv[1] + ' ' + str(time.time())))
    #time.sleep(2)
    #await asyncio.sleep(0.5)
    print('Time: ',time.asctime(time.localtime())[11:20])
    await client.send_message('CamoZeya', str(sys.argv[1]))

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
