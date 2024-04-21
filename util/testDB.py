import time
import uuid
from main import DBConnect
import pymysql.cursors

# 连接到数据库
# connection = pymysql.connect(host='172.17.0.9',
#                              port=3306,
#                              user='root',
#                              password='13619402818ydh',
#                              database='wx',
#                              charset='utf8')

# offer = {
#     'company_name': '测试公司',
#     'company_uuid': 'a0f6d7c0-6e8b-11e9-8f5c-00163e0d1d0f',
#     'recruit_city': '北京',
#     'recruit_title': 'Java开发工程师',
#     'uuid': 'a0f6d7c0-6e8b-11e9-8f5c-00163e0d1d0f'
# }
# 定义参数映射字典
offer_param_mapping = {
    '公司': 'company_name',
    '录入人': 'company_uuid',
    '城市': 'recruit_city',
    '标题': 'recruit_title',
    'UUID': 'uuid'
}

db = DBConnect()


# connection = db.getConnect()


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


def get_params(statement):
    # 提取参数部分
    pre_params = statement.strip().split()
    params = pre_params[1:]
    offer = {}
    if len(params) <= len(offer_param_mapping):
        for param in params:
            key, value = param.split('=')
            if key not in offer_param_mapping:
                return Exception("参数名不正确")
            offer[offer_param_mapping.get(key)] = value
    else:
        return Exception("参数格式不正确")
    return offer


# PATH = {
#     "我说你学": '学不会',
#     "全部offer": offers(),
#     "参数查询": lambda par_name, par_value: get_param(par_name, par_value)
#     "创建offer":
# }


def redirect(rec_msg):
    try:
        if rec_msg == '我说你学':
            return '学不会'
        elif rec_msg == '全部offer':
            data_count, data = offers({})
            return "共有 {} 条数据\n{}(超出10条仅显示10条)".format(data_count, data)
        elif rec_msg.startswith('参数查询'):
            # 提取参数部分
            offer = get_params(rec_msg)
            data_count, data = offers(offer)
            return "共有 {} 条数据\n{}".format(data_count, data)
        elif rec_msg.startswith('创建offer'):
            # 输入 ”创建offer 公司=测试公司 公司ID=a0f6d7c0-6e8b-11e9-8f5c-00163e0d1d0f 城市=北京 职位=Java开发工程师 UUID=a0f6d7c0-6e8b-11e9-8f5c-00163e0d1d0f“ 或更多参数
            offer = get_params(rec_msg)
            re= create_offer(offer)
            if re is not True:
                raise re
        elif rec_msg.startswith('更新offer'):
            # 提取参数部分
            offer = get_params(rec_msg)
            re= update_offer(offer)
            if re is not True:
                raise re
        elif rec_msg.startswith('删除offer'):
            # 提取参数部分
            pre_params = rec_msg.strip().split()
            params = pre_params[1:]
            if len(params) == 1:
                re= delete_offer(params[0])
                if re is not True:
                    raise re
            else:
                return "参数格式不正确"

        else:
            return '这不是系统命令哦'

    except Exception as e:
        return '失败：{}'.format(e)
    else:
        return '成功'
    # for key in PATH:
    #     if rec_msg.startswith(key):
    #         if rec_msg.endswith(key):
    #             return PATH[key]
    #         else:
    #             # 提取参数部分
    #             params = rec_msg[len(key):].strip().split()
    #             if len(params) == 2:
    #                 return PATH[key](params[0], params[1])  # 传递参数给 lambda 函数
    #             else:
    #                 return "参数格式不正确"
    # return '这不是系统命令哦'


# create_offer(offer)


# rec_msg = '参数查询 公司=测试公司'
# rec_msg = '创建offer 公司=测试公司 录入人=a0f6d7c0-6e8b-11e9-8f5c-00163e0d1d0f 城市=北京 标题=C++开发工程师'
rec_msg = '更新offer 公司=测试公司 录入人=a0f6d7c0-6e8b-11e9-8f5c-00163e0d1d0f 城市=上海 标题=Java开发工程师 UUID=13d42320-fe40-11ee-85ef-5254008a1b8d'
# rec_msg="删除offer eba69c3c-fedc-11ee-8196-5254008a1b8d"
# rec_msg = '全部offer'
data_str = redirect(rec_msg)
print(data_str)
#
# print(data_str[0])
# for i, info in enumerate(data_str[1].split('),')):
#     print(i, " ", info)
