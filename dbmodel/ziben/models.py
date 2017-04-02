# coding=utf-8
import uuid
import time
from datetime import datetime, timedelta
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
    bonus_switch = models.IntegerField(default=0)
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
    status = models.SmallIntegerField(default=1)
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
    pwd = models.CharField(max_length=32, default='')
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
    reg_type = models.SmallIntegerField(default=1)
    reg_ip = models.CharField(max_length=15, default='')
    reg_location = models.CharField(max_length=128, default='')
    invite_code = models.CharField(max_length=10)
    bank_code = models.CharField(max_length=16, default='')
    bank_card = models.CharField(max_length=64, default='')
    status = models.SmallIntegerField(default=1)
    member_area = models.CharField(max_length=64, default='left')

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
        if not self.invite_code:
            self.invite_code = InviteCode.objects.pop()
        super(UserInfo, self).save(*args, **kwargs)

        Statics.objects.member_counter()

    class Meta:
        managed = False
        db_table = 'user_info'


class UserConnection(models.Model):
    '''用户关联表(推荐网络)'''
    parent = models.ForeignKey(auth_models.User, related_name="parent_id")
    user = models.ForeignKey(auth_models.User)
    depth = models.SmallIntegerField(default=0)
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
    parent = models.ForeignKey(auth_models.User, related_name="bparent_id")
    user = models.ForeignKey(auth_models.User)
    create_time = models.DateTimeField(auto_now_add=True)
    ratio = models.DecimalField(max_digits=7, decimal_places=3, default=0)

    class Meta:
        managed = False
        db_table = 'user_connection_buying'


class UserChangeRecommend(models.Model):
    '''用户转介表'''
    user = models.ForeignKey(auth_models.User)
    recommend_user = models.ForeignKey(auth_models.User, related_name="recommend_user_id")
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
    revenue_type = models.SmallIntegerField()
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
    optype = models.SmallIntegerField()
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
    order_id = models.CharField(max_length=64)
    partner_order_id = models.CharField(max_length=64)
    user = models.ForeignKey(auth_models.User)
    pay_type = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.SmallIntegerField(default=1)
    point = models.IntegerField(default=0)
    remark = models.CharField(max_length=1024, default='')
    params = models.CharField(max_length=1024, default='')
    status = models.SmallIntegerField(default=0)
    create_at= models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField()
    ip = models.CharField(max_length=15, default='')
    location = models.CharField(max_length=128, default='')
    request_url = models.CharField(max_length=1024)
    resp_code = models.CharField(max_length=64)
    callback = models.CharField(max_length=256, default='')

    STATUS = {
        0: '付款中',
        1: '充值成功',
        -1: '充值失败'
    }

    RESP_CODE = {
        -1: '订单号错误',
        0: '交易失败',
        5: '同一IP重复',
        8: '同一COOKIE重复交易',
        10: '不存在该商户号',
        11: 'MD5KEYi不存在',
        13: '交易网址未注册',
        14: 'MD5验签失败',
        15: '商户未开通',
        16: '通道未开通',
        22: '返回地址未绑定',
        24: '交易流水号重复',
        25: '订单金额有误',
        26: '当天金额超过限制',
        30: '待处理',
        88: '付款成功'
    }

    def save(self, *args, **kwargs):
        self.order_id = self.gen_id()
        super(UserPayment, self).save(*args, **kwargs)

    def gen_id(self):
        applicant_time = timezone.now()
        active_on = applicant_time.date()
        next_day = active_on + timezone.timedelta(days=1)
        total = UserPayment.objects \
            .filter(create_at__range=(active_on, next_day)) \
            .count()
        order_id = str(int(active_on.strftime("%Y%m%d") + '000000') + total + 1) + '-'+ str(int(time.time()*1000))
        return order_id

    class Meta:
        managed = False
        db_table = 'user_payment'


