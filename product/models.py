# coding=utf-8

# django app
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Product(models.Model):
    '产品'

    # 名称
    name = models.CharField(_('name'), max_length=50)
    # 说明
    detail = models.TextField(_('detail'))

    def __str__(self):
        return self.name

