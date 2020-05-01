from multiprocessing import Process
import os

def run_proc(name):
    print('son proc is operating,name=%s,pid=%s' %(name,os.getpid()))

if __name__ == '__main__':
    print('farther proc %d0' %os.getpid())
    p = Process(target=run_proc,args=('test',))
    print('tht son ...')
    p.start()
    p.join()
    print('is end')
