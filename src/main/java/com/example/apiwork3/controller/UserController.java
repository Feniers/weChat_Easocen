package com.example.apiwork3.controller;

import com.example.apiwork3.domain.Result;
import com.example.apiwork3.service.StudentService;
import org.hibernate.validator.constraints.Range;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Validated
public class UserController {
    @Autowired
    private StudentService studentService;

    @GetMapping("/students")
    public Result getStudents(@RequestParam @Range(min = 1, max = 1000) int num) {
        return new Result().ok(studentService.getStudents(num));
    }

}
