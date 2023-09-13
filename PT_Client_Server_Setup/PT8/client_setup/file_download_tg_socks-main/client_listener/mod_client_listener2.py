from telethon import TelegramClient, events
import logging
import time
import aiofiles
import asyncio
import socket
import os

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',level=logging.WARNING)

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 9016

csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket.setdefaulttimeout(3600)

csock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
csock.listen()
conn, addr = csock.accept()

client = TelegramClient('~/file_download_tg_socks-main/client_listener/client_listener2', <API-ID2>, '<API-HASH2>') #username2

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
    global csock
    global addr

    msg = event.raw_text
    sender = await event.get_sender()
    
    if sender.username == "<username1>":
        print('Interrupt via Msg::',sender.username, msg)
        csock.listen()
        conn, addr = csock.accept()
    else:
        file_name = "/root/pTesting/file_download_tg_socks-main/index_d.txt"

        #truncate file if already some data
        #async with aiofiles.open(file_name, mode='w') as f:
        #    await f.truncate()
        #    await f.close()

        await event.download_media(file_name)

        total_msgs = total_msgs + 1
        print("Received file!! ", total_msgs, time.asctime(time.localtime())[11:20])
        
        async with aiofiles.open(file_name, mode='r') as f:
            msg = await f.read()
            print(f"[!] Bytes received from Telegram: {len(msg)}")
            msg = msg.encode('ascii')+b'|'
            print('Msg after encoding:: ',len(msg))
            try:
                conn.send(msg)  ##added line 23apr
                os.system('truncate -s 0 '+file_name)
                f.close()
            except Exception as e:
                print(e)
                exit(1)
            
        # msg = msg.encode('ascii')
        # #clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # l = len(msg)
        # i = 1
        # lim = 0
        # while lim<l:
        #     msg_d = msg[lim:lim+400]
        #     lim = 400 * i 
        #     # msg_d = msg[lim:lim+2048]
        #     # lim = 2048 * i
        #     i = i + 1
            
        #     conn.send(msg_d)            
        
        #os.system('truncate -s 0 '+file_name)


    #else:
    #    print('Ignored Timestamp ' + str(time.time()))
    #sender = await event.get_sender()
    #print(sender)
    #print(event)

client.start()
client.run_until_disconnected()
