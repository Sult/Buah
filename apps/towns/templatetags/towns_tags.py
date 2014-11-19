from django import template
from django.contrib.humanize.templatetags.humanize import intcomma


register = template.Library()


#able to view gather income (per hour) that selected hero will get
@register.filter
def display_gather_income(obj, hero_id):
    return obj.display_income(hero_id)


#able to view staminaloss (per hour) that a hero will loose on this outskirt
@register.filter
def display_stamina_loss(obj, hero_id):
    return obj.display_stamina_loss(hero_id)







#http://stackoverflow.com/questions/346467/format-numbers-in-django-templates
#https://docs.djangoproject.com/en/dev/howto/custom-template-tags/

