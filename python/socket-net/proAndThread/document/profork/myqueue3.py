from multiprocessing import Manager,Pool
import os,time,random
def reader(q):
    print("reader coming(%s),farther pid(%s)"%(os.getpid(),os.getppid()))
    for i in range(q.qsize()):
        print("reader from queue get message:%s"%q.get(True))
def writer(q):
    print("writer coming(%s),farther pid(%s)"%(os.getpid(),os.getppid()))
    for i in "dongGe":
        q.put(i)
if __name__=="__main__":
    print("(%s) start"%os.getpid())
    q=Manager().Queue() #using Manager's Queue to init
    po=Pool()
    #using pool
    po.apply(writer,(q,))
    po.apply(reader,(q,))
    po.close()
    po.join()
    print("(%s) End"%os.getpid())
