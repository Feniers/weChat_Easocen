import requests
import time
import random


def send_request(num):
    url = "http://localhost:9090/students"
    params = {'num': num}
    try:
        send_time = time.time()
        response = requests.get(url, params=params)
        output = f"时间：{send_time}, 请求状态码：{response.status_code}, 请求耗时：{time.time() - send_time:.2f}秒, 请求参数：{params}\n"
        if response.status_code == 200:
            return True, output
        else:
            return False, output
    except Exception as e:
        output = f"Exception: {e}\n"
        return False, output


def test_api(qps, duration, output_file):
    total_requests = 0
    successful_requests = 0
    failed_requests = 0

    with open(output_file, 'a') as file:
        for second in range(duration):
            file.write(f"开始第 {second + 1} 秒的请求...\n")
            start_time = time.time()
            for _ in range(qps):
                num = random.randint(1, 1000)
                result, output = send_request(num)
                file.write(output)
                if result:
                    successful_requests += 1
                else:
                    failed_requests += 1
                total_requests += 1
                time.sleep(1 / qps)
            end_time = time.time()

            success_rate = (successful_requests / total_requests) * 100 if total_requests > 0 else 0
            file.write(f"本秒成功率: {success_rate:.2f}%\n")
            file.write(f"累计成功请求数: {successful_requests}\n")
            file.write(f"累计失败请求数: {failed_requests}\n")
            file.write(f"累计请求次数: {total_requests}\n")
            file.write(f"本秒请求耗时: {end_time - start_time:.2f}秒\n\n")


if __name__ == "__main__":
    while True:
        qps = int(input("请输入每秒请求数: "))
        duration = int(input("请输入持续时间(秒): "))
        output_file = "output.txt"
        test_api(qps, duration, output_file)
        print("测试结束，结果已写入文件\n")
        time.sleep(1)
