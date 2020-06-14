'''
模板过滤器
用于处理有下划线的数据字段
'''
from django import template

register = template.Library()

@register.filter
def top250_id(value,arg):
    return value._meta.get_field(arg)._id