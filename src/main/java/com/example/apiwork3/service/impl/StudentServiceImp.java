package com.example.apiwork3.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.apiwork3.dao.StudentMapper;
import com.example.apiwork3.domain.Student;
import com.example.apiwork3.service.StudentService;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class StudentServiceImp extends ServiceImpl<StudentMapper, Student>  implements StudentService {

    /**
     * 获取指定数量的随机学生信息
     * @param num 1~1000的int值
     * @return 相应数量的随机学生信息
     */
    @Override
    public List<Student> getStudents(int num) {
        //随机生成num个1-100000的int值
        List<Integer> ids = new ArrayList<>();
        for (int i = 0; i < num; i++) {
            ids.add((int) (Math.random() * 100000) + 1);
        }
        return this.baseMapper.selectBatchIds(ids);
    }
}
