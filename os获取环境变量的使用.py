import os

from dotenv import find_dotenv,load_dotenv
# 查找dotenv的配置文件
find_dotenv('.env')
# 读取并临时写入环境变量
load_dotenv()
# 获取环境变量
name = os.environ.get('hello')

print(name)