class UserMessage(models.Model):
    '''用户信箱'''
    from_user = models.ForeignKey(auth_models.User, related_name="to_user_id")
    to_user = models.ForeignKey(auth_models.User, related_name="from_user_id")
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=1024)
    status = models.SmallIntegerField()
    ctype = models.CharField(max_length=32, default='member')
    create_time = models.DateTimeField(auto_now_add=True)
    read_time = models.DateTimeField()

    # 定义状态
    STATUS = {
        0: '未读',
        1: '已读',
        2: '已回复'
    }

    class Meta:
        managed = False
        db_table = 'user_message'


class UserFeedback(models.Model):
    '''用户反馈'''
    user = models.ForeignKey(auth_models.User)
    ctype = models.SmallIntegerField()
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
    parent_user = models.ForeignKey(auth_models.User, related_name="parent_user_id")
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'user_selling_mall'


class UserWithDraw(models.Model):
    '''会员提款'''
    user = models.ForeignKey(auth_models.User)
    order_id = models.CharField(max_length=32)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    pay_type = models.CharField(max_length=128)
    bank_code = models.CharField(max_length=128)
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


class UserOrderSell(models.Model):
    '''会员挂单记录'''
    seller_user = models.ForeignKey(auth_models.User)
    order_id = models.CharField(max_length=64)
    num = models.IntegerField()
    num_unsell = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.SmallIntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    STATUS = {
        0: '挂单中',
        1: '已结单',
    }

    def save(self, *args, **kwargs):
        self.order_id = self.gen_id()
        super(UserOrderSell, self).save(*args, **kwargs)

    def gen_id(self):
        applicant_time = timezone.now()
        active_on = applicant_time.date()
        next_day = active_on + timezone.timedelta(days=1)
        total = UserOrderSell.objects \
            .filter(create_at__range=(active_on, next_day)) \
            .count()
        order_id = int(active_on.strftime("%Y%m%d") + '0000') + total + 1
        return order_id

    class Meta:
        managed = False
        db_table = 'user_order_sell'


class UserOrderBuy(models.Model):
    '''会员买入'''
    buyer_user = models.ForeignKey(auth_models.User)
    order_id = models.CharField(max_length=64)
    seller_order_id = models.CharField(max_length=64)
    num = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        self.order_id = self.gen_id()
        super(UserOrderBuy, self).save(*args, **kwargs)

    def gen_id(self):
        applicant_time = timezone.now()
        active_on = applicant_time.date()
        next_day = active_on + timezone.timedelta(days=1)
        total = UserOrderBuy.objects \
            .filter(create_at__range=(active_on, next_day)) \
            .count()
        order_id = int(active_on.strftime("%Y%m%d") + '0000') + total + 1
        return order_id

    class Meta:
        managed = False
        db_table = 'user_order_buy'


class NewsCategory(models.Model):
    '''新闻资讯分类表'''
    name = models.CharField(max_length=1024)
    status = models.SmallIntegerField(default=1)
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
    status = models.SmallIntegerField(default=1)
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


class CBCDPriceLog(models.Model):
    '''资本兑历史价格表'''
    price = models.DecimalField(max_digits=14, decimal_places=2)
    closing_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'CBCD_price_log'


class CBCDInit(models.Model):
    total = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    unsell = models.IntegerField()
    status = models.IntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'CBCD_init'


class UserVisaApply(models.Model):
    user = models.ForeignKey(auth_models.User)
    first_name = models.CharField(max_length=64, default='')
    last_name = models.CharField(max_length=64, default='')
    age = models.IntegerField()
    email = models.CharField(max_length=64, default='')
    phone = models.CharField(max_length=64, default='')
    id_card = models.CharField(max_length=64, default='')
    address = models.CharField(max_length=1024)
    city = models.CharField(max_length=128)
    provincy = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=64)
    status = models.SmallIntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'user_visa_apply'


class UserResetPwd(models.Model):
    username = models.CharField(max_length=64, default='')
    email = models.CharField(max_length=128, default='')
    hashkey = models.CharField(max_length=256, default='')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField()
    expire_at = models.DateTimeField()
    status = models.SmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.hashkey = uuid.uuid1()
        self.expire_at = timezone.now() + timedelta(hours=1)
        super(UserResetPwd, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'user_reset_pwd'
