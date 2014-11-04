from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404

from apps.towns.models import Town, Tavern, TavernHero



@login_required
def view_town_info(request, slug):
    town = get_object_or_404(Town, slug=slug)
    
    return render(request, "town_info.html", {"town": town})
    




@login_required
def tavern(request):
    #get active here for user
    tavern = Tavern.objects.get(id=2)
    #check if tavern heroes need a refresh
    tavern.check_for_refresh()
    
    request.session['hero'] = "bla"
    heroes = tavern.tavernhero_set.all()
    
    return render(request, "tavern.html", {"heroes": heroes})
    
    #tavernhero_set.filter(warrior__isnull=False)



def tavern_hero_info(request, tavernhero_id):
    tavernhero = get_object_or_404(TavernHero, pk=tavernhero_id)
    
    return render(request, "tavernhero.html", {"tavernhero": tavernhero})
