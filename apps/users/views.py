from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.contrib.auth.models import User

from apps.users.forms import RegistrationForm, LoginForm
from apps.users.models import Profile
from apps.heroes.models import Hero


def add_needed_sessions(request):
    if "hero_id" not in request.session:
        request.session['hero_id'] = Hero.objects.filter(user=request.user)[0].id
    if "town_name" not in request.session:
        request.session['town_name'] = Hero.objects.get(pk=request.session['hero_id']).town.name
        request.session['town_slug'] = Hero.objects.get(pk=request.session['hero_id']).town.slug




def index(request):
    login_form = LoginForm(request.POST or None)
    
    if request.POST and login_form.is_valid():
        user = login_form.login(request)
        if user:
            login(request, user)
            
            #add sessions if they dont exist yet
            add_needed_sessions(request)
            
            return HttpResponseRedirect(request.POST.get('next') or reverse('index'))
    
    return render(request, "users/index.html", {"login_form": login_form, 'next': request.GET.get('next', '')})
    
    
    
    #return render(request, "index.html", {"login_form": login_form})



# Register new user
def register_user(request):
    form = RegistrationForm(request.POST or None)
    # False till someone fills in and sends
    if request.POST and form.is_valid():
        new_user = form.save()
        #send confiermationmail blabla
        Profile.create_profile(new_user)
        
        
        return HttpResponseRedirect(reverse('register succes'))
    
    return render(request, 'users/register.html', {'form': form})
    


def register_succes(request):
    login_form = LoginForm(request.POST or None)
    return render(request, "users/register_succes.html", {"login_form": login_form})



@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))



    

