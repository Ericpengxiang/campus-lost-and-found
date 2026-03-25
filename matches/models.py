from django.db import models


class Match(models.Model):
    STATUS_CHOICES = [('pending', '待确认'), ('confirmed', '已确认'), ('rejected', '已拒绝')]

    found_item = models.ForeignKey('items.Item', on_delete=models.CASCADE, related_name='found_matches', verbose_name='失物招领')
    lost_item = models.ForeignKey('items.Item', on_delete=models.CASCADE, related_name='lost_matches', verbose_name='寻物启事')
    score = models.IntegerField('匹配分数', default=0)
    reason = models.TextField('匹配理由', blank=True, null=True)
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '匹配记录'
        verbose_name_plural = '匹配记录'
        db_table = 'matches_match'
        ordering = ['-score', '-created_at']
        unique_together = [('found_item', 'lost_item')]

    def __str__(self):
        return f'匹配: {self.found_item.title} <-> {self.lost_item.title} ({self.score}分)'
