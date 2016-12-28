# coding=utf-8
from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth import models as auth_models
from redactor.fields import RedactorField


class StaticsQuerySet(models.QuerySet):

    def member_counter(self):
        q = self.order_by('-id').first()
        q.members += 1
        q.online += 1
        q.save()
        return True


class Statics(models.Model):
    '''配置表之首页数据'''
    members = models.IntegerField()
    online = models.IntegerField()
    hits = models.IntegerField()
    total_paid = models.DecimalField(max_digits=14, decimal_places=3)
    offers = models.DecimalField(max_digits=14, decimal_places=3)
    pts_value = models.DecimalField(max_digits=10, decimal_places=3)
    ptc_value = models.DecimalField(max_digits=10, decimal_places=3)
    create_time = models.DateTimeField(auto_now_add=True)

    objects = StaticsQuerySet.as_manager()

    class Meta:
        managed = False
        db_table = 'statics'

    def counter(self):
        q = self.objects.order_by('-id').first()
        q.members += 1
        q.save()


class SiteSetting(models.Model):
    '''网站其他配置表'''
    user_buy_price = models.DecimalField(max_digits=14, decimal_places=3)
    bonus_50 = models.IntegerField(default=0)
    bonus_100 = models.IntegerField(default=0)
    bonus_200 = models.IntegerField(default=0)
    bonus_400 = models.IntegerField(default=0)
    bonus_600 = models.IntegerField(default=0)
    bonus_800 = models.IntegerField(default=0)
    bonus_1000 = models.IntegerField(default=0)
    bonus_2000 = models.IntegerField(default=0)
    bonus_times = models.IntegerField(default=3)

    class Meta:
        managed = False
        db_table = 'site_setting'


class InviteCodeQuerySet(models.QuerySet):

    def pop(self):
        q = self.filter(status=0).order_by('-id').first()
        q.status = 1
        q.update_time = datetime.now()
        q.save()
        return q.code


class InviteCode(models.Model):
    '''注册邀请码表'''
    code = models.CharField(max_length=15)
    status = models.SmallIntegerField(max_length=4, default=1)
    update_time = models.DateTimeField()

    objects = InviteCodeQuerySet.as_manager()
    # 定义状态
    STATUS = {
        0: '未使用',
        1: '已使用'
    }

    class Meta:
        managed = False
        db_table = 'invite_code'


class UserInfo(models.Model):
    '''用户信息表'''
    user = models.ForeignKey(auth_models.User)
    phone_number = models.CharField(max_length=64, default='')
    address1 = models.CharField(max_length=256, default='')
    address2 = models.CharField(max_length=256, default='')
    city = models.CharField(max_length=64, default='')
    provincy = models.CharField(max_length=128, default='')
    country = models.CharField(max_length=128, default='')
    zip_code = models.CharField(max_length=32, default='')
    sexal = models.CharField(max_length=32, default='')
    age = models.CharField(max_length=32, default='')
    recommend_user = models.CharField(max_length=64, default='')
    reg_time = models.DateTimeField(auto_now_add=True)
    reg_code = models.CharField(max_length=10)
    reg_type = models.SmallIntegerField(max_length=4, default=1)
    reg_ip = models.CharField(max_length=15, default='')
    reg_location = models.CharField(max_length=128, default='')
    invite_code = models.CharField(max_length=10)
    bank_code = models.CharField(max_length=16, default='')
    bank_card = models.CharField(max_length=64, default='')
    status = models.SmallIntegerField(default=1)

    # 定义注册类型
    REG_TYPE = {
        1: '自由注册',
        2: '推荐注册'
    }

    # 用户状态
    STATUS = {
        0: '不可用',
        1: '正常'
    }

    # 用户角色
    ROLE = {
        0: '普通用户',
        1: '后台管理员'
    }

    def save(self, *args, **kwargs):
        self.invite_code = InviteCode.objects.pop()
        super(UserInfo, self).save(*args, **kwargs)

        Statics.objects.member_counter()

    class Meta:
        managed = False
        db_table = 'user_info'


