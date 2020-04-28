#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-

"""
腾讯sdk ： 创建桶和上传文件

"""

# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = 'AKIDMzOXrumGpt2xlJvpumPp0vdDxVjhdvOg'      # 替换为用户的 secretId
secret_key = 'CAtTZOxIPedcKmCRREm59sL3WUZOGuKT'      # 替换为用户的 secretKey
region = 'ap-nanjing'     # 替换为用户的 Region
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
# 2. 获取客户端对象
client = CosS3Client(config)

response = client.create_bucket(
    Bucket='mahongda2211-1258040712',
    ACL='public-read'
)

# response = client.upload_file(
#     Bucket='mahongda2211-1258040712',
#     LocalFilePath='Python后端开发_马洪达.pdf',
#     Key='Python后端开发_马洪达.pdf',
# )
# print(response['ETag'])