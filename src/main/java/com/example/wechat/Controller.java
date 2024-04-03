package com.example.wechat;

import com.example.wechat.utils.CheckUtil;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.HashMap;
import java.util.Map;

@org.springframework.stereotype.Controller
public class Controller {
    @GetMapping("/verify_wx_token")
    public void login(HttpServletRequest request, HttpServletResponse response) throws UnsupportedEncodingException {
        request.setCharacterEncoding("UTF-8");
        String signature = request.getParameter("signature");
        String timestamp = request.getParameter("timestamp");
        String nonce = request.getParameter("nonce");
        String echostr = request.getParameter("echostr");
        PrintWriter out = null;
        try {
            out = response.getWriter();
            if (CheckUtil.checkSignature(signature, timestamp, nonce)) {
                out.write(echostr);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            out.close();
        }
    }

//    @PostMapping("/verify_wx_token")
//    public void handler(HttpServletRequest request, HttpServletResponse response) throws Exception {
//        request.setCharacterEncoding("UTF-8");
//        response.setCharacterEncoding("UTF-8");
//        PrintWriter out = response.getWriter();
//        Map<String, String> parseXml = MessageUtil.parseXml(request);
//        String msgType = parseXml.get("MsgType");
//        String content = parseXml.get("Content");
//        String fromusername = parseXml.get("FromUserName");
//        String tousername = parseXml.get("ToUserName");
//        System.out.println(msgType);
//        System.out.println(content);
//        System.out.println(fromusername);
//        System.out.println(tousername);
//    }

}
