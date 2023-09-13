import logging
import select
import socket
import struct
import os
import base64
import time
import socketserver
from socketserver import ThreadingMixIn, TCPServer, StreamRequestHandler
import asyncio

logging.basicConfig(level=logging.DEBUG)

#total_msgs = 0
def exchange_loop(client, remote):
    global total_msgs
    while True:
        #wait until client or remote is avaiable for read
        r, w, e = select.select([client, remote], [], [])

        if client in r:
            data = client.recv(2048)
            data = base64.b64decode(data)
            #text = text.decode('ascii')
            print("Received Data from client! Forwardng to end server!", len(data))
            if remote.send(data) <= 0:
                break

        if remote in r:
            #assuming tls_connection has been established properly
            if total_msgs > 19:  ###it was 26 when mod_client_listener has 27
                print("Total_msgs:::: ",total_msgs)
                data1 = b''
                # while len(data1) < 1024*1024:
                #     data1 += remote.recv(5*1024*1024)
                while True:
                    rcvd = remote.recv(2*1024*1024)
                    if(len(rcvd) <= 0) :
                        break
                    data1 += rcvd
                    print(f"[!] Bytes received from TOR: {len(data1)/1024/1024}")
                
                #one corner case still remains
                if(len(data1) > 0):
                    encoded = base64.b64encode(data1)
                    sendable_string = encoded.decode('ascii')
                    print(f"[!] Sending Bytes to mod_client_2: {len(sendable_string)}")
                    print(f"{sendable_string[0:10]} ---------- {sendable_string[-10:]}")
                    file_name = "~/file_download_tg_socks-main/index.txt"
                    file = open( file_name,"w")
                    file.write(sendable_string) #one-time checkup
                    
                    file.close()
                    #time.sleep(2)
                    os.system("python3 proxy_file_sender.py " + file_name)
                    file = open( file_name,"w")
                    file.truncate()
                    file.close()
                else:
                    print('Signing off from server.')
                    break
            else:           
                data = remote.recv(300)
                total_msgs = total_msgs + 1
                print("Total_msgs: ",total_msgs)
                print("Data recivd from end server ",len(data), "[Time: ",time.asctime(time.localtime())[11:20],"]")
                if(len(data) > 0):
                    encoded = base64.b64encode(data)
                    sendable_string = encoded.decode('ascii')
                    #print("text-to-proxy-mod-int-curl : " + sendable_string)
                    #time.sleep(2)
                    os.system("python3 proxy_data_sender.py " + sendable_string)
                else:
                    print('Signing off from server quite early.[Will exit after 5 seconds]')
                    #await asyncio.sleep(5)
                    time.sleep(5)
                    break
            #back_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #back_client.sendto(data, ("127.0.0.1", 9015))
            #if back_client.send(data) <= 0:
            #    break

