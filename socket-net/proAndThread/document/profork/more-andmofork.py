import os
import time
pid = os.fork()
if pid == 0:
    print('--->1')
else:
    print('--->2')
pid = os.fork()
if pid == 0:
    print('--->3')
else:
    print('--->4')
time.sleep(8)
