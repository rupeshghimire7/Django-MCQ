from django import template
import json
import random
register = template.Library()



@register.filter(name='get_options')
def get_options(value):
    option = json.loads(value)
    random.shuffle(option)
    return option


@register.filter(name='get_level')
def get_level(value):
    if value == 'E':
        return "Marks:1"
    elif value == 'M':
        return "Marks:2"
    elif value == 'H':
        return "Marks:3"
    else:
        return 'Unknown'
    

@register.filter(name='get_subject')
def get_subject(value):
    if value==None or value=='':
        return "Minor Project"
    

@register.filter(name='get_remarks')
def get_remarks(value):
    if value==None or value=='':
        return "No Remarks"
    else:
        
        return value[0]
        