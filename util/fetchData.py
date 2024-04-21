import csv
import json

import pymysql
import requests
from sklearn.metrics import roc_auc_score

auc=roc_auc_score(y_test, y_pred)

def fetch_data():
    # 定义请求URL和初始页码、页面大小
    base_url = "https://www.offershow.cn/api/od/search_plan"
    page = 1
    size = 15

    all_offers = []  # 保存所有数据

    while True:
        # 构建请求参数
        params = {'page': page, 'size': size}
        response = requests.post(base_url, params=params)

        # 检查状态码
        if response.status_code == 200:
            # 获取数据
            data = response.json()

            plans = data['data']['plans']
            for plan in plans:
                all_offers.append({
                    'company_name': plan['company_name'],
                    'uuid': plan['uuid'],
                    'create_time': plan['create_time'],
                    'end_time': plan['end_time'],
                    'is_official': plan['is_official'],
                    'plan_type': plan['plan_type'],
                    'recruit_city': plan['recruit_city'],
                    'recruit_title': plan['recruit_title'],
                    'company_uuid': plan['company_uuid']
                })

            # 判断是否还有下一页
            # if len(data['data']['plans']) < size:
            if page == 2:
                break  # 已经到达最后一页，结束循环
            else:
                page += 1  # 继续下一页
        else:
            print("请求失败，状态码：", response.status_code)
            break

    print(" len： ", len(all_offers))

    # 将数据写入CSV文件
    with open('all_offers.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file,
                                fieldnames=['company_name', 'uuid', 'create_time', 'end_time', 'is_official',
                                            'plan_type', 'recruit_city',
                                            'recruit_title', 'company_uuid'])

        writer.writeheader()
        for line in all_offers:
            writer.writerow(line)
        file.close()
        # writer = csv.DictWriter(file, fieldnames=['company_name', 'uuid', 'create_time', 'end_time', 'is_official',
        #                                           'plan_type', 'recruit_city',
        #                                           'recruit_title', 'company_uuid'])
        #
        # writer.writeheader()
        # for line in all_offers:
        #     writer.writerow(line)


if __name__ == '__main__':
    fetch_data()