###socks-client making connection with Tor [running on 127.0.0.1:9050]
def initial_tor_setup(rm, rm_addr, rm_port, client):
    print('----------------Connected to Tor-----------------')
    SOCK_VER, nmethods, method = 5, 1, 2
    request = struct.pack("!BBB", SOCK_VER,nmethods,method)
    rm.send(request)
    print('::First request with version, nmethods and method sent. \n1 host --> Tor')

    recv = rm.recv(2)
    ver, nm = struct.unpack("!BB", recv)
    print('::ver and nm received from Tor \nTor---> host ', ver, nm,'\n')
    
    if nm == 2:
        AUTH_VER, ULEN, UNAME, PLEN, PASSWD = 1 , 8 , 'username' , 8 , 'password'
        req2 = struct.pack("!BB",AUTH_VER,ULEN) + bytes(UNAME, 'ascii') + struct.pack("!B", PLEN) + bytes(PASSWD, 'ascii') 
        rm.send(req2)
        print('::Second request with auth_version, ulen, uname, plen, passwd  sent. \n2 host --> Tor', AUTH_VER,ULEN, UNAME, PLEN, PASSWD)
    

    ############response from server
    recv2 = rm.recv(2)
    a_ver, status = struct.unpack("!BB", recv2)
    print('::Response from server for authentication \n Tor --> host ',a_ver, status)
    print('------------Initial greetings done--------------')

    if status == 0:
        print('\n::Authentication successful')
        print('------------------------------------------------------')
        print('------------------------------------------------------\n')
    
    ###############################connection to rm_addr on behalf of client 
    CMD, RSV = 1, 0
    ATYP = 1 #make it 3 for domain name and 1 for IPv4 address
    print('::Pre-Request for web page sent. \n3a host-->Tor ', SOCK_VER, CMD, RSV, ATYP)
    if ATYP == 3:
        req3 = struct.pack("!BBBB",SOCK_VER, CMD, RSV,ATYP)      
        Domain = 'www.amazon.com'  #input from user
        domain_byte = bytes(Domain,'ascii')
        PORT = rm_port
        
        domain_length = len(domain_byte)
        req4 = struct.pack("!B", domain_length)
        req5 = PORT.to_bytes(2, byteorder='big')
        
        comp_req = req3 + req4 + domain_byte  + req5 
        rm.send(comp_req)
        print('::The case of ATYP = 3, Domain length, domain name and port sent. \n3b host-->Tor ',domain_length, Domain, PORT)
        
    ####when ATYP = 1 (ipv4 address)
    elif ATYP == 1:
        ipv4 = rm_addr
        DST_PORT = rm_port
        print('::Received addr and port in case of ipv4 now: ', ipv4, DST_PORT)
        req3 = struct.pack("!BBBB",SOCK_VER, CMD, RSV,ATYP)     
        DST_ADDR = socket.inet_aton(ipv4)
        
        req3_fin = req3 + DST_ADDR + DST_PORT.to_bytes(2, byteorder='big')
        rm.send(req3_fin)
        print('::The case of ATYP = 1, dst.addr and dst.port send. \nHost --> Tor ',DST_ADDR, DST_PORT)

    ##########receive response of web-page access from Tor
    recv3 = rm.recv(10)
    sock_v, reply, rsrv, addr_type, addr, port = struct.unpack("!BBBBIH", recv3)
    print('::Response from Tor on web-request: \nTor-->host ',sock_v, reply, rsrv, addr_type, addr, port)

    if reply == 0:
        print('::Tor has succeeded in connecting to remote destination [', addr, ':', port, ']')
        print('::Data exchange phase for website:',ipv4)
        
        exchange_loop(client, rm)
    
    else:
        print('::Tor failed to connect to the destination with Reply code - ',reply)
        print('\nCode info as follows:\n00 succeeded',
              '\n01 general SOCKS server failure',
              '\n02 connection not allowed by ruleset',
              '\n03 Network unreachable',
              '\n04 Host unreachable',
              '\n05 Connection refused',
              '\n06 TTL expired',
              '\n07 Command not supported',
              '\n08 Address type not supported',
              '\n09 to FF unassigned ')     

if __name__ == '__main__':

    UDP_IP_ADDRESS = "127.0.0.1"
    UDP_PORT_NO = 9014

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

    global total_msgs
    while(1):
        #just checking if below solution will resolve the problem
        #client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #client.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

        data = ''
        data = client.recv(400) 
        if len(data)<0:
            print('All Done FN')
            break
        print('First data Received from Client')
        # Do some processing here to get the address and port
        #text = data.decode('ascii')
        print("as is:",data,"Len(data): ", len(data))

        #hard-coding ip.addr and port for checking if consecutive requests will be served
        #to remove hard-code: delete if condition
        #if total_msgs < 10:
        text = base64.b64decode(data)
        text = text.decode('ascii')
        print(text)
        #address = "1"
        #port = "2"

        #if text[0] == 'a':
        __, address, port = text.split()
        port = int(port)
        print("Address :" + address + " Port :" + str(port))

        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #xe-added below line to keep the socket open for 1 hr in case of long silences
        #socket.setdefaulttimeout(3600)

        remote.connect(("127.0.0.1",9050))

        #xe-added below line to not let the tor close the connection for 1 hour due to silence in reading
        #remote.settimeout(3600)

        total_msgs = 0
        initial_tor_setup(remote, address, port, client)
        print('::This URL from client has been served.')
        while 1:
            pass
        break

