from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name='标题', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄", default=18)
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    # create_time = models.DateTimeField(verbose_name="入职时间")
    create_time = models.DateField(verbose_name="入职时间")
    # 设置外键
    # 表示部门表被删，此处也会自动删除
    depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)

    def __str__(self):
        return self.name


class PrettyNumber(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="号码", max_length=11)
    price = models.IntegerField(verbose_name="价格", default=0)
    level_choices = (
        (1, "青铜"),
        (2, "白银"),
        (3, "黄金"),
        (4, "钻石"),
        (5, "王者"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=2)
    status_choices = (
        (1, "已占用"),
        (2, "未占用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)


class Admin(models.Model):
    """管理员表"""
    username = models.CharField(verbose_name="Username", max_length=20)
    password = models.CharField(verbose_name="Password", max_length=40)


class Order(models.Model):
    """订单表"""
    oid = models.CharField(verbose_name="订单ID", max_length=64)
    title = models.CharField(verbose_name="商品名称", max_length=64)
    price = models.IntegerField(verbose_name="价格")

    status_choices = (
        (1, "待支付"),
        (2, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="订单状态", choices=status_choices, default=1)
    admin = models.ForeignKey(verbose_name="管理员", to="Admin", on_delete=models.CASCADE)


class Application(models.Model):
    """应用表"""
    app_type_choices = (
        (1, '前端'),
        (2, '后端'),
        (3, '联接'),
        (4, '运维'),
        (5, '其他'),
    )
    app_type = models.SmallIntegerField(verbose_name="应用分类", choices=app_type_choices)
    app_name = models.CharField(verbose_name="应用名称", max_length=128)

    def __str__(self):
        return self.get_app_type_display() + "---" + self.app_name


class AssetsInfo(models.Model):
    """硬件资产"""
    sn = models.CharField(verbose_name="序列号", max_length=128)
    ipv4 = models.CharField(verbose_name="IPv4地址", max_length=256)
    core_num = models.SmallIntegerField(verbose_name="CPU核心数")
    mem = models.IntegerField(verbose_name="内存")
    disk = models.CharField(verbose_name="硬盘", max_length=128)
    status_choices = (
        (1, 'online'),
        (2, 'offline')
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices)
    owner = models.ForeignKey(to="UserInfo", to_field="id", on_delete=models.SET_NULL, blank=True, null=True)
    # app = models.ForeignKey(to="Application", on_delete=models.SET_NULL, null=True)
    app = models.ManyToManyField(Application, blank=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)


class PasswordManagement(models.Model):
    """密码管理表"""
    url = models.CharField(verbose_name="网址", max_length=1000, blank=True, null=True)
    username = models.CharField(verbose_name="用户名", max_length=128)
    password = models.CharField(verbose_name="密码", max_length=128)
    remark = models.CharField(verbose_name="备注", max_length=256)
    update_user = models.ForeignKey(User, to_field="id", on_delete=models.SET_NULL, blank=True, null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    def __str__(self):
        return self.update_user


class PasswordManagementRecord(models.Model):
    url = models.CharField(verbose_name="url", max_length=1000)
    msg = models.CharField(verbose_name="变更记录", max_length=1000)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


class LowValueConsumable(models.Model):
    name = models.CharField(verbose_name='物品分类', max_length=512)
    brand = models.CharField(verbose_name='品牌名称', max_length=512)
    model = models.CharField(verbose_name='物品型号', max_length=512)
    inventory_quantity = models.IntegerField(verbose_name='库存数量')
    price = models.IntegerField(verbose_name='价格')
    warehouse_choice = (
        (1, '上海仓库'),
        (2, '杭州仓库'),
        (3, '深圳仓库'),
    )
    warehouse = models.SmallIntegerField(verbose_name='所在库房', choices=warehouse_choice)
    barcode = models.CharField(verbose_name='商品条码', max_length=512)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)


class LowValueConsumableRecord(models.Model):
    username = models.CharField(verbose_name="领用人", max_length=512)
    model = models.CharField(verbose_name="物品名称", max_length=512)
    create_time = models.DateTimeField(verbose_name="申请时间", auto_now_add=True)
