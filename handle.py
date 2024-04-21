# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import receive, reply
from db import Service


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
            # print("Handle Post webdata is ", webData)
            # 后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                # 获取传入
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                service = Service(recMsg)

                if recMsg.MsgType == 'text':
                    replyMsg = reply.TextMsg(toUser, fromUser, service.operate())
                    return replyMsg.send()

                elif recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()
                elif recMsg.MsgType == 'event':
                    if recMsg.Event == 'subscribe':
                        service.subscribe(recMsg)
                        content = "欢迎关注EasocenAdonis的公众号，我们将为您提供最新的信息\n" \
                                  "回复以下关键字获取相关信息\n" \
                                  "1.全部offer：获取所有offer信息，超过十条时只显示十条\n" \
                                  "2.分页查询：分页查询offer信息，示例：分页查询 1 10\n" \
                                  "3.参数查询：获取符合条件的offer信息\n" \
                                  "   示例：参数查询 公司=字节跳动\n" \
                                  "4.详情：获取招聘信息详情，后跟uuid\n" \
                                  "   示例：详情 fe26eb04-24a4-4755-b223-c88251b454a3\n" \
                                  "5.创建offer：创建offer信息,单个用户限定上限十条\n" \
                                  "   示例：创建offer 公司=字节跳动 公司ID=1 城市=北京 职位=Java开发工程师 UUID=1\n" \
                                  "6.更新offer：更新offer信息\n" \
                                  "   示例：更新offer 公司=字节跳动 公司ID=1 城市=北京 职位=Java开发工程师 UUID=1\n" \
                                  "7.删除offer：删除offer信息,后跟uuid\n" \
                                  "   示例：删除offer 1\n"
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                        return replyMsg.send()
                else:
                    return reply.Msg().send()
            else:
                print("暂且不处理")
                return "success "
        except Exception as Argument:
            return Argument
