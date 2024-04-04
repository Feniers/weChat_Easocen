# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web

class Handle(object):
    def GET(self):
        try:
            data = web.input()
            # print("Received data: ", data)  # 输出接收到的请求内容
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "EasocenAdonis"  # 请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            # map(sha1.update, list)

            # 对列表中的每个元素进行散列更新
            for param in list:
                sha1.update(param.encode('utf-8'))  # 将字符串转换为字节串并进行更新

            hashcode = sha1.hexdigest()
            print("handle/GET func: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return "error"
        except Exception as Argument:
            return Argument