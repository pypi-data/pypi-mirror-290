# -*- coding: UTF-8 -*-
# @Time : 2024/8/14 23:58 
# @Author : 刘洪波
import hashlib
import base64
import random


def insert_middle(str1, str2):
    length = min(len(str1), len(str2))
    result = [str1[i] + str2[i] for i in range(length)]
    result.append(str1[length:])
    result.append(str2[length:])
    return ''.join(result)


def insert_front(str1, str2): return str2 + str1


def insert_after(str1, str2): return str1 + str2


merge_algorithm_dict = {
    'insert_middle': insert_middle,
    'insert_front': insert_front,
    'insert_after': insert_after
}


def merge_str(str1, str2, algorithm: str = 'insert_middle') -> str:
    if str1 and str2 and algorithm:
        if algorithm in merge_algorithm_dict:
            return eval(algorithm)(str1, str2)
        else:
            raise ValueError('Error: The input parameter algorithm is incorrect!')
    else:
        raise ValueError('Error: Input parameter error, please check!')


def generate_sign(key: str, timestamp: str, algorithm: str = None):
    """
    生成sign
    :param key: 生成签名所需密钥
    :param timestamp: 时间戳
    :param algorithm: 生成签名方式
    :return:
    """
    if not algorithm:
        algorithm = random.choice(list(merge_algorithm_dict.keys()))
    _key = merge_str(key, timestamp, algorithm)
    hash_object = hashlib.sha256()
    hash_object.update(_key.encode())
    return algorithm, hash_object.hexdigest()


def generate_fused_sign(key: str, timestamp: str, algorithm: str = None, user_id: str = None):
    """
    生成融合的签名，签名里包含 时间戳 或 用户ID
    :param key: 生成签名所需密钥
    :param timestamp: 时间戳
    :param algorithm: 生成签名方式
    :param user_id: 用户ID
    :return:
    """
    algorithm, sign = generate_sign(key, timestamp, algorithm)
    content = algorithm + '###' + sign
    if user_id:
        content += '###' + user_id
    return base64.b64encode(content.encode()).decode('utf-8')


def parse_sign(sign: str):
    """
    解析签名
    :param sign: 签名
    :return:
    """
    sign_info = {}
    if sign:
        new_sign = base64.b64decode(sign).decode('utf-8')
        if '###' in new_sign:
            new_sign = new_sign.split('###')
            if len(new_sign) > 1:
                sign_info['algorithm'] = new_sign[0]
                sign_info['sign'] = new_sign[1]
            if len(new_sign) > 2:
                sign_info['user_id'] = '###'.join(new_sign[2:])
    return sign_info
