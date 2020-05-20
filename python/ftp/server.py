import  socketserver
import json
import os
import hashlib
import struct
base_path = os.path.dirname(__file__)
userinfo = os.path.join(base_path,"db","userinfo.txt")
class Auth():
    @staticmethod
    def md5(usr,pwd):
        md5_obj = hashlib.md5(usr.encode())
        md5_obj.update(pwd.encode())
        return md5_obj.hexdigest()
    @classmethod
    def register(cls,opt_dic):
        with open(userinfo,mode='r',encoding='utf-8') as fp:
            for line in fp:
                username = line.split(":")[0]
                if username == opt_dic["user"]:
                    return {"result":False,"info":"username used"}
        with open(userinfo,mode='a+',encoding='utf-8') as fp:
            fp.write("%s:%s\n" % (opt_dic["user"],cls.md5(opt_dic["user"],opt_dic["pwd"])))
        return {"result":True,"info":"successed"}
    @classmethod
    def login(cls,opt_dic):
        with open(userinfo,mode='r',encoding='utf-8') as fp:
            for line in fp:
                username,password = line.strip().split(":")
                if username == opt_dic['user'] and password == cls.md5(opt_dic["user"],opt_dic["pwd"]):
                    return {"result":True,"info":"login successed"}
            return {"result":False,"info":'login fail'}
    @classmethod
    def myexit(cls,opt_dic):
        return {"result":"myexit"}

class ftpServe(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            opt_dic = self.myrecv()
            print(opt_dic)
            #反射处理不同类的函数
            if hasattr(Auth,opt_dic["operate"]):
                res = getattr(Auth,opt_dic["operate"])(opt_dic)
                if res['result']=="myexit":
                    return
                # 将返回的数据发送给客户端
                self.mysend(res)
                if res["result"]:
                    while True:
                        opt_dic = self.myrecv()
                        print(opt_dic)
                        if opt_dic["operate"] == "myexit":
                            return
                        if hasattr(self,opt_dic["operate"]):
                            getattr(self,opt_dic["operate"])(opt_dic)
            else:
                dic = {"result":False,"info":'no'}
                self.mysend(dic)

    #接受数据
    def myrecv(self):
        info = self.request.recv(1024)
        opt_str = info.decode()
        opt_dic = json.loads(opt_str)
        return opt_dic
    #发送数据
    def mysend(self,send_info,sign=False):
        #将字典->字符串->字节流
        send_info = json.dumps(send_info).encode()
        if sign:
            res =struct.pack("i",len(send_info))
            self.request.send(res)
        self.request.send(send_info)
    def download(self, opt_dic):
        # print(opt_dic)
        filename = opt_dic["filename"]
        file_abs = os.path.join(base_path, "video", filename)
        print(filename)
        print(file_abs)
        if os.path.exists(file_abs):
            #告诉用户是否存在该文件
            dic = {"result": True, "info": "file exit"}
            self.mysend(dic, sign=True)
            #发送文件的大小和名字
            filesize = os.path.getsize(file_abs)
            dic = {"filename":filename,"filesize":filesize}
            self.mysend(dic,sign=True)
            #文件的内容发送
            with open(file_abs,mode="rb") as fp:
                while filesize:
                    content = fp.read(1024)
                    self.request.send(content)
                    filesize -= len(content)
            print("download over")
        else:
            dic = {"result":False,"info":"file not found"}
            self.mysend(dic,True)
myserver = socketserver.ThreadingTCPServer(("127.0.0.1",9000), ftpServe)
#让一个端口绑定多个程序，一般用于测试。
#socketserver.TCPServer.allow_reuse_address = True
myserver.serve_forever()