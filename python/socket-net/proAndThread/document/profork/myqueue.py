from multiprocessing import Queue
q=Queue(3)
q.put('1--->')
q.put('2--->')
print(q.full())
q.put('3--->')
print(q.full())

try:
    q.put('4',True,8)
except:
    print('the queue is fully %s' %q.qsize())

#try:
#    q.put('5')
#except:
#    print('the queue is fully %s' %q.qsize())
if not q.full():
    q.put_nowait('6--->')

if not q.empty():
    for i in range(q.qsize()):
        print(q.get_nowait())

