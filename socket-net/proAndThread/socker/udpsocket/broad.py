import socket,sys
dest = ('<broadcast>', 8778)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
data='hi'.encode('utf-8')
s.sendto(data, dest)
print ("wait(ctrl+c exit)")
while True:
    (buf, address) = s.recvfrom(2048)
    print ("Received from %s: %s" % (address, buf))
