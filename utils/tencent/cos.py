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

    secret_id = settings.TENCENT_COS_ID      # 替换为用户的 secretId
    secret_key = settings.TENCENT_COS_KEY      # 替换为用户的 secretKey
    region = region     # 替换为用户的 Region
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    # 2. 获取客户端对象
    client = CosS3Client(config)

    client.create_bucket(
        Bucket=buckrt,
        ACL='public-read'
    )

    cors_config = {
        'CORSRule': [
            {
                'AllowedOrigin': '*',
                'AllowedMethod': ['GET', 'PUT', 'HEAD', 'POST', 'DELETE'],
                'AllowedHeader': "*",
                'ExposeHeader': "*",
                'MaxAgeSeconds': 500
            }
        ]
    }
    client.put_bucket_cors(
        Bucket=buckrt,
        CORSConfiguration=cors_config
    )

def upload_file(request,files_object):
    """
        调用腾讯对象存储
    """
    #h获取文件名后缀
    ext = files_object.name.split('.')[-1]
    #根据用户手机号和文件名后缀生成随机的文件名称，防止上传重复文件
    files_name = "{}.{}".format(uid(request.tracer.user.mobile_phone),ext)
    print(files_name)
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

def credential(bucket, region):
    """ 获取cos上传临时凭证 """

    from sts.sts import Sts

    config = {
        # 临时密钥有效时长，单位是秒（30分钟=1800秒）
        'duration_seconds': 5,
        # 固定密钥 id
        'secret_id': settings.TENCENT_COS_ID,
        # 固定密钥 key
        'secret_key': settings.TENCENT_COS_KEY,
        # 换成你的 bucket
        'bucket': bucket,
        # 换成 bucket 所在地区
        'region': region,
        # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
        # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
        'allow_prefix': '*',
        # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
        'allow_actions': [
            # "name/cos:PutObject",
            # 'name/cos:PostObject',
            # 'name/cos:DeleteObject',
            # "name/cos:UploadPart",
            # "name/cos:UploadPartCopy",
            # "name/cos:CompleteMultipartUpload",
            # "name/cos:AbortMultipartUpload",
            "*",
        ],

    }

    sts = Sts(config)
    result_dict = sts.get_credential()
    return result_dict

def delete_file(bucket, region, key):
    config = CosConfig(Region=region, SecretId=settings.TENCENT_COS_ID, SecretKey=settings.TENCENT_COS_KEY)
    client = CosS3Client(config)

    client.delete_object(
        Bucket=bucket,
        Key=key
    )

def delete_file_list(bucket, region, key_list):
    config = CosConfig(Region=region, SecretId=settings.TENCENT_COS_ID, SecretKey=settings.TENCENT_COS_KEY)
    client = CosS3Client(config)
    objects = {
        "Quiet": "true",
        "Object": key_list
    }
    client.delete_objects(
        Bucket=bucket,
        Delete=objects
    )