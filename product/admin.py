# coding=utf-8

# django apps
from django.contrib import admin

# our apps
from . import models


# Register your models here.
admin.site.register(models.Product)

