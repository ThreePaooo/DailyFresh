from django.template import Library

register = Library()

@register.filter
def total(price,num):
    return price * num
