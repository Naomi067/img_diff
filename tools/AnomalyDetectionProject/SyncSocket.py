#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import errno
import sys
import time
import configparser
import logging
DATEFMT ="[%Y-%m-%d %H:%M:%S]"
FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(level=logging.INFO,format=FORMAT,datefmt=DATEFMT,filename='ssim_test.log')

class SyncSocket(object):
    def __init__(self):
        # log("SyncSocket, __init__")
        logging.info("SyncSocket, __init__")
        self.SizePerRecv = 4096
        self.syncSocket = self.socket_init()

    def socket_init(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            # log("socket_init:%s" % str(e))
            sys.exit(-1)
        else:
            # log("Socket create success")
            logging.info("Socket create success")
        return s

    def socket_connect(self):
        try:
            self.syncSocket.connect((self.ip, self.port))
            self.syncSocket.settimeout(2)
        except socket.error as err:
            self.syncSocket.close()
            if err.errno == errno.ECONNREFUSED:
                return False, errno.ECONNREFUSED
            # log(err)
            sys.exit(-1)
        else:
            logging.info("Socket connect success "+ self.ip +":" +str(self.port))

    def sendmsg(self):
            count = self.syncSocket.send((self.luacmd+"\r\n").encode())
            logging.info("SyncSocket, content:%s, sended bytes:%s" % (self.luacmd, str(count)))
            buffer = []
            bufferData = b''
            while True:
                try:
                    msg = self.syncSocket.recv(SyncSocket.SizePerRecv)
                    #logging.info(msg)
                    if msg:
                        # buffer.append(msg.decode('utf-8', errors='ignore'))
                        bufferData += msg
                        # buffer.append(msg)
                        if len(msg) < SyncSocket.SizePerRecv:
                            #logging.info(SyncSocket.SizePerRecv)
                            break
                    else:
                        break
                except Exception as recvExption:
                    # log("SyncSocket, recvException:%s" % str(recvExption))
                    break
            # result = "".join(buffer)
            #logging.info(bufferData)
            result = bufferData.decode('utf-8')
            result = self.syncSocket.recv(8192).decode()
            logging.info("SyncSocket, result:%s" % str(result))
            return result
    
    def close(self):
        try:
            self.syncSocket.close()
        except Exception as e:
            sys.exit(-1)
        else:
            # log("Socket create success")
            logging.info("Socket close success")
        return
    
    def getcontent(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        qc_path = config.get('common', 'qc_path').replace("\\",'/')
        collection_script = config.get('common', 'collection_script').replace("\\",'/')
        self.ip = config.get('common', 'ip')
        self.port = int(config.get('common', 'port'))
        self.luacmd = 'pg.global.luaMgr:AddSearchPath(\"test\") \r\n local qcutil = require(\"' + qc_path + '/qcutil\") \r\n qcutil.initTestEnv(\"PM02\") \r\n qcutil.run(\"' + collection_script + '\")'
        logging.info(self.luacmd)
        pass


if __name__ == '__main__':
    syncSocket = SyncSocket()
    syncSocket.getcontent()
    syncSocket.socket_connect()
    syncSocket.sendmsg()
    time.sleep(20)
    syncSocket.close()
    pass