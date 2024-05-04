package com.example.apiwork3;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.EnableAspectJAutoProxy;
import org.springframework.scheduling.annotation.EnableScheduling;

@EnableAspectJAutoProxy
@EnableScheduling
@SpringBootApplication
@MapperScan("com.example.apiwork3.dao")
public class ApIwork3Application {

    public static void main(String[] args) {
        SpringApplication.run(ApIwork3Application.class, args);
    }



}