class UserConnection(models.Model):
    '''用户关联表(推荐网络)'''
    parent = models.ForeignKey(auth_models.User)
    user = models.ForeignKey(auth_models.User)
    depth = models.SmallIntegerField(max_length=4, default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    ratio = models.DecimalField(max_digits=7, decimal_places=3, default=0)
    is_selling = models.SmallIntegerField(default=0)

    IS_SELLING = {
        0: '不在下线大厅',
        1: '在下线大厅'
    }

    class Meta:
        managed = False
        db_table = 'user_connection'


class UserConnectionBuying(models.Model):
    '''用户关联表(购买下线)'''
    parent = models.ForeignKey(auth_models.User)
    user = models.ForeignKey(auth_models.User)
    create_time = models.DateTimeField(auto_now_add=True)
    ratio = models.DecimalField(max_digits=7, decimal_places=3, default=0)

    class Meta:
        managed = False
        db_table = 'user_connection_buying'


class UserChangeRecommend(models.Model):
    '''用户转介表'''
    user = models.ForeignKey(auth_models.User)
    recommend_user = models.ForeignKey(auth_models.User)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'user_change_recommend'


class UserBalance(models.Model):
    '''用户账户表'''
    user = models.ForeignKey(auth_models.User)
    cash = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    invite_benifit = models.DecimalField(max_digits=14,
                                         decimal_places=3,
                                         default=0)
    total = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    point = models.IntegerField(default=0)
    update_time = models.DateTimeField(auto_now_add=True)
    revenue_promote = models.DecimalField(max_digits=14,
                                          decimal_places=3,
                                          default=0)
    total_investment = models.DecimalField(max_digits=14,
                                           decimal_places=3,
                                           default=0)

    class Meta:
        managed = False
        db_table = 'user_balance'


class UserRevenue(models.Model):
    '''用户收入流水表'''
    user = models.ForeignKey(auth_models.User)
    parent_user_id = models.IntegerField()
    revenue_type = models.SmallIntegerField(max_length=4)
    revenue = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    # 定义流水记录类型
    REVENUE_TYPE = {
        1: '充值',
        2: '邀请获利',
        3: '项目收入'
    }

    class Meta:
        managed = False
        db_table = 'user_revenue'


class UserOplog(models.Model):
    '''用户日志表'''
    user = models.ForeignKey(auth_models.User)
    optype = models.SmallIntegerField(max_length=4)
    content = models.CharField(max_length=1024)
    ip = models.CharField(max_length=15, default='')
    location = models.CharField(max_length=128, default='')
    create_time = models.DateTimeField(auto_now_add=True)

    # 定义操作类型
    OPTYPE = {
        1: '登陆',
        2: '退出',
        3: '转介',
        4: '购买下线',
        5: '选择上线',
        6: '充值',
        7: '发信',
        8: '读信',
        9: '认购抽奖'
    }

    OPTYPE_CODES = {
        'login': 1
    }

    class Meta:
        managed = False
        db_table = 'user_oplog'


class Bank(models.Model):
    '''银行配置表'''
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'bank'


class UserPayment(models.Model):
    '''用户充值记录表'''
    user = models.ForeignKey(auth_models.User)
    order_id = models.CharField(max_length=32)
    pay_type = models.SmallIntegerField(max_length=4)
    payout = models.DecimalField(max_digits=14, decimal_places=3)
    account = models.CharField(max_length=64, default='')
    bank_id = models.IntegerField()
    bank_card = models.CharField(max_length=64, default='')
    ip = models.CharField(max_length=15, default='')
    location = models.CharField(max_length=128, default='')
    create_time = models.DateTimeField(auto_now_add=True)

    # 定义充值类型
    PAY_TYPE = {
        1: '银行卡/信用卡',
        2: 'Paypal'
    }

    class Meta:
        managed = False
        db_table = 'user_payment'


class UserMessage(models.Model):
    '''用户信箱'''
    from_user = models.ForeignKey(auth_models.User)
    to_user = models.ForeignKey(auth_models.User)
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=1024)
    status = models.SmallIntegerField(max_length=4)
    create_time = models.DateTimeField(auto_now_add=True)
    read_time = models.DateTimeField()

    # 定义状态
    STATUS = {
        0: '未读',
        1: '已读'
    }

    class Meta:
        managed = False
        db_table = 'user_message'


