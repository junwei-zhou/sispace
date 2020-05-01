from socket import *
from threading import Thread
from time import sleep

def dealWithSocket(newSocket,destAddr):
    while True:
        recvData = newSocket.recv(1024)
        if len(recvData)>0:
            print('recv[%s]:%s'%(str(destAddr),recvData))
        else:
            print('%s is close'%str(destAddr))
            break
    newSocket.close()

def main():
    serSocket = socket(AF_INET,SOCK_STREAM)
    serSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    localaddr = ('',7788)
    serSocket.bind(localaddr)
    serSocket.listen(5)
    try:
        while True:
            print('wait the client')
            newSocket,destAddr = serSocket.accept()
            print('create the thread %s' %newSocket)
            client = Thread(target=dealWithSocket,args=(newSocket,destAddr))
            client.start()


    finally:
        serSocket.close()

if __name__ == '__main__':
    main()

