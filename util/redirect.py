from db_old import *

# 定义参数映射字典
offer_param_mapping = {
    '公司': 'company_name',
    '录入人': 'company_uuid',
    '城市': 'recruit_city',
    '标题': 'recruit_title',
    'UUID': 'uuid'
}


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
            re = create_offer(offer)
            if re is not True:
                raise re
        elif rec_msg.startswith('更新offer'):
            # 提取参数部分
            offer = get_params(rec_msg)
            re = update_offer(offer)
            if re is not True:
                raise re
        elif rec_msg.startswith('删除offer'):
            # 提取参数部分
            pre_params = rec_msg.strip().split()
            params = pre_params[1:]
            if len(params) == 1:
                re = delete_offer(params[0])
                if re is not True:
                    raise re
            else:
                return "参数格式不正确"

        else:
            rep_msg = "这不是系统指令" \
                      "回复以下关键字获取相关信息\n" \
                      "1.全部offer：获取所有offer信息，超过十条时只显示十条\n" \
                      "2.参数查询：获取符合条件的offer信息\n" \
                      "   示例：参数查询 公司=字节跳动\n" \
                      "3.创建offer：创建offer信息\n" \
                      "   示例：创建offer 公司=字节跳动 公司ID=1 城市=北京 职位=Java开发工程师 UUID=1\n" \
                      "4.更新offer：更新offer信息\n" \
                      "   示例：更新offer 公司=字节跳动 公司ID=1 城市=北京 职位=Java开发工程师 UUID=1\n" \
                      "5.删除offer：删除offer信息,后跟uuid\n" \
                      "   示例：删除offer 1\n"
            return rep_msg


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
