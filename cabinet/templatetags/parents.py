from django import template
from cabinet.models import Word

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

@register.filter
def word_mark_id(word):
    return Word.objects.get(id=word[0].id.split('w.')[1]).mark_up_id