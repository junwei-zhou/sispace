'''
待解决的问题：反射，静态应用与类的应用
'''

import socket
import json
import struct
import os
sk = socket.socket()
sk.connect(('127.0.0.1',9000))

def myrecv(info_len = 1024,sign=False):
    if sign:
        info_len = sk.recv(4)
        info_len = struct.unpack("i",info_len)[0]
    file_info = sk.recv(info_len).decode()
    file_dic = json.loads(file_info)
    return file_dic
def auth(opt):
    usr = input('please input name').strip()
    pwd = input('please input password').strip()
    dic = {"user":usr,"pwd":pwd,"operate":opt}
    str_dic = json.dumps(dic)
    sk.send(str_dic.encode())
    #接受服务端的数据
    return myrecv()

def register():
    res = auth('register')
    return res

def login():
    res = auth('login')
    return res

def myexit():
    opt_dic = {"operate":"myexit"}
    sk.send(json.dumps(opt_dic).encode())
    exit("welcome come next")
def download():
    operate_dict = {
        "operate":"download",
        "filename":"2020.mp4"
    }
    opt_str = json.dumps(operate_dict)
    sk.send(opt_str.encode('utf-8'))
    #避免粘包
    res = myrecv(sign=True)
    print(res)
    if res["result"]:
        #创建文件夹
        try:
            os.mkdir("download")
        except:
            pass
        #接受文件的名字和文件的大小
        dic = myrecv(sign=True)
        print(dic,"<2>")
        #接受真实的数据
        with open("./download/"+dic["filename"],mode="wb") as fp:
            while dic["filesize"]:
                content = sk.recv(1024)
                fp.write(content)
                dic["filesize"] -= len(content)
        print("client: file download over")
    else:
        print("client: file no found ")
operate_list1=[("login", login),("register", register), ("myexit", myexit)]
operate_list2=[("download", download),("myexit", myexit)]
def main(operate_list):
    for i,tup in enumerate(operate_list,start=1):
        print(i,tup[0])
    num = int(input("input num >>>>>").strip())
    res = operate_list[num-1][1]()
    return res
while True:
    res = main(operate_list1)
    print(res)
    if res["result"]:
        while True:
            res = main(operate_list2)
            print(res)
sk.close()