class UserFeedback(models.Model):
    '''用户反馈'''
    user = models.ForeignKey(auth_models.User)
    ctype = models.SmallIntegerField(max_length=4)
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=1024)
    status = models.SmallIntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    # 定义状态
    STATUS = {
        0: '已发送',
        1: '已解决'
    }

    # 定义状态
    CTYPE = {
        1: '类型一',
        2: '类型二'
    }

    class Meta:
        managed = False
        db_table = 'user_feedback'


class UserPromoteRank(models.Model):
    '''用户信箱'''
    user = models.ForeignKey(auth_models.User)
    recommend_users = models.IntegerField(default=0)
    commission = models.DecimalField(max_digits=14, decimal_places=2)
    reward = models.DecimalField(max_digits=14, decimal_places=2)
    season = models.SmallIntegerField(default=0)
    season_date = models.DateField(auto_now_add=True)

    # 定义状态
    STATUS = {
        0: '未读',
        1: '已读'
    }

    class Meta:
        managed = False
        db_table = 'user_promote_rank'


class UserSellingMall(models.Model):
    '''下线购买大厅'''
    user = models.ForeignKey(auth_models.User)
    parent_user = models.ForeignKey(auth_models.User)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'user_selling_mall'


class UserWithDraw(models.Model):
    '''会员提款'''
    user = models.ForeignKey(auth_models.User)
    order_id = models.CharField(max_length=32)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    pay_type = models.SmallIntegerField(default=0)
    pay_account = models.CharField(max_length=128)
    status = models.SmallIntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField()

    PAY_TYPE = {
        1: '支付宝',
        2: '银行卡'
    }

    STATUS = {
        0: '申请中',
        1: '申请成功',
        2: '申请失败'
    }

    def save(self, *args, **kwargs):
        self.order_id = self.gen_id()
        super(UserWithDraw, self).save(*args, **kwargs)

    def gen_id(self):
        applicant_time = timezone.now()
        active_on = applicant_time.date()
        next_day = active_on + timezone.timedelta(days=1)
        total = UserWithDraw.objects \
            .filter(create_time__range=(active_on, next_day)) \
            .count()
        order_id = int(active_on.strftime("%Y%m%d") + '0000') + total + 1
        return order_id

    class Meta:
        managed = False
        db_table = 'user_withdraw'


class UserBonus(models.Model):
    '''会员认购抽奖记录'''
    user = models.ForeignKey(auth_models.User)
    point = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.SmallIntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    STATUS = {
        0: '未充值',
        1: '充值成功'
    }

    class Meta:
        managed = False
        db_table = 'user_bonus'


class NewsCategory(models.Model):
    '''新闻资讯分类表'''
    name = models.CharField(max_length=1024)
    status = models.SmallIntegerField(max_length=4, default=1)
    create_time = models.DateTimeField(auto_now_add=True)

    # 定义状态
    STATUS = {
        1: '正常',
        2: '删除'
    }

    def __str__(self):
        return self.name.encode('utf-8')

    class Meta:
        managed = False
        db_table = 'news_category'


class News(models.Model):
    '''新闻资讯表'''
    category = models.ForeignKey(NewsCategory)
    # publisher = models.ForeignKey(auth_models.User)
    title = models.CharField(max_length=1024)
    content = RedactorField()
    status = models.SmallIntegerField(max_length=4, default=1)
    create_time = models.DateTimeField(auto_now_add=True)

    # 定义状态
    STATUS = {
        1: '正常',
        2: '删除'
    }

    class Meta:
        managed = False
        db_table = 'news'


class Projects(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.IntegerField()
    status = models.SmallIntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    # 定义状态
    STATUS = {
        1: '正常',
        2: '删除'
    }

    class Meta:
        managed = False
        db_table = 'project'


class CBDCPriceLog(models.Model):
    '''资本兑历史价格表'''
    buy = models.DecimalField(max_digits=14, decimal_places=2)
    sell = models.DecimalField(max_digits=14, decimal_places=2)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'CBCD_price_log'
