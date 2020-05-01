import threading
from time import sleep,ctime
def sing():
    for i in range(3):
        print('sing %s' %i)
        sleep(1)
def dance():

    for i in range(3):
        print('dancing %s' %i)
        sleep(1)

if __name__ == '__main__':
    print('------------>')
    t1 = threading.Thread(target=sing)
    t2 = threading.Thread(target=dance)
    t1.start()
    t2.start()
    print('------->end---> %s'%ctime())
    while True:
        length = len(threading.enumerate())
        print('the current pro:%d'%length)
        if length<=1:
            break
        sleep(0.5)
