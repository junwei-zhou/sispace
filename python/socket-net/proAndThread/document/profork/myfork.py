import os
rpid = os.fork()
if rpid<0:

    print("fork is fail")
elif rpid == 0:
    print("my son process(%s),my farther (%s)"%(os.getpid(),os.getppid()))
else:
    print("my farther (%s),my son process(%s)"%(os.getpid(),rpid))
print("all")
