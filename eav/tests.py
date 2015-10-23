# coding=utf-8

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from . import models
from product.models import Product


class InfoTypeTestCase(TestCase):
    def setUp(self):
        models.InfoType.objects.make_init_data()

    def test_init(self):
        '测试InfoType的信息'
        info = {
                'Boolean': models.TypeBoolean,
                'DateTime': models.TypeDateTime,
                'Integer': models.TypeInteger,
                'Float': models.TypeFloat,
                'Char': models.TypeChar,
                'Text': models.TypeText,
                'Binary': models.TypeBinary,
                }
        for k, v in info.items():
            o = models.InfoType.objects.filter(name = k).first()
            self.assertEqual(o.content_type.model_class(), v)

    def test_InfoAttribute(self):
        '测试InfoAttribute'
        info = {
                '钢笔': models.TypeInteger,
                '文章': models.TypeText,
                }
        for k, v in info.items():
            content_type = ContentType.objects.get_for_model(v)
            o = models.InfoType.objects.filter(content_type = content_type).first()
            models.InfoAttribute.objects.create(
                    content_type = content_type,
                    field_name = k,
                    field_type = o,
                    )

