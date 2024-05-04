package com.example.apiwork3.dao;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.apiwork3.domain.Student;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface StudentMapper extends BaseMapper<Student> {
}
