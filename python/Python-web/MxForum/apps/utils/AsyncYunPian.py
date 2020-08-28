import json
from urllib.parse import urlencode
#解决HTTPRequest传输的body不可一世字典，包括json。因此进行重新的编码。
from tornado import httpclient
from tornado.httpclient import HTTPRequest

class AsyncYunPian:
    def __init__(self, api_key):
        self.api_key = api_key

    async def send_single_sms(self,code, mobile):
        http_client = httpclient.AsyncHTTPClient()
        url = "https://sms.yunpian.com/v2/sms/single_send.json"
        text = "【慕学生鲜】您的验证码是{}。如非本人操作，请忽略本短信".format(code)
        post_request = HTTPRequest(url=url, method="POST", body=urlencode({
            "apikey": self.api_key,
            "mobile": mobile,
            "text": text
        }))
        res = await http_client.fetch(post_request)
        return json.loads(res.body.decode("utf8"))

if __name__ == "__main__":
    import tornado
    io_loop = tornado.ioloop.IOLoop.current()

    yun_pian = AsyncYunPian("d6c4ddbf50ab36611d2f52041a0b949e")

    #run_sync方法可以在运行完某个协程之后停止事件循环
    from functools import partial
    new_func = partial(yun_pian.send_single_sms, "1234", "18785625498")
    io_loop.run_sync(new_func)