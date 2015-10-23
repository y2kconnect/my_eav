# coding=utf-8

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.fields.related import OneToOneField
from django.utils.translation import ugettext_lazy as _


class InfoTypeManager(models.Manager):
    def make_init_data(self):
        '实体的属性类型: 初始化数据'
        info = {
                'Boolean': TypeBoolean,
                'DateTime': TypeDateTime,
                'Integer': TypeInteger,
                'Float': TypeFloat,
                'Char': TypeChar,
                'Text': TypeText,
                'Binary': TypeBinary,
                }
        for k, v in info.items():
            o = ContentType.objects.get_for_model(v)
            InfoType.objects.create(
                    name = k,
                    content_type = o,
                    )


class InfoType(models.Model):
    '实体的属性类型'

    # 属性类型的名称
    name = models.CharField(_('name'), max_length=50)
    # 属性类型，对应的数据表
    content_type = models.ForeignKey(ContentType, verbose_name=_('content_type'))

    objects = InfoTypeManager()

    def __str__(self):
        return self.name


class InfoAttribute(models.Model):
    '实体的属性信息'

    # 实体的数据模型
    content_type = models.ForeignKey(ContentType, verbose_name=_('content_type'))
    # 实体的属性名称
    field_name = models.CharField(_('name'), max_length=50)
    # 实体的属性类型
    field_type = models.ForeignKey(InfoType, verbose_name=_('field_type'))

    def __str__(self):
        return '{}, {}'.format(self.field_name, self.field_type.name)

    def get_InfoAttribute(self):
        '''
        获取实体的属性
        参照:
            django/db/models/base.py --> ModelBase.__new__()
        '''
        # 实体的model
        model = self.content_type.model_class()
        # 给model增加字段
        base = model._meta.concrete_model
        attr_name = '{}_ptr'.format( base._meta.model_name )
        field = OneToOneField(
                base,
                name = attr_name,
                auto_created = True,
                parent_link = True,
                )
        model.add_to_class(self.field_name, field)
        model._meta.parents[base] = field
        return model

    def set_InfoAttribute(self, obj, field_name, field_type):
        '设置实体的属性'
        self.field_name = field_name
        self.field_type = field_type
        o = ContentType.objects.get_for_model( obj.__class__ )
        self.content_type = o


class TypeBase(models.Model):
    'eav类型的基类'

    # 实体_id
    entity_id = models.IntegerField(_('entity_id'))
    # 实体的属性_id
    info_attribute = models.ForeignKey(InfoAttribute, verbose_name=_('info_attribute'))

    class Meta:
        abstract = True

    def get_entity(self):
        '通过info_attribute和entity_id，获取实体对象'
        print('TypeBase.get_entity(): ...')
        model = self.info_attribute.content_type.model_class()
        print('\tmodel: {}'.format(model))
        self.entity = model.objects.get(pk = self.entity_id)
        print('\tself.entity: {}'.format( self.entity ))

    def set_entity(self, obj):
        print('TypeBase.set_entity(): ...')
        self.entity_id = obj.id
        print('\tself.entity_id: {}'.format( self.entity_id ))
        model = ContentType.objects.get_for_model( obj.__class__ )
        print('\tmodel: {}'.format(model))
        self.info_attribute = model
        print('\tself.info_attribute: {}'.format( self.info_attribute ))

    entity = property(get_entity, set_entity)


class TypeBoolean(TypeBase):
    '布尔类型'
    value = models.BooleanField(_('value'))


class TypeDateTime(TypeBase):
    '时间类型'
    value = models.DateTimeField(_('value'))


class TypeInteger(TypeBase):
    '整型'
    value = models.IntegerField(_('value'))


class TypeFloat(TypeBase):
    '浮点类型'
    value = models.FloatField(_('value'))


class TypeChar(TypeBase):
    '字符串类型'
    value = models.CharField(_('value'), max_length=256)


class TypeText(TypeBase):
    '文本类型'
    value = models.TextField(_('value'))


class TypeBinary(TypeBase):
    '二进制数据块类型'
    value = models.BinaryField(_('value'))


