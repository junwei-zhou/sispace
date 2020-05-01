from multiprocessing import Pool
import os,time,random

def worker(msg):
    t_start = time.time()
    print("%s is coming,pid is %d" %(msg,os.getpid()))
    time.sleep(random.random()*2)
    t_stop = time.time()
    print(msg,"is end ,spend time is %0.2f" %(t_stop-t_start))

po = Pool(3)
for i in range(0,10):
    po.apply_async(worker,(i,))

print('----start---->')
po.close()
po.join()
print('-----end----->')
