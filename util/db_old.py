import time
import uuid

import pymysql
from dbutils.pooled_db import PooledDB



class DBConnect:
    _instance = None  # 保存类的实例

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'pool'):
            mysql_conf = {
                'host': '172.17.0.9',  # 数据库服务器主机地址
                'port': 3306,  # 端口号 可选 整型
                'user': 'root',  # 用户名
                'password': '13619402818ydh',  # 密码
                'database': 'wx',  # 数据库名称
                'charset': 'utf8'
            }
            self.pool = PooledDB(pymysql, 5, **mysql_conf)

    def getConnect(self):
        return self.pool.connection()



db = DBConnect()

def offers(offer):
    connection = db.getConnect()
    cursor = connection.cursor()

    data = None

    # 构建查询语句
    if offer == {}:
        sql = "SELECT * FROM `all_offers` WHERE 1=1"
    else:
        sql = "SELECT * FROM `all_offers` WHERE {}".format(
            ' AND '.join(["{}='{}'".format(key, offer[key]) for key in offer.keys()])
        )

    # 执行查询
    cursor.execute(sql)
    data_count = cursor.rowcount
    if data_count <= 10:
        data = cursor.fetchall()
    else:
        data = cursor.fetchmany(10)

    cursor.close()
    connection.close()

    response = data_count, str(data)

    return response


def create_offer(offer):
    connection = db.getConnect()
    try:
        cursor = connection.cursor()

        # 查询offer是否已经存在
        if exists_offer(offer) is not None:
            raise Exception("offer已经存在")

        # 若不存在
        # 添加创建时间，时间戳
        offer['create_time'] = time.time()
        # 自动创建uuid
        offer['uuid'] = uuid.uuid1()

        data = None

        # 构建 SQL 语句，动态指定列名
        sql = "INSERT INTO all_offers ({}) VALUES ({})".format(
            ', '.join(offer.keys()),  # 列名列表
            ', '.join(['%(' + key + ')s' for key in offer.keys()])  # 占位符列表
        )

        cursor.execute(sql, offer)
        connection.commit()
        cursor.close()
        return True
    except Exception as e:
        connection.rollback()
        return e
    finally:
        connection.close()


# 查询offer是否已经存在
# 若存在则返回uuid    若不存在则返回None
def exists_offer(offer):
    connection = db.getConnect()
    cursor = connection.cursor()

    # 查询offer是否已经存在
    select_sql = "SELECT * FROM `all_offers` WHERE 1=1 and {}".format(
        ' AND '.join(["{}='{}'".format(key, offer[key]) for key in offer.keys()])
    )
    cursor.execute(select_sql)
    # 若存在则返回uuid    若不存在则返回False
    if cursor.rowcount > 0:
        return cursor.fetchone()[1]
    else:
        return None


# 根据uuid查询offer
def get_offer_by_uuid(uuid):
    connection = db.getConnect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM all_offers WHERE uuid='{}'".format(uuid))
    data = cursor.fetchone()
    cursor.close()
    connection.close()
    return data


def update_offer(offer):
    connection = db.getConnect()
    try:
        data = get_offer_by_uuid(offer['uuid'])
        if data is None:
            raise Exception("offer不存在")

        cursor = connection.cursor()

        # 构建 SQL 语句，动态指定列名
        sql = "UPDATE all_offers SET {} WHERE uuid='{}'".format(
            ', '.join(["{}='{}'".format(key, offer[key]) for key in offer.keys()]),  # 列名列表
            data[1]  # 占位符列表
        )

        cursor.execute(sql)
        connection.commit()
        cursor.close()
        return True
    except Exception as e:
        connection.rollback()
        return e


def delete_offer(uuid):
    connection = db.getConnect()
    try:
        data = get_offer_by_uuid(uuid)
        if data is None:
            raise Exception("offer不存在")

        cursor = connection.cursor()

        # 构建 SQL 语句，动态指定列名
        sql = "DELETE FROM all_offers WHERE uuid='{}'".format(
            data[1]  # 占位符列表
        )

        cursor.execute(sql)
        connection.commit()
        cursor.close()
        return True
    except Exception as e:
        connection.rollback()
        return e


def subscribe(recMsg):
    connection = db.getConnect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE openid='{}'".format(recMsg.FromUserName))
    if cursor.rowcount == 0:
        cursor.execute("INSERT INTO user (openid, create_time) VALUES ('{}',{})".format(recMsg.FromUserName,time.time()))
        connection.commit()
    cursor.close()
    connection.close()
    return True
