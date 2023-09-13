import logging
import select
import socket
import struct
import os
from socketserver import ThreadingMixIn, TCPServer, StreamRequestHandler
import time

logging.basicConfig(level=logging.DEBUG)
SOCKS_VERSION = 5
INT_IP_ADDR = "127.0.0.1"
INT_PORT = 9012


class ThreadingTCPServer(ThreadingMixIn, TCPServer):
    pass


class SocksProxy(StreamRequestHandler):
    username = 'username'
    password = 'password'

    def handle(self):
        logging.info('Accepting connection from %s:%s' % self.client_address)

        # greeting header
        # read and unpack 2 bytes from a client
        header = self.connection.recv(2)
        version, nmethods = struct.unpack("!BB", header)

        # socks 5
        assert version == SOCKS_VERSION
        assert nmethods > 0

        # get available methods
        methods = self.get_available_methods(nmethods)

        # accept only USERNAME/PASSWORD auth
        '''if 2 not in set(methods):
            # close connection
            self.server.close_request(self.request)
            return'''

        # send welcome message
        self.connection.sendall(struct.pack("!BB", SOCKS_VERSION, 0))

        '''if not self.verify_credentials():
            return'''

        # request
        version, cmd, _, address_type = struct.unpack("!BBBB", self.connection.recv(4))
        assert version == SOCKS_VERSION

        if address_type == 1:  # IPv4
            address = socket.inet_ntoa(self.connection.recv(4))
        elif address_type == 3:  # Domain name
            domain_length = self.connection.recv(1)[0]
            address = self.connection.recv(domain_length)
            address = socket.gethostbyname(address)

        port = struct.unpack('!H', self.connection.recv(2))[0]

        # reply
        try:
            if cmd == 1:  # CONNECT
                logging.info('Trying to establish connection with the Intermediate code!')
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #remote.connect((address, port))
                remote.connect((INT_IP_ADDR, INT_PORT))

                #increasing the socket timeout to 1 hour
                #remote.settimeout(3600)

                bind_address = remote.getsockname()
                #Send address and port in the first packet
                address_info = bytes("address ", 'ascii')
                address_info += bytes(address, 'ascii')
                address_info += bytes(" ", 'ascii')
                address_info += bytes(str(port), 'ascii')
                remote.send(address_info)
                #logging.info('Connected to %s %s' % (address, port))
                logging.info('Connected to %s %s' % (INT_IP_ADDR, INT_PORT))
            else:
                self.server.close_request(self.request)

            addr = struct.unpack("!I", socket.inet_aton(bind_address[0]))[0]
            port = bind_address[1]
            reply = struct.pack("!BBBBIH", SOCKS_VERSION, 0, 0, 1,addr, port)

        except Exception as err:
            logging.error(err)
            # return connection refused error
            reply = self.generate_failed_reply(address_type, 5)

        self.connection.sendall(reply)

        # establish data exchange
        if reply[1] == 0 and cmd == 1:
            self.exchange_loop(self.connection, remote)

        self.server.close_request(self.request)

    def get_available_methods(self, n):
        methods = []
        for i in range(n):
            methods.append(ord(self.connection.recv(1)))
        return methods

    def generate_failed_reply(self, address_type, error_number):
        return struct.pack("!BBBBIH", SOCKS_VERSION, error_number, 0, address_type, 0, 0)

    def exchange_loop(self, client, remote):

        while True:

            # wait until client or remote is available for read
            r, w, e = select.select([client, remote], [], [])

            if client in r:
            
                data = client.recv(2048)
                print(client)
                #os.system('python3.6 client_requester.py ' + str(data))
                
                print('Data sent to int_client at time: ',time.asctime(time.localtime())[11:20])
                if remote.send(data) <= 0:
                    break
                ##else:
                ##    print('Data sent to int_client at time: ',time.asctime(time.localtime())[11:20])

            if remote in r:
                # data = remote.recv(400)
                data = remote.recv(20*1024*1024)
                #print(data)
                if client.send(data) <= 0:
                    break


if __name__ == '__main__':
    server = ThreadingTCPServer(('127.0.0.1', 9011), SocksProxy)
    server.serve_forever()

#connection break after 5.00925 minutes
