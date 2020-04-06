from django import template
# https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/#code-layout
from django.template.defaultfilters import stringfilter


register = template.Library()



# @register.filter # will use function name as a filtername
# @register.filter(name='kilosep') # set custom name for the filter
# @stringfilter # This will convert an object to its string value before being passed to function
def kilosep(value, sep=' '):
    """My own copy of humanize:intcomma"""
    if not isinstance(value, int):
        return value
    listval = list(str(value))
    result = ''
    while len(listval):
        try:
            result = listval.pop() + result
            result = listval.pop() + result
            result = listval.pop() + result
        except IndexError:
            return result
        if len(listval):
            result = sep + result
    return result


register.filter('kilosep', kilosep) # first - the name of the filter, second - function
