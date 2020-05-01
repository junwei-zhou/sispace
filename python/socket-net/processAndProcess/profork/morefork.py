import os
import time
num = 0
pid = os.fork()
if pid == 0:
    num+=1
    print('  1---num=%d'%num)
else:
    time.sleep(1)
    num+=1
    print('  2---num=%d'%num)
