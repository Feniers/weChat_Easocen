package com.example.apiwork3.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.example.apiwork3.domain.Student;

import java.util.List;

public interface StudentService extends IService<Student> {

    List<Student> getStudents(int num);
}
