#!/usr/bin/env python

import sys
import struct
import time

if sys.version_info[0] < 3:
    import SocketServer as socketserver
else:
    import socketserver

class MeshHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.buf = bytearray()
        print(self)
        try:
            while True:
                header = self.read_full(4)
                l, = struct.unpack_from('<H', header[2:4])
                body = self.read_full(l-4)
                req = bytearray()
                req.extend(header)
                req.extend(body)
                resp = bytearray()
                resp.extend(req[0:4])
                resp.extend(req[10:16])
                resp.extend(req[4:10])
                resp.extend(req[16:])
                self.request.sendall(resp)
                log= "%02x%02x%02x%02x%02x%02x\r\n"%(req[10],req[11],req[12],req[13],req[14],req[15]) 
                timeArray = time.strptime(time.time(), "%Y-%m-%d %H:%M:%S")
               
                print(log)
                print(timeArray)

        except Exception as e:
            print(e)

    def read_full(self, n):
        while len(self.buf) < n:
            try:
                req = self.request.recv(1024)
                if not req:
                    raise(Exception('recv error'))
                self.buf.extend(req)
            except Exception as e:
                raise(e)
        read = self.buf[0:n]
        self.buf = self.buf[n:]
        return bytes(read)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 7000
    server = ThreadedTCPServer((HOST, PORT), MeshHandler)
    server.allow_reuse_address = True
    print('mesh server works')
    server.serve_forever()
