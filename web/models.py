from django.db import models

# Create your models here.

class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名',max_length=32)
    email = models.EmailField(verbose_name='邮箱',max_length=32)
    mobile_phone = models.CharField(verbose_name='手机号',max_length=32)
    password = models.CharField(verbose_name='密码',max_length=32)

class PricePoliy(models.Model):
    """价格策略"""
    category_choices =(
        (1,'免费版'),
        (2,'收费版'),
        (3,'其他')
    )
    category = models.SmallIntegerField(verbose_name="收费类型",default=2,choices=category_choices)
    title = models.CharField(verbose_name='标题',max_length=10)
    #PositiveIntegerField：正整数类型
    price = models.PositiveIntegerField(verbose_name='价格')

    project_num = models.PositiveIntegerField(verbose_name='项目数')
    project_member = models.PositiveIntegerField(verbose_name='项目成员数')
    project_space = models.PositiveIntegerField(verbose_name='单项目空间')
    per_file_size = models.PositiveIntegerField(verbose_name='单项目大小（M）')
    creation_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)

class Transaction(models.Model):
    """交易记录"""
    status_choices = (
        (1,'未支付'),
        (2,'已支付')
    )
    status = models.SmallIntegerField(verbose_name="订单状态",choices=status_choices)
    order = models.CharField(verbose_name='订单号',max_length=64,unique=True)
    user = models.ForeignKey(verbose_name='用户',to="UserInfo")
    price_poliy = models.ForeignKey(verbose_name='价格策略',to='PricePoliy')
    count = models.IntegerField(verbose_name='数量（年）',help_text='0表示无限期')
    price = models.IntegerField(verbose_name='实际支付价格')
    #blank 表示此处可以不填
    start_datetime = models.DateTimeField(verbose_name='开始时间',null=True,blank=True)
    end_datetime = models.DateTimeField(verbose_name='结束时间',null=True,blank=True)
    creation_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

class Project(models.Model):
    """项目表"""
    COLOR_CHOICES = (
        (1,'#56b8eb'),  #56b8eb
        (2,'#f28033'),  #f28033
        (3,'#ebc656'),  #ebc656
        (4,'#a2d148'),  #a2d148
        (5,'#20BFA4'),  #20BFA4
        (6,'#7461c2'),  #7461c2
        (7,'#7461c2'),  #7461c2
    )
    name = models.CharField(verbose_name='项目名称',max_length=64)
    color = models.SmallIntegerField(verbose_name='颜色',choices=COLOR_CHOICES,default=1)
    desc = models.CharField(verbose_name='项目描述',max_length=255,null=True,blank=True)
    use_space = models.IntegerField(verbose_name='项目已经使用空间',default=0)
    star = models.BooleanField(verbose_name='星标',default=False)
    join_count = models.SmallIntegerField(verbose_name='参与人数',default=1)
    creator = models.ForeignKey(verbose_name='创建者',to='UserInfo')
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    bucket = models.CharField(verbose_name='cos桶',max_length=128)
    region = models.CharField(verbose_name='cos区域',max_length=128)

class ProjectUser(models.Model):
    """项目参与者"""
    user = models.ForeignKey(verbose_name='用户',to='UserInfo')
    project = models.ForeignKey(verbose_name='项目名称',to='Project')
    star = models.BooleanField(verbose_name='星标',default=False)
    join_datetime = models.DateTimeField(verbose_name='加入时间', auto_now_add=True)

class Wiki(models.Model):
    project = models.ForeignKey(verbose_name='项目',to='Project')
    title = models.CharField(verbose_name='标题',max_length=32)
    content = models.TextField(verbose_name='内容')
    depth = models.IntegerField(verbose_name='深度',default=1)
    #子关联
    parent = models.ForeignKey(verbose_name='父文章',to='self',null=True, blank=True,related_name='children')

class FileRepository(models.Model):
    """  文件库  """
    project = models.ForeignKey(verbose_name="项目名称",to='project')
    file_type_choices = (
        (1,"文件"),
        (2,"文件夹"),
    )
    file_type = models.SmallIntegerField(verbose_name="类型",choices=file_type_choices)
    name = models.CharField(verbose_name="文件夹名称",max_length=64,help_text="文件/文件夹")
    key = models.CharField(verbose_name="文件存储存在COS中的KEY",max_length=128,null=True)
    file_size = models.IntegerField(verbose_name="文件大小",null=True,blank=True)
    file_path = models.CharField(verbose_name="文件路径",max_length=255,null=True,blank=True)
    parent = models.ForeignKey(verbose_name="父目录",to="self",related_name="child",null=True,blank=True)
    update_user = models.ForeignKey(verbose_name="最近更新者",to="UserInfo")
    update_time = models.DateTimeField(verbose_name="最近更新的时间",auto_now=True)

