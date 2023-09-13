from telethon import TelegramClient
import logging
import select
import socket
import struct
import os
import base64
import time
from socketserver import ThreadingMixIn, TCPServer, StreamRequestHandler

logging.basicConfig(level=logging.DEBUG)

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 9013

#client_number = 0

class ThreadingTCPServer(ThreadingMixIn, TCPServer):
    pass

remaining = b''
class SocksProxy(StreamRequestHandler):

    def handle(self):
        logging.info('Accepting connection from %s:%s' % self.client_address)
        #global client_number
        try:
            #if cmd == 1:  # CONNECT
            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote.connect((UDP_IP_ADDRESS, UDP_PORT_NO))
            remote2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote2.connect((UDP_IP_ADDRESS, 9016))

        except Exception as err:
            logging.error(err)

        # establish data exchange
        self.exchange_loop(self.connection, remote, remote2)

        self.server.close_request(self.request)

    def exchange_loop(self, client, remote, remote2):
        global remaining
        while True:

            # wait until client or remote is available for read
            r, w, e = select.select([client, remote, remote2], [], [])

            if client in r:
                data = client.recv(2048)
                if(len(data) <=0):
                    break;
                #print(client)
                #Encode the data to base64 for easily sending it as an argument
                encoded = base64.b64encode(data)
                sendable_string = encoded.decode('ascii')
                print("Data sent to IM App!")
                
                #time.sleep(0.5)
                os.system('python3 ~/file_download_tg_socks-main/client_requester.py ' + sendable_string)

            if remote in r:
                data = remote.recv(400)
                if(len(data) <= 0):
                   break;
               
                final = base64.b64decode(data) 
                print("Data received from IM App [mod-client listener]! [Time: ", time.asctime(time.localtime())[11:20], "]")
                #print("Received data " + str(data) + "\n Decoded data " + str(final))
                if client.send(final) <= 0:
                    break

            if remote2 in r:
                # data = remote2.recv(400)
                # data = remote2.recv(20971520)
                
                
                # print("-----------------------")
                # # print(data)
                # bla = open("data", "w")
                # bla.write(data.decode())
                # bla.close()
                # print("-----------------------")
                data = remaining
                while True:
                    int_data = remote2.recv(30*1024*1024)
                    ind = int_data.find(b'|')

                    print(f"DEBUG ==> len(int_data): {len(int_data)} ind: {ind}")
                    if len(int_data) == 0:
                        break
                    if ind >= 0:
                        print("xx xxx xxxx xxxxx x xxxxx")
                        data += int_data[:ind]
                        remaining = int_data[ind+1:]
                        # if remaining == b'':
                        #     remaining = b'?'
                        break
                    elif ind == -1:
                        print("append")
                        data += int_data
                    if(len(int_data) <= 0):
                        break;
                
                print(f"[!] Data received from mod_client_2: {len(data)}")
                print(f"{data[0:10]} ----------- {data[-10:]}")
                final = base64.b64decode(data)
                # final = base64.b64decode(data) 
                print('------------final-size:', len(final))
                #final = data.encode()
                print("Data received from IM App [mod-client listener2]! [Time: ", time.asctime(time.localtime())[11:20], "]")
                #print("Received data " + str(data) + "\n Decoded data " + str(final))
                if client.send(final) <= 0:
                    break

if __name__ == '__main__':
    server = ThreadingTCPServer(('127.0.0.1', 9012), SocksProxy)
    server.serve_forever()

