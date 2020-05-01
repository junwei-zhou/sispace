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
    sleep(4)
    print('------->end---> %s'%ctime())
