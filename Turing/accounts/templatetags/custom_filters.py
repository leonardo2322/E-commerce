from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='replace')
def replace_comma(value):
    return str(value).replace(',', '.')