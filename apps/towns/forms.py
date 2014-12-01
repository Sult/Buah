from django import forms
from django.db.models import get_model
from django.utils.timezone import utc
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime, timedelta
from collections import namedtuple
import math

# buy a new hero for a user
def buy_tavernhero(postdata, user):
    Result = namedtuple("Result", "error message")
    #check if user is allowed to buy another hero
    if not user.profile.new_hero_available():
        return Result(error=True, message="You do not have room for more heroes.")
    
    #see if hero still exists
    try:
       tavernhero = get_model("towns", "TavernHero").objects.get(pk=postdata['tavernhero_id'])
    except TavernHero.DoesNotExist, KeyError:
        return Result(error=True, message="This hero is already taken.")
    
    #check if player has enough money
    price = tavernhero.actual_hero_price(user)
    if not user.profile.has_enough_munny(price):
        return Result(error=True, message="You do not have enough munny to buy this hero.")
        
    #if all requirements are met
    #pay money
    user.profile.update_munny(-price)
    
    #transfer hero
    tavernhero.transfer_hero(user)
    return Result(error=False, message="""You bought a hero. Go to the "Heroes" overview, to select it and put it to work.""")
    





    
    

    
class OutskirtForm(forms.Form):
    """ set a hero to work at an outskirt """
    

    def __init__(self, hero_id, outskirt, timer, *args, **kwargs):
        super(OutskirtForm, self).__init__(*args, **kwargs)
        self.hero = get_model("heroes", "Hero").objects.get(id=hero_id)
        self.outskirt = outskirt
        if timer:
            choices = self.duration_choices(self.hero, self.outskirt)
        else:
            choices = self.resource_choices(self.hero, self.outskirt)
        self.fields['worktime'] = forms.ChoiceField(choices=choices, label="")


##### validation ###############
    #prosses the postdata to an active outskirt worker
    @staticmethod
    def save_form(postdata, hero_id, outskirt_id):
        #validate data
        hero = get_model("heroes", "Hero").objects.get(id=hero_id)
        result = OutskirtForm.validate_postdata(postdata, outskirt_id, hero)
        if result != True:
            return result
        
        #create worker
        outskirt = get_model("towns", "OutskirtResource").objects.get(id=outskirt_id)
        result, obj = OutskirtForm.create_outskirt_worker(postdata, outskirt, hero)
        if result != True:
            return obj
        #update hero
        OutskirtForm.update_hero(postdata, outskirt, hero)
        return "Your hero wil be done at %s" % obj.finnished_at
        
        
        
        
    #validate if the POSTdata is correct
    @staticmethod
    def validate_postdata(postdata, outskirt_id, hero):
        try:
            int(postdata['outskirt_id'])
            int(postdata['worktime'])
        except ValueError, KeyError:
            return "Stop messing with POST data!"
        
        try:
            get_model("towns", "OutskirtResource").objects.get(id=outskirt_id)
        except ObjectDoesNotExist:
            return "This outskirt no longer exists."
        if hero.active:
            return "Your hero is already working."
        
        return True
            
        

    #create working object from postdata
    @staticmethod
    def create_outskirt_worker(postdata, outskirt, hero):
        now = datetime.utcnow().replace(tzinfo=utc)
        timer = timedelta(seconds = int(postdata["worktime"]) * 60)
        finnished_at = now + timer
        
        if finnished_at > outskirt.outskirt.refresh_at:
            return False, "The outskirt will be gone before your hero is finnished."
        
        worker = get_model("towns", "OutskirtWorker").objects.create(outskirtresource=outskirt,
                                                        hero=hero, started_at=now, finnished_at=finnished_at)
        return True, worker
        
        
    # update hero remove stamina
    @staticmethod
    def update_hero(postdata, outskirt, hero):
        stamina_cost = int(postdata["worktime"]) * hero.stamina_loss(outskirt.resource.stamina_cost) + 0.0
        hero.stamina_current -= stamina_cost
        hero.save()
        
    
            
        

        
        





#### Dynamic Form Field Functions

    #generate refined choices
    @staticmethod
    def duration_choices(hero, outskirt):
        minutes_left = outskirt.outskirt.time_left()
        stamina_minutes = hero.max_time_with_stamina(outskirt.resource.stamina_cost)
        part_1 = OutskirtForm.add_5_15_minutes(minutes_left, stamina_minutes)
        part_2 = OutskirtForm.add_30_60_minutes(minutes_left, stamina_minutes)
        part_3 = OutskirtForm.add_90_120_minutes(minutes_left, stamina_minutes)
        part_4 = OutskirtForm.add_remaining_hours(minutes_left, stamina_minutes)
        choices = tuple(part_1 + part_2 + part_3 + part_4)
        
        return choices
    
    
    #generate simple choices
    @staticmethod
    def resource_choices(hero, outskirt):
        minutes_left = outskirt.outskirt.time_left()
        stamina_minutes = hero.max_time_with_stamina(outskirt.resource.stamina_cost)
        
        choices_list = OutskirtForm.add_per_resource(minutes_left, stamina_minutes, hero, outskirt)
        
        return tuple(choices_list)
        
    
    #get the first hour time secdule
    @staticmethod
    def add_5_15_minutes(minutes_left, stamina_minutes):
        choices_list = []
        if minutes_left > 5 and stamina_minutes > 5:
            choices_list.append((5, "5 minutes"))
        if minutes_left > 15 and stamina_minutes > 15:
            choices_list.append((15, "15 minutes"))
        return choices_list
    
    
    #get the first hour time secdule
    @staticmethod
    def add_30_60_minutes(minutes_left, stamina_minutes):
        choices_list = []
        if minutes_left > 30 and stamina_minutes > 30:
            choices_list.append((30, "30 minutes"))
        if minutes_left > 60 and stamina_minutes > 60:
            choices_list.append((60, "1 hour"))
        return choices_list
    
        
    #add the 90 and 120 minutes to choices
    @staticmethod
    def add_90_120_minutes(minutes_left, stamina_minutes):
        choices_list = []
        if minutes_left > 90 and stamina_minutes > 90:
            choices_list.append((90, "1 hour 30 minutes"))
        if minutes_left > 120 and stamina_minutes > 120:
            choices_list.append((120, "2 hours"))
        return choices_list
            
    
    #add hours to chocies untill time or stamina runs out
    @staticmethod
    def add_remaining_hours(minutes_left, stamina_minutes):
        choices_list = []
        counter = 180
        while counter < minutes_left:
            if counter < stamina_minutes:
                choices_list.append((counter, str(counter / 60) + " hours"))
            counter += 60
        
        return choices_list
    
    
        #get tuime needed for x resources
    @staticmethod
    def time_needed_for_x_resources(x, gather_income):
        return math.ceil(x / gather_income * 60)
    
    
    #add the option to choose for 1 or 10 of the given resource
    @staticmethod
    def add_per_resource(minutes_left, stamina_minutes, hero, outskirt):
        choices_list = []
        gather_income = hero.gather_income(outskirt.resource.gather_speed, outskirt.quality)
        #get rounded up minutes to get 1 resource
        values = [1, 5, 10, 25, 50, 100, 250, 500, 1000, 2000]
        for value in values:
            duration = OutskirtForm.time_needed_for_x_resources(value, gather_income)
            if minutes_left > duration and stamina_minutes > duration:
                choices_list.append((duration, "%d %s" % (value, outskirt.resource.name)))
            else:
                return choices_list
        
        return choices_list
    
    
    
    
    
    
    
    
    
    
    
