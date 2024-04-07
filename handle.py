# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import receive, reply


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

    def POST(self):
        try:
            webData = web.data()
            print("Handle Post webdata is ", webData)
            # 后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                # 获取传入
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName

                if recMsg.MsgType == 'text':
                    textMsg = receive.TextMsg(recMsg)
                    content = textMsg.Content
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()

                if recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()
                else:
                    return reply.Msg().send()
            else:
                print("暂且不处理")
                return "success"
        except Exception as Argment:
            return Argment
