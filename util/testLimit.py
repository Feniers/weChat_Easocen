import time
import uuid

import pymysql
import requests
from math import ceil

import receive





class DBManager(object):
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    # 连接数据库
    def connect(self):
        self.conn = pymysql.connect(
            host='172.17.0.9',
            port=3306,
            user='root',
            password='13619402818ydh',
            database='wx',
            charset='utf8'
        )
        self.conn.ping(reconnect=True)
        self.cursor = self.conn.cursor()

    def query_all(self):
        sql = "SELECT * FROM all_offers"
        self.cursor.execute(sql)
        count = self.cursor.rowcount
        data = self.cursor.fetchall()
        return count, data

    # 分页查询
    def query_limit(self, sql, offset, number=10):
        try:
            self.conn.begin()
            limit_param = f'limit {offset}, {number}'
            ex_sql = " ".join([sql, limit_param])
            self.cursor.execute(ex_sql)  # 修改，由arge改为*args
            db_limit_res = self.cursor.fetchall()
            self.conn.commit()
            return db_limit_res
        except pymysql.Error as e:
            self.conn.rollback()
            return '数据库操作失败:' + str(e)

    # 单条数据查询
    def query_single(self, sql):
        try:
            self.conn.begin()
            self.cursor.execute(sql)
            db_single_res = self.cursor.fetchone()
            self.conn.commit()
            return db_single_res
        except pymysql.Error as e:
            self.conn.rollback()
            return '数据库操作失败:' + str(e)

    # 插入，更新，删除
    def update_delete(self, sql, uuid):
        if self.query_exist(uuid):
            try:
                self.conn.begin()
                self.cursor.execute(sql)
                self.conn.commit()
                return '数据库操作成功！'
            except pymysql.Error as e:
                self.conn.rollback()
                return '数据库操作失败:' + str(e)
        else:
            return '数据不存在'

    def insert(self, sql, offer=None):
        if self.check_valid_user(offer['company_uuid']):
            return '异常操作，您的上传已被禁止'
        # 如果不存在则插入
        if not self.query_exist(offer=offer):
            try:
                self.conn.begin()
                self.cursor.execute(sql)
                self.conn.commit()
                return '数据库操作成功！'
            except pymysql.Error as e:
                self.conn.rollback()
                return '数据库操作失败:' + str(e)
        else:
            return '数据已存在'

    # 查询一条数据是否存在
    def query_exist(self, uuid=None, offer=None):
        sql = None
        if uuid is not None:
            sql = f"SELECT * FROM all_offers WHERE uuid='{uuid}'"
        elif offer is not None:
            sql = "SELECT * FROM all_offers WHERE "
            for key, value in offer.items():
                sql += f"{key}='{value}' AND "
            sql = sql[:-4]
        else:
            return False
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            return True
        else:
            return False

    def check_valid_user(self, company_uuid):
        sql = f"SELECT * FROM user WHERE company_uuid='{company_uuid}'"
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            return False
        else:
            return True


    def close(self):
        self.cursor.close()
        self.conn.close()


