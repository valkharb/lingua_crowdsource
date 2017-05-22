from django import template

register = template.Library()

# парсит результат поиска по фолиа-доку
@register.filter
def cql_word(word):
    return word[0].text()
