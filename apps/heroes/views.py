from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf

from django.contrib.auth.models import User
from apps.heroes.models import Hero
from apps.heroes.forms import HeroNameForm


@login_required
def view_heroes(request):
    heroes = Hero.objects.filter(user=request.user)
    
    if request.GET:
        hero_id = request.GET.get("hero", heroes[0].id)
        try:
            hero = Hero.objects.get(pk=int(hero_id), user=request.user)
        except Hero.DoesNotExist, ValueError:
            hero = heroes[0]
        
        request.session['hero_id'] = hero.id
        request.session['town_name'] = hero.town.name
        request.session['town_slug'] = hero.town.slug
        
        #if request.GET:
        #order_by = request.GET.get('order_by', "id")
        #region_name = request.GET.get('region', character.region.name)
        #region = Region.objects.get(name=region_name)
        #region_actions = show_garage_regions(region_name)
    
    return render(request, "view_heroes.html", {"heroes": heroes})



@login_required
def view_hero(request, hero_id):
    hero = get_object_or_404(Hero, pk=hero_id)
    hero_form = HeroNameForm(request.POST or None)
    
    if request.POST and hero_form.is_valid():
        hero_form.save(hero=hero)

    hero_form = HeroNameForm(initial={"name": hero.name})
    
    return render(request, "view_hero.html", {"hero": hero, "hero_form": hero_form})