class Service(object):
    def __init__(self):
        # 定义参数映射字典
        self.FromUserName = '管理员录入'
        self.offer_param_mapping = {
            '公司': 'company_name',
            '录入人': 'company_uuid',
            '城市': 'recruit_city',
            '标题': 'recruit_title',
            'UUID': 'uuid'
        }
        self.sql = "SELECT * FROM all_offers"
        self.page_count = None
        self.page = None
        self.size = 10
        self.db = DBManager()

    def operate(self, rec_msg):
        pre_params = rec_msg.strip().split()
        command = pre_params[0]
        if command == '全部offer':
            cnt, data = self.all_query()
            if cnt is None:
                return '查询失败'
            elif cnt <= 10:
                return f"共有 {cnt} 条数据\n{data}"
            else:
                return f"共有 {cnt} 条数据\n多余10条，请使用分页查询指令\n示例：分页查询 1 10"
        elif command == '分页查询':
            # 全部查询，获得总页数
            self.all_query()
            # 获取页数和每页数量
            if len(pre_params) == 3:
                page = int(pre_params[1])
                size = int(pre_params[2])
                data = self.page_query(page, size)
                # 逐行输出data元组
                # ('民生银行', '42d157a2-9af9-4208-9f84-10e72e9adee0', 1712763822, 20240414, 0, 2, '青岛｜烟台｜威海｜日照', '民生银行青岛分行2024届校园招聘', '管理员录入')
                data = '\n'.join(
                    [' '.join([str(row[0]), str(row[1]), str(row[3]), str(row[6]), str(row[7])]) for row in data])
                return f"第{page}/{self.page_count}页数据\n" \
                       f"公司  uuid  城市  标题\n" \
                       f"{data}"
            else:
                return '参数错误'
        elif command == '参数查询':
            offer = self.get_params(rec_msg)
            sql = "SELECT * FROM all_offers WHERE "
            for key, value in offer.items():
                sql += f"{key}='{value}' AND "
            data = self.db.query_single(sql[:-4])
            if data is not None:
                rep = '公司={} uuid={} 录入人={} 城市={} 标题={}'.format(data[0], data[1], data[3], data[6], data[7])
            else:
                rep = '没有符合条件的数据'
            return rep
        elif command == '创建offer':
            offer = self.get_params(rec_msg)
            # sql = f"INSERT INTO all_offers ({','.join(offer.keys())}) VALUES ({','.join(offer.values())})"
            # 添加创建时间，时间戳，自动创建uuid，company_uuid=self.msg.FromUserName
            sql = "INSERT INTO all_offers ({},create_time,uuid,company_uuid) VALUES ({},'{}','{}','{}')" \
                .format(', '.join(offer.keys()),
                        ', '.join(['\'' + offer[key] + '\'' for key in offer.keys()]),
                        time.time(), uuid.uuid1(), self.FromUserName)
            return self.db.insert(sql, offer=offer)
        elif command == '更新offer':
            offer = self.get_params(rec_msg)
            sql = "UPDATE all_offers SET {} WHERE uuid='{}'".format(
                ', '.join(["{}='{}'".format(key, offer[key]) for key in offer.keys()]), offer['uuid'])
            return self.db.update_delete(sql, uuid=offer['uuid'])
        elif command == '删除offer':
            offer = self.get_params(rec_msg)
            sql = f"DELETE FROM all_offers WHERE uuid='{offer['uuid']}'"
            return self.db.update_delete(sql, uuid=offer['uuid'])
        elif command == '详情':
            detail_uuid = pre_params[1]
            return self.get_detail(detail_uuid)
        else:
            return '指令错误'

    def get_params(self, rec_msg):
        pre_params = rec_msg.strip().split()
        params = pre_params[1:]
        offer = {}
        if len(params) <= len(self.offer_param_mapping):
            for param in params:
                key, value = param.split('=')
                if key not in self.offer_param_mapping:
                    return Exception("参数名不正确")
                offer[self.offer_param_mapping.get(key)] = value
        else:
            return Exception("参数格式不正确")
        return offer

    def page_query(self, page, size=None):
        if size is not None:
            self.size = size
        if page is not None and page < self.page_count:
            self.page = page
        offset = (page - 1) * self.size
        return self.db.query_limit(self.sql, offset, self.size)

    def all_query(self):
        cnt, data = self.db.query_all()
        self.page_count = ceil(cnt / self.size)
        return cnt, data

    def get_detail(self, uuid):
        base_url = 'https://www.offershow.cn/api/od/get_recruit_plan_detail'
        params = {'recruit_plan_uuid': uuid}
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()['data']['recruit_plan_detail']
            rep_msg = "详情网址：https://www.offershow.cn/jobs/a_plan?recruit_plan_id={}\n" \
                      "招聘简介：\n" \
                      "{}\n" \
                      "{}\n" \
                      "===============\n" \
                      "工作城市：{}\n" \
                      "投递时间：{}--{}\n" \
                      "===============\n" \
                      "{}" \
                .format(uuid, data['company_name'], data['company_intro'], data['recruit_city'],
                        data['recruit_local_graduate_date_start'], data['recruit_local_graduate_date_end'],
                        data['recruit_intro'])
            return rep_msg
        else:
            return '查询失败，请重试'

if __name__ == '__main__':
    service = Service()

    # print("全部offer")
    # rec_msg = '全部offer'
    # print(service.operate(rec_msg))
    # print("分页查询")
    # rec_msg = '分页查询 1 10'
    # print(service.operate(rec_msg))
    # rec_msg = '分页查询 2 10'
    # print(service.operate(rec_msg))
    # print("参数查询")
    # rec_msg = '参数查询 公司=龙湖集团'
    # print(service.operate(rec_msg))
    # print("创建offer")
    # rec_msg = '创建offer 公司=测试公司 城市=北京 标题=项目经理'
    # print(service.operate(rec_msg))
    # print("更新offer")
    # rec_msg = '更新offer 公司=测试公司 城市=北京 标题=项目经理 UUID=13d42320-fe40-11ee-85ef-5254008a1b8d'
    # print(service.operate(rec_msg))
    # print("删除offer")
    # rec_msg = '删除offer UUID=13d42320-fe40-11ee-85ef-5254008a1b8d'
    # print(service.operate(rec_msg))
    print("详情")
    rec_msg = '详情 fe26eb04-24a4-4755-b223-c88251b454a3'
    print(service.operate(rec_msg))

    service.db.close()
