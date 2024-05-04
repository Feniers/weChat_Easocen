package com.example.apiwork3.domain;

import lombok.Data;

@Data
public class Result {

    private int code;
    private String message;
    private Object data;

    public Result ok(Object data){
        this.code = 200;
        this.message = "success";
        this.data = data;
        return this;
    }

    public Result fail(String message){
        this.code = 500;
        this.message = message;
        return this;
    }


}
