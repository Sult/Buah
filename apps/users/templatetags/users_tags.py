from django import template
from django.contrib.humanize.templatetags.humanize import intcomma


register = template.Library()


#view money value in templates
@register.filter
def munny(value):
    money = round(float(value), 2)
    return "%s%s Mn" % (intcomma(int(money)), ("%0.2f" % money)[-3:])







#http://stackoverflow.com/questions/346467/format-numbers-in-django-templates
#https://docs.djangoproject.com/en/dev/howto/custom-template-tags/

