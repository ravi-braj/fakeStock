#custom filters for accessing informations in dictionaries in Django templates

from django import template
from django.template.defaulttags import register


register = template.Library()


#finds the item in a dict based on a key
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

#finds the price of an item based on the key
@register.filter
def get_price(dictionary, key):
	return dictionary.get(key)['price']

#finds the volume of an item based on the key
@register.filter
def get_volume(dictionary, key):
	return dictionary.get(key)['volume']