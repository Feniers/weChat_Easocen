package com.example.apiwork3.aop;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.concurrent.atomic.AtomicInteger;

@Component
@Aspect
public class QpsMonitorAspect {
    private static final Logger monitorLogger = LoggerFactory.getLogger("monitor");
    private static final Logger requestLogger = LoggerFactory.getLogger("request");
    private static final int MAX = 10;
    AtomicInteger count = new AtomicInteger(0);


    /**
     * 定义切点
     */
    @Pointcut("execution(* com.example.apiwork3.controller.UserController.getStudents(..))")
    public void monitor() {
    }

    /**
     * 环绕通知
     *
     * @param joinPoint 切点
     * @return 返回值
     * @throws Throwable 异常
     */
    @Around("monitor()")
    public Object around(ProceedingJoinPoint joinPoint) throws Throwable {
        if (count.get() > MAX) {
            requestLogger.error("Method: {}, Args: {}, Error：too many requests and qps limit is {}",
                    joinPoint.getSignature().toShortString(), joinPoint.getArgs(), MAX);
            throw new RuntimeException("服务器繁忙，请稍后再试");
        }

        long start = System.currentTimeMillis();
        // 计数器加1
        int currentCount = count.incrementAndGet();

        // 执行目标方法
        Object result = joinPoint.proceed();

        long end = System.currentTimeMillis();
        //输出详细日志，包括请求时间，线程id，线程名，方法名，参数，返回值，耗时，如果有异常的话的异常信息
        requestLogger.info("Request time: {},  Method: {}, Args: {}, Cost time: {}ms , Result: {}",
                start, joinPoint.getSignature().toShortString(),
                joinPoint.getArgs(), end - start, result);

        return result;
    }

    /**
     * 每秒执行一次，输出QPS
     */
    @Scheduled(fixedRate = 1000) // 每秒执行一次
    public void monitorQps() {
        int currentCount = count.getAndSet(0);
        //输出到文件
        if(currentCount > 0)
            monitorLogger.info("QPS: " + currentCount);
    }


}