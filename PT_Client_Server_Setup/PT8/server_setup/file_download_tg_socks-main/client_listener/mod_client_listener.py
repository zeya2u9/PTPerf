from telethon import TelegramClient, events
import logging
import time
import aiofiles
import asyncio
import socket

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',level=logging.WARNING)

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 9013

csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket.setdefaulttimeout(3600)

csock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
csock.listen()
conn, addr = csock.accept()

client = TelegramClient('~/file_download_tg_socks-main/client_listener/client_listener', <API-ID1>, '<API-HASH1>') #for username1

'''async with aiofiles.open('alexa_1000.txt', mode='r') as f:
    async for website in f:
        await client.send_message('n1nj4tor', website)
        time.sleep(20)'''
#weblist=[]
#ts=0.0
total_msgs = 0
@client.on(events.NewMessage(incoming=True))
async def my_event_handler(event):
    global total_msgs
    global conn
    global addr
    global csock

    msg = event.raw_text
    total_msgs = total_msgs + 1
    #web = event.raw_text.split()
    #ts = web[-1]
    #print(ts)
    #if('ts' in locals()):
    #print('Time to download ' + msg + ' is :' + str(time.time()-float(ts)))
    #print("Received Text :" + msg)
    print("Received Text!! ", total_msgs, time.asctime(time.localtime())[11:20])
    msg = msg.encode('ascii')
    #clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conn.send(msg)

    #reconnecting with client_int if total_msgs is a multiple of 27
    if total_msgs > 1:
        if total_msgs%20==0: #single check for >1 and %27 was not working somehow -_-
            csock.listen()
            conn, addr = csock.accept()        
            print('It looks like multiple of 27. Time to wake-up listener2')
            #sending msg to Camoplus02 to reconnect to int_client
            await client.send_message('<username2>', "WP")

    #else:
    #    print('Ignored Timestamp ' + str(time.time()))
    #sender = await event.get_sender()
    #print(sender)
    #print(event)

client.start()
client.run_until_disconnected()
