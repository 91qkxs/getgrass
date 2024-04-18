import asyncio
import hashlib
import json
import random
import secrets
import string
import time
import os
import uuid
from datetime import datetime, timezone, timedelta
from enum import Enum
from http import HTTPStatus
from typing import Optional

from loguru import logger



class DELAY2(Enum):
    account = (2, 3)  # 不同帐户之间的秒数延迟
    chain = (2, 3)  # 不同帐户之间的秒数延迟

last_sequence = -1


def countdown_timer(seconds):
    for remaining in range(seconds, 0, -1):
        print(f"\r当前线程休眠，剩余: {remaining} 秒", end='', flush=True)
        time.sleep(1)
    print("\r线程休眠结束，准备下一步操作            ")


def sleep(key):
    rs = random.randint(key[0], key[1])
    logger.info(f"线程休眠等待 {rs} 秒")
    time.sleep(rs)


def print_wallet_address(wallet_address):
    address = wallet_address[:4] + "****" + wallet_address[-5:]
    return address


def read_wallets_from_file(file_path):
    wallets = []
    with open(file_path, 'r') as file:
        for line in file:
            address, private_key = line.strip().split(',')
            wallets.append({'address': address, 'private_key': private_key})
    return wallets


def print_wallet_address_sol(input_string):
    if len(input_string) <= 7:
        return input_string
    else:
        visible_prefix = input_string[:3]
        visible_suffix = input_string[-4:]
        masked_middle = '*' * (len(input_string) - 7)
        masked_string = visible_prefix + masked_middle + visible_suffix
        return masked_string


def read_wallets_from_files(file_names, current_directory, *directories):
    wallets = []
    for file_path in file_names:
        file_name = os.path.join(current_directory, *directories, file_path)
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                address, private_key, proxy_ip = line.strip().split(',')
                wallets.append(
                    {'address': address, 'private_key': private_key, 'proxy_ip': proxy_ip})
    return wallets

def read_users_from_files(file_names, current_directory, *directories):
    wallets = []
    for file_path in file_names:
        file_name = os.path.join(current_directory, *directories, file_path)
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                address, proxy_ip = line.strip().split(',')
                wallets.append(
                    {'user': address ,'proxy_ip': proxy_ip})
    return wallets


def read_wallets(file_names, current_directory, *directories):
    wallets = []
    for file_path in file_names:
        file_name = os.path.join(current_directory, *directories, file_path)
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                address, private_key = line.strip().split(',')
                wallets.append(
                    {'address': address, 'private_key': private_key})
    return wallets


def string_in_file(target_string, file_names, current_directory, *directories):
    for file_path in file_names:
        file_name = os.path.join(current_directory, *directories, file_path)
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                for line in file:
                    if target_string in line:
                        return True
        except FileNotFoundError:
            print(f"File {file_name} not found.")
    return False


def get_random_line(filename, current_directory, *directories):
    file_name = os.path.join(current_directory, *directories, filename)
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        if lines:
            return random.choice(lines)
        else:
            return None


def read_wallets_twitter_from_files(file_names, current_directory, *directories):
    wallets = []
    for file_path in file_names:
        file_name = os.path.join(current_directory, *directories, file_path)
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                print("当前随机钱包", line)
                address, private_key, tw_token, ip_proxy = line.strip().split(',')
                wallets.append(
                    {'address': address, 'private_key': private_key, 'tw_token': tw_token, 'ip_proxy': ip_proxy})
    return wallets


def generate_random_string(length):
    num_bytes = length // 2  # 一个十六进制字符对应4位二进制，所以需要length//2个字节
    random_bytes = secrets.token_bytes(num_bytes)  # 生成安全的随机字节
    random_string = random_bytes.hex()[:length]  # 将随机字节转换为十六进制表示并取前length位
    return random_string


def generate_random_float(min_value, max_value, decimal_places):
    # 生成一个指定范围内的随机浮点数
    random_value = random.uniform(min_value, max_value)

    # 四舍五入到指定的小数位数
    rounded_float = round(random_value, decimal_places)

    # 格式化为字符串
    number_str = "{:.{}f}".format(random_value, decimal_places)
    logger.info(f"随机生成金额: {number_str}")
    return rounded_float


def fmt_float(price, decimal_places):
    # 生成一个指定范围内的随机浮点数
    # 四舍五入到指定的小数位数
    rounded_float = round(price, decimal_places)

    # 格式化为字符串
    number_str = "{:.{}f}".format(rounded_float, decimal_places)
    logger.info(f"格式化金额: {number_str}")
    return rounded_float, number_str


def load_abi(file_name, current_directory, *directories, encoding: Optional[str] = None) :
    path = os.path.join(current_directory, *directories, file_name)
    return json.load(open(path, encoding=encoding))


def read_json(path: str, encoding: Optional[str] = None):
    return json.load(open(path, encoding=encoding))


def generate_custom_id():
    global last_sequence

    timestamp = int(time.time() * 1000)  # 获取当前时间戳（毫秒）
    worker_id = random.randint(0, 1023)  # 生成一个随机的工作节点 ID（0-1023）

    # 生成一个不等于上一个序列号的随机序列号
    sequence = random.randint(0, 4095)
    while sequence == last_sequence:
        sequence = random.randint(0, 4095)

    last_sequence = sequence

    prefix = random.randint(17, 57)  # 生成一个17到57之间的随机前缀

    # 打乱序列号
    sequence_list = list(str(sequence))
    random.shuffle(sequence_list)
    shuffled_sequence = int(''.join(sequence_list))

    # 构造雪花 ID
    snowflake_id = ((prefix * 10 ** 16) | (timestamp % 10 ** 16) << 12 | worker_id << 2 | shuffled_sequence)
    snowflake_id_str = '{:018d}'.format(snowflake_id)  # 将雪花 ID 转换为 18 位字符串

    return snowflake_id_str

def write_to_file(filename, data, *directories):
        file_path = os.path.join(*directories, filename)
        # Check if data is already in the file
        if data in open(file_path, 'r', encoding='utf-8').read():
            print("已经存在跳过")
        else:
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(data + '\n')
                print("已经写入email.txt")

def convert_beijing_to_utc():
    # 获取当前北京时间
    beijing_time = datetime.now(timezone(timedelta(hours=8)))

    # 将北京时间转换为UTC时间
    utc_time = beijing_time.astimezone(timezone.utc)

    # 格式化为ISO 8601字符串
    iso_string = utc_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    return iso_string


def generate_moca_id():
    # 生成长度在5到20之间的随机整数作为Moca ID的长度
    id_length = random.randint(5, 9)

    # 生成包含大小写字母和数字的可选字符集合
    characters = string.ascii_letters + string.digits

    # 从可选字符集合中随机选择字符生成Moca ID
    moca_id = ''.join(random.choices(characters, k=id_length))

    return moca_id


def to_md5(input_string):
    # 创建一个 hashlib.md5 对象
    hash_object = hashlib.md5()

    # 更新对象的状态，添加要计算散列值的数据
    hash_object.update(input_string.encode('utf-8'))

    # 获取 MD5 散列值的十六进制表示
    md5_hash = hash_object.hexdigest()

    return md5_hash
# 示例用法
if __name__ == "__main__":
    generated_id = generate_moca_id()
    print("Generated ID:", generated_id)


