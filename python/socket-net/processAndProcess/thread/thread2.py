import threading
import time
def say(i):
    print(i,'-->wangwang..')
    time.sleep(1)
if __name__ == '__main__':
    for i in range(5):
        t = threading.Thread(target=say,args=[i])
        t.start()
