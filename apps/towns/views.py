from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404
from django.db import transaction

from apps.towns.models import Town, Tavern, TavernHero, OutskirtResource
from apps.towns.forms import buy_tavernhero, OutskirtForm
from apps.heroes.models import Hero



@login_required
def town_info(request, slug):
    town = get_object_or_404(Town, slug=slug)
    
    
    return render(request, "towns/town_info.html", {"town": town})
    




@login_required
@transaction.atomic
def tavern(request):
    town = get_object_or_404(Town, slug=request.session['town_slug'])
    #check if tavern heroes need a refresh
    town.tavern.check_for_refresh()
    heroes = town.tavern.tavernhero_set.all()
    
    if request.POST:
        result = buy_tavernhero(request.POST, request.user)
        return render(request, "tavern.html", {"heroes": heroes, "result": result})
        
    return render(request, "towns/tavern.html", {"heroes": heroes})
    
    

@login_required
def tavern_hero_info(request, tavernhero_id):
    tavernhero = get_object_or_404(TavernHero, pk=tavernhero_id)
    
    if request.POST:
        result = buy_tavernhero(request.POST, request.user)
        return render(request, "tavernhero.html", {"tavernhero": tavernhero, "result": result})
    
    return render(request, "towns/tavernhero.html", {"tavernhero": tavernhero})



@login_required
@transaction.atomic
def outskirts(request):
    town = get_object_or_404(Town, slug=request.session['town_slug'])
    town.outskirt.check_for_refresh()
    hero = Hero.objects.get(id=request.session["hero_id"])
    outskirts = town.outskirt.display_outskirts(hero.id)
    refresh_at = town.outskirt.refresh_at
    
    if request.POST:
        try:
            result = OutskirtForm.save_form(request.POST, request.session['hero_id'], request.POST['outskirt_id'])
        
        except KeyError:
            result = "Don't customize POST data"
        return render(request, "outskirts.html", {"hero": hero, "outskirts": outskirts, "refresh_at": refresh_at, "result": result})
    
    #make sure forms disapear for a hero that is active
    #chekc if hero is actif before submiting form
    
    return render(request, "towns/outskirts.html", {"hero": hero, "outskirts": outskirts, "refresh_at": refresh_at})
    
    

@login_required
def outskirt_info(request, outskirt_id):
    outskirt = get_object_or_404(OutskirtResource, pk=outskirt_id)
    hero = Hero.objects.get(id=request.session["hero_id"])
    outskirt_view = outskirt.display_outskirt(hero)
    outskirt_form = OutskirtForm(request.POST or request.session["hero_id"], outskirt, False)
    
    if request.POST:
        print request.POST
    
    return render(request, "towns/outskirt.html", {"hero": hero, "outskirt_view": outskirt_view, "outskirt_form": outskirt_form, "outskirt": outskirt})
    




