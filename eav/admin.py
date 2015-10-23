# coding=utf-8

# django app
from django.contrib import admin

# our apps
from . import models


# Register your models here.
admin.site.register(models.InfoAttribute)

