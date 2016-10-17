# coding=utf-8
from django.db import models
from django.contrib.auth import models as auth_models


class UserInfo(models.Model):
    '''用户信息表'''
    user = models.ForeignKey(auth_models.User)
    nickname = models.CharField(max_length=64, default='')
    reg_time = models.DateTimeField(auto_add_now=True)
    reg_code = models.CharField(max_length=10)
    reg_type = models.SmallIntegerField(max_length=4, default=1)
    reg_ip = models.CharField(max_length=15, default='')
    reg_location = models.CharField(max_length=128, default='')
    invite_code = models.CharField(max_length=10)
    bank_code = models.CharField(max_length=16, default='')
    bank_card = models.CharField(max_length=64, default='')

    # 定义注册类型
    REG_TYPE = {
        1: '自由注册',
        2: '推荐注册'
    }

    def save(self, *args, **kwargs):
        super(UserInfo, self).save(*args, **kwargs)

    class Meta:
        managed = False
        table = 'user_info'


class UserConnection(models.Model):
    '''用户关联表(推荐网络)'''
    parent = models.ForeignKey(auth_models.User)
    user = models.ForeignKey(auth_models.User)
    depth = models.SmallIntegerField(max_length=4, default=0)
    create_time = models.DateTimeField(auto_add_now=True)
    ratio = models.DecimalField(max_digits=7, decimal_places=3, default=0)

    class Meta:
        managed = False
        table = 'user_connection'


class UserBalance(models.Model):
    '''用户账户表'''
    user = models.ForeignKey(auth_models.User)
    cash = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    invite_benifit = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=3, default=0)

    class Meta:
        managed = False
        table = 'user_balance'


class UserRevenue(models.Model):
    '''用户收入流水表'''
    user = models.ForeignKey(auth_models.User)
    revenue_type = models.SmallIntegerField(max_length=4)
    revenue = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    create_time = models.DateTimeField(auto_add_now=True)

    # 定义流水记录类型
    REVENUE_TYPE = {
        1: '充值',
        2: '邀请获利',
        3: '项目收入'
    }

    class Meta:
        managed = False
        table = 'user_revenue'


class UserOplog(models.Model):
    '''用户日志表'''
    user = models.ForeignKey(auth_models.User)
    optype = models.SmallIntegerField(max_length=4)
    content = models.CharField(max_length=1024)
    ip = models.CharField(max_length=15, default='')
    location = models.CharField(max_length=128, default='')
    create_time = models.DateTimeField(auto_add_now=True)

    # 定义操作类型
    OPTYPE = {
        1: '登陆',
        2: '退出',
        3: '转介',
        4: '购买下线',
        5: '选择上线',
        6: '充值',
        7: '发信',
        8: '读信'
    }

    class Meta:
        managed = False
        table = 'user_oplog'


class Bank(models.Model):
    '''银行配置表'''
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=32)

    class Meta:
        managed = False
        table = 'bank'


class UserPayment(models.Model):
    '''用户充值记录表'''
    user = models.ForeignKey(auth_models.User)
    order_id = models.CharField(max_length=32)
    pay_type = models.SmallIntegerField(max_length=4)
    payout = models.DecimalField(max_digits=14, decimal_places=3)
    account = models.CharField(max_length=64, default='')
    bank = models.ForeignKey(Bank)
    bank_card = models.CharField(max_length=64, default='')
    ip = models.CharField(max_length=15, default='')
    location = models.CharField(max_length=128, default='')
    create_time = models.DateTimeField(auto_add_now=True)

    # 定义充值类型
    PAY_TYPE = {
        1: '银行卡/信用卡',
        2: 'Paypal'
    }

    class Meta:
        managed = False
        table = 'user_payment'


class UserMessage(models.Model):
    '''用户信箱'''
    from_user = models.ForeignKey(auth_models.User)
    to_user = models.ForeignKey(auth_models.User)
    content = models.CharField(max_length=1024)
    status = models.SmallIntegerField(max_length=4)
    create_time = models.DateTimeField(auto_add_now=True)
    read_time = models.DateTimeField()

    # 定义状态
    STATUS = {
        0: '未读',
        1: '已读'
    }

    class Meta:
        managed = False
        table = 'user_message'


class NewsCategory(models.Model):
    '''新闻资讯分类表'''
    name = models.CharField(max_length=1024)
    status = models.SmallIntegerField(max_length=4, default=1)
    create_time = models.DateTimeField(auto_add_now=True)

    # 定义状态
    STATUS = {
        1: '正常',
        2: '删除'
    }

    class Meta:
        managed = False
        table = 'news_category'


class News(models.Model):
    '''新闻资讯表'''
    category = models.ForeignKey(NewsCategory)
    publisher = models.ForeignKey(auth_models.User)
    title = models.CharField(max_length=1024)
    content = models.TextField()
    status = models.SmallIntegerField(max_length=4, default=1)
    create_time = models.DateTimeField(auto_add_now=True)

    # 定义状态
    STATUS = {
        1: '正常',
        2: '删除'
    }

    class Meta:
        managed = False
        table = 'news'


class Statics(models.Model):
    '''配置表之首页数据'''
    members = models.IntegerField()
    onlines = models.IntegerField()
    hits = models.IntegerField()
    total_paid = models.DecimalField(max_digit=14, decimal_places=3)
    offers = models.IntegerField()
    pts_value = models.IntegerField()
    ptc_value = models.IntegerField()
    create_time = models.DateTimeField()

    class Meta:
        managed = False
        table = 'statics'


class InviteCode(models.Model):
    '''注册邀请码表'''
    category = models.ForeignKey(NewsCategory)
    publisher = models.ForeignKey(auth_models.User)
    title = models.CharField(max_length=1024)
    content = models.TextField()
    status = models.SmallIntegerField(max_length=4, default=1)
    create_time = models.DateTimeField(auto_add_now=True)

    # 定义状态
    STATUS = {
        0: '未使用',
        1: '已使用'
    }

    class Meta:
        managed = False
        table = 'invite_code'
