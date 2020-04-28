#!E:\py_virtual_env\saas_project\Scripts\python.exe
# -*- coding: utf-8 -*-
from django.conf import settings
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from utils.encrypt import uid
import sys
import logging

def create_bucket(buckrt,region='ap-nanjing'):
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    secret_id = 'AKIDMzOXrumGpt2xlJvpumPp0vdDxVjhdvOg'      # 替换为用户的 secretId
    secret_key = 'CAtTZOxIPedcKmCRREm59sL3WUZOGuKT'      # 替换为用户的 secretKey
    region = region     # 替换为用户的 Region
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    # 2. 获取客户端对象
    client = CosS3Client(config)

    response = client.create_bucket(
        Bucket=buckrt,
        ACL='public-read'
    )

def upload_file(request,files_object):
    """
        调用腾讯对象存储
    """
    #h获取文件名后缀
    ext = files_object.name.split('.')[-1]
    #根据用户手机号和文件名后缀生成随机的文件名称，防止上传重复文件
    files_name = "{}.{}".format(uid(request.tracer.user.mobile_phone),ext)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    config = CosConfig(Region=request.tracer.project.region,
                       SecretId=settings.TENCENT_COS_ID,
                       SecretKey=settings.TENCENT_COS_KEY
                       )
    # 2. 获取客户端对象
    client = CosS3Client(config)

    response,url = client.upload_file_from_buffer(
        Body=files_object,  # 文件对象
        Bucket=request.tracer.project.bucket,  # 数据库中保存得桶名称
        Key=files_name,  # 保存的文件名称
    )

    return url
