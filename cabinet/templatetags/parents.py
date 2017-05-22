from django import template
from cabinet.models import Word

register = template.Library()

# вернет номер предложения
@register.filter
def parent(word):
    return int(word[0].parent.id.split('s.')[1])

# вернет номер текста
@register.filter
def id(word):
    return word[0].id

# вернет номер слова
@register.filter
def word_id(word):
    return int(word[0].id.split('w.')[1])

# найдет морфологию найденного в фолиа-доке слова
@register.filter
def word_mark_id(word):
    return Word.objects.get(id=word[0].id.split('w.')[1]).mark_up_id