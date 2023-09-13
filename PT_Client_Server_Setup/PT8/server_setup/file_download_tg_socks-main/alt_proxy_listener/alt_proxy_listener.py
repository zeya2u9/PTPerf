from telethon import TelegramClient, events
import logging
import time
import aiofiles
import asyncio
import os
import base64
import socket

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',level=logging.WARNING)

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 9014

#something like below
client = TelegramClient('proxy', <API-ID3> , '<API-HASH3>')


@client.on(events.NewMessage(incoming=True))
#@client.on(events.NewMessage(incoming=True, pattern=r'abc'))
async def my_event_handler(event):
    sender = await event.get_sender()
    #print(sender.username)
    #print(event.raw_text)

    #Create a UDP socket to listen for replies from intermediary
    int_listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    int_listener.bind((UDP_IP_ADDRESS, 9015))

    text = event.raw_text
    print("New Text (Time)" + time.asctime(time.localtime())[11:20] + ": " + text)
    int_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = bytes(text, 'ascii')
    int_sender.sendto(text, (UDP_IP_ADDRESS, UDP_PORT_NO))
    print('Data sent to server_int.')

    '''#creating TCP socket to listen for replies from intermediary
    int_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #int_listener.bind((UDP_IP_ADDRESS, 9015))

    text = event.raw_text
    print("New Text (Time)" + time.asctime(time.localtime())[11:20] + ": " + text)
    int_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    int_sender.connect((UDP_IP_ADDRESS, UDP_PORT_NO))

    text = bytes(text, 'ascii')
    int_sender.send(text)
    print('Data sent to server_int.')'''



    '''data = int_listener.recv(4096)
    encoded = base64.b64encode(data)
    sendable_string = encoded.decode('ascii')
    print("returned text : " + sendable_string)
    if(len(sendable_string) > 0):
        await client.send_message(sender.username, sendable_string)
    int_listener.close()
    int_sender.close()'''
    #print(text)
    '''__,web,ts = text.split()
    filename = web + '.html'
    curr_ts = time.time()
    p1 = time.time()-float(ts)
    print('Received request for ' + web + ' with timestamp '+ ts)
    #print("Time taken to receive by proxy : " + str(p1))
    os.system('timeout 5 wget -O ' + filename + ' https://' + web)
    if(os.stat(filename).st_size != 0):
        #os.system('mv index.html ' + filename)
        #await client([SendMessageRequest(sender.username, web + ' ' + ts, file = filename)])
        await client.send_message(sender.username, web + ' ' + ts, file = filename)
    os.system('rm ' + filename)
    p2 = time.time() - curr_ts'''
    #ts = time.time()
    #await client.send_message(sender.username, text + ' ' + str(ts))
    #print("Time taken to send by proxy : " + str(p2))
    #print("Total time 1 : " + str((2*p1)+p2) + ' ' + web)
    #print("Total time 2 : " + str((2*p2)+p1) + ' ' + web)
    #if 'hello' in event.raw_text:
    #    await event.reply('hi!')

client.start()
client.run_until_disconnected()
