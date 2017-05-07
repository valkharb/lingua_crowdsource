from django import template

register = template.Library()

@register.filter
def cql_word(word):
    return word[0].text()