from django.db import models
from django.conf import settings


class Item(models.Model):
    TYPE_CHOICES = [('found', '失物招领'), ('lost', '寻物启事')]
    CATEGORY_CHOICES = [
        ('证件', '证件'), ('电子产品', '电子产品'), ('书籍文具', '书籍文具'),
        ('钥匙', '钥匙'), ('钱包', '钱包'), ('衣物', '衣物'), ('其他', '其他'),
    ]
    STATUS_CHOICES = [('active', '进行中'), ('matched', '已匹配'), ('closed', '已关闭')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items', verbose_name='发布者')
    type = models.CharField('类型', max_length=10, choices=TYPE_CHOICES)
    title = models.CharField('标题', max_length=200)
    category = models.CharField('分类', max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField('描述')
    location = models.CharField('地点', max_length=200)
    happened_at = models.DateTimeField('发生时间')
    contact_phone = models.CharField('联系电话', max_length=20, blank=True, null=True)
    contact_wechat = models.CharField('微信号', max_length=64, blank=True, null=True)
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='active')
    view_count = models.PositiveIntegerField('浏览次数', default=0)
    is_approved = models.BooleanField('已审核', default=True)
    created_at = models.DateTimeField('发布时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '物品'
        verbose_name_plural = '物品'
        db_table = 'items_item'
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.get_type_display()}] {self.title}'


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images', verbose_name='物品')
    image = models.ImageField('图片', upload_to='items/')
    order = models.PositiveSmallIntegerField('排序', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '物品图片'
        verbose_name_plural = '物品图片'
        db_table = 'items_image'
        ordering = ['order', 'created_at']


class Message(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='messages', verbose_name='物品')
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages', verbose_name='发送者')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages', verbose_name='接收者')
    content = models.TextField('内容')
    is_read = models.BooleanField('已读', default=False)
    created_at = models.DateTimeField('发送时间', auto_now_add=True)

    class Meta:
        verbose_name = '留言'
        verbose_name_plural = '留言'
        db_table = 'items_message'
        ordering = ['-created_at']
