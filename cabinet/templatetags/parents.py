from django import template

register = template.Library()

@register.filter
def parent(word):
    return int(word[0].parent.id.split('s.')[1])

@register.filter
def id(word):
    return word[0].id

@register.filter
def word_id(word):
    return int(word[0].id.split('w.')[1])