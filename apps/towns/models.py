from django.db import models
from django.utils.timezone import utc
from django.db.models import get_model
from django.contrib.auth.models import User


from apps.elements.models import VersionControl, Resource
from apps.towns.forms import OutskirtForm

import random, itertools
from datetime import datetime, timedelta
from collections import namedtuple




class TownMathValues(VersionControl):
    """ Holds numbers used in building related equations and functions. to balance and provide a smooth system """
    
    #Tavern numbers
    tavern_refresh_min = models.IntegerField()                      #timer to new refresh in seconds
    tavern_refresh_max = models.IntegerField()                     
    tavern_heroes_min = models.IntegerField()                       #amount of heroes available
    tavern_heroes_max = models.IntegerField()
    
    #townhall
    townhall_tier_value_per_level = models.IntegerField()
    townhall_category_value_per_level = models.IntegerField()           #increases basechance for randmozing resource category
    townhall_category_base_value = models.IntegerField()                #base chance for randomizing resource category
    
    #Outskirts
    outskirt_duration_min = models.IntegerField()
    outskirt_duration_max = models.IntegerField()
    
    
    


    
class Town(models.Model):
    """ town objects keep track of all buildings, location, respawns etc """
    
    PLAYER = True
    NPC = False
    CONTROLLED = (
        (PLAYER, "Player"),
        (NPC, "NPC"),
    )
    
    slug = models.SlugField(max_length=63, unique=True)
    
    controlled = models.BooleanField(choices=CONTROLLED, default=True)
    owner_player = models.ForeignKey(User, null=True)
    owner_npc = models.ForeignKey('users.Npc', null=True)
    difficulty = models.IntegerField()
    #coordinates = models.ForeignKey(Coordinates)
        
    name = models.CharField(max_length=63, unique=True)
    description = models.TextField(blank=True)
    
    
    
    
    def __unicode__(self):
        if self.controlled:
            controlled = "Player"
        else:
            controlled = "NPC"
        return "%s Town: %s" % (controlled, self.name)
    



####### buildings #######
#TODO: tavern refresh can be done with 1 datetime instead of datetime + integer

class Tavern(models.Model):
    """ Taverns are the place where new aquireable heroes spawn """
    
    now = datetime.utcnow().replace(tzinfo=utc)

    town = models.OneToOneField("towns.Town")
    refresh_at = models.DateTimeField(default=now)
    
    def __unicode__(self):
        return "Tavern in %s" % self.town.name
    
    
    #check if tavernheroes need to be refreshed
    def check_for_refresh(self):
        now = datetime.utcnow().replace(tzinfo=utc)
        if now > self.refresh_at:
            self.refresh_at = self.random_refresh_timer()
            self.save()
            self.refresh_hero_list()
    

    #refresh the existing set of available heroes
    def refresh_hero_list(self):
        self.delete_related_heroes()                                        #delete all old TavernHeroes
        
        #populate with new heroes
        total_heroes = self.max_heroes_available()
        counter = 0
        while counter < total_heroes:
            TavernHero.add_hero(self)
            counter += 1
        

    
    #Calculate max heroes available
    #TODO: use amount of active players to get chance the random of max heroes
    def max_heroes_available(self):
        town_values = TownMathValues.current_version(TownMathValues)
        max_heroes = random.randint(town_values.tavern_heroes_min, town_values.tavern_heroes_max)
        return max_heroes

    
    
    #random refresh time
    #TODO: customize random a bit by active users in town?
    def random_refresh_timer(self):
        town_values = TownMathValues.current_version(TownMathValues)
        now = datetime.utcnow().replace(tzinfo=utc)
        minutes = random.randint(town_values.tavern_refresh_min, town_values.tavern_refresh_max)
        new_refresh = now + timedelta(minutes=minutes)
        return new_refresh
        
        
    #delete all related tavernheroes
    def delete_related_heroes(self):
        #iterate over all related heroes
        related_heroes = self.tavernhero_set.all()
        for related_hero in related_heroes:
            #delete hero object, then tavernhero
            related_hero.hero.delete()
            related_hero.delete()
    
    
      

class TavernHero(models.Model):
    """ available heroes in a perticulair Tavern """
    
    tavern = models.ForeignKey("towns.Tavern")
    price = models.IntegerField()
    
    #classes
    hero = models.ForeignKey("heroes.Hero")
    
    
    def __unicode__(self):
        return "Tavern Hero"
    
    
    
    #get a dict of min/max prices by attribute quality
    @staticmethod
    def get_quality_prices():
        prices = {}
        statperlevel = get_model("heroes", "StatPerLevel")
        prices["Very Bad"] = [1000, 2500]
        prices["Bad"] = [2500, 5000]
        prices["Decent"] = [5000, 7500]
        prices["Good"] = [7500, 15000]
        prices["Excellent"] = [20000, 75000]
        return prices

    
    #calculate the price of a hero based on hero attribute qualities
    @staticmethod
    def calculate_hero_price(hero):
        categories = ['combat', 'trade', 'crafting']
        prices = TavernHero.get_quality_prices()
        
        total = 0
        for category in categories:
            quality = hero.view_category_score(hero.get_category_score(category))
            price = prices[quality]
            total += random.randint(price[0], price[1])
        
        total = int(round(total, -2))
        return total

        

    #add a new tavernhero
    @staticmethod
    def add_hero(tavern):
        hero = get_model("heroes", "Hero").create_random_hero()
        price = TavernHero.calculate_hero_price(hero)
        tavernhero = TavernHero.objects.create(hero=hero, price=price, tavern=tavern)
        tavernhero.add_hero_name()
        tavernhero.hero.town = tavern.town
        
        
    
    #add a tavern hero name
    def add_hero_name(self):
        check = True
        while check:
            name = self.hero.random_hero_name()
            tavernheroes = TavernHero.objects.filter(tavern=self.tavern, hero__name=name)
            if not tavernheroes:
                self.hero.name=name
                self.hero.save()
                check = False
     
     
     
    #get the actual hero price for the user
    def actual_hero_price(self, user):
        #get tribe/guild of town reputation and the corrosponding modifier
        #price = self.price * modifier
        return self.price
         
     
     
    
    #remove hero from tavern and set hero to a player
    def transfer_hero(self, user):
        hero = self.hero
        hero.user = user
        hero.town = self.tavern.town
        hero.created = datetime.utcnow().replace(tzinfo=utc)
        hero.save()
        self.delete()
        return hero
    
    
    



class Townhall(models.Model):
    """ building that lets players partly control spawning of resource locations """
    
        #(TOWNHALL, "Townhall"),
        #(BARRACKS, "Barracks"),
        #(TRADEHOUSE, "Tradehouse"),
    
    NO_FOCUS = "no focus"
    FOCUS = ((NO_FOCUS, "No Focus"),) + Resource.CATEGORIES
    NO_TIER = 0
    TIERS = ((NO_TIER, "No Focus"),) + Resource.TIERS
    
    town = models.OneToOneField("towns.Town")
    level = models.IntegerField()
    category = models.CharField(max_length=15, choices=FOCUS)
    tier = models.IntegerField(choices=TIERS)

    def __unicode__(self):
        return "Townhall. level: %d" % (self.level)
    
    
    #get the total value for randomizing resource category
    def total_category_value(self, town_values):
        bonus = 0
        categories = len(Resource.CATEGORIES)
        
        if self.category != Townhall.NO_FOCUS:
            bonus = self.level * town_values.townhall_category_value_per_level
        
        total = categories * town_values.townhall_category_base_value + bonus 
        return total
    
    
    #get the total value for randomizing resource tier
    def total_tier_value(self, spawnoutskirt, town_values):
        bonus = 0
        difficulty_total = spawnoutskirt.total_from_tiers()
        if self.tier != Townhall.NO_TIER:
            bonus = self.level * town_values.townhall_tier_value_per_level
        
        return difficulty_total + bonus
    
    
    #see roll is succes
    @staticmethod
    def roll_success(roll, success):
        if roll <= success:
            return True
        else:
            return False
    
                
    #random the resource tier for outskirt
    def random_resource_category(self):
        town_values = TownMathValues.current_version(TownMathValues)
        total = self.total_category_value(town_values)
        
        for category in itertools.cycle(Resource.CATEGORIES):
            result = self.check_category_succeed(total, category[0], town_values)
            if result:
                return category[0]
        
        
    # check if a random resource roll succeeds or not
    def check_category_succeed(self, total, category, town_values):
        roll = random.randint(0, total)
        success = town_values.townhall_category_base_value
        if category == self.category:
            success += self.level * town_values.townhall_category_value_per_level
        
        return self.roll_success(roll, success)
    
    
    #random a random resource tier for outskirts
    def random_resource_tier(self):
        town_values = TownMathValues.current_version(TownMathValues)
        spawnoutskirt = get_model("elements", "SpawnOutskirt").objects.get(difficulty=self.town.difficulty)
        total = self.total_tier_value(spawnoutskirt, town_values)
        
        for tier in itertools.cycle(Resource.TIERS):
            result = self.check_tier_succeed(total, tier[0], spawnoutskirt, town_values)
            if result:
                return tier[0]
        
    
    #check if a random tier roll succeeds
    def check_tier_succeed(self, total, tier, spawnoutskirt, town_values):
        roll = random.randint(0, total)
        success = getattr(spawnoutskirt, "tier_" + str(tier))
        if self.tier == tier:
            success += self.level * town_values.townhall_tier_value_per_level
            
        return self.roll_success(roll, success)
        






##### Town Surroundings ########

class Outskirt(models.Model):
    """ resource gathering outskirts of a town """
    
    now = datetime.utcnow().replace(tzinfo=utc)
    
    town = models.OneToOneField("towns.Town")
    refresh_at = models.DateTimeField(default=now)
    resources_min = models.IntegerField()                               # amount of resources (base values)
    resources_max = models.IntegerField()    
    
    resources_upgrade_level = models.IntegerField(default=0)            #maximum 10 upgrades (every 2 is +1 resource)
    heroes_upgrade_level = models.IntegerField(default=0)               #maximum 10
    
    
    
    def __unicode__(self):
        return "Outskirts of %s." % self.town.name
    
    
    #check if tavernheroes need to be refreshed
    def check_for_refresh(self):
        now = datetime.utcnow().replace(tzinfo=utc)
        if now > self.refresh_at:
            self.refresh_at = self.random_refresh_timer()
            self.save()
            self.refresh_outskirts()
    
    #random a new outskirt duration for town
    def random_refresh_timer(self):
        town_values = TownMathValues.current_version(TownMathValues)
        hours = random.randint(town_values.outskirt_duration_min, town_values.outskirt_duration_max)
        now = datetime.utcnow().replace(tzinfo=utc)
        new_refresh = now + timedelta(hours=hours)
        return new_refresh
        
    #refreshes the outskirt resources
    def refresh_outskirts(self):
        self.remove_outskirt_resources()

        #generate new resources
        self.create_new_resources()
            
    #remove all connected outskirts
    def remove_outskirt_resources(self):
        for resource in self.outskirtresource_set.all():
            resource.remove_heroes()
            resource.delete()
    
    #create new resources for outskirt
    def create_new_resources(self):
        amount_resources = self.random_amount_resources() + int(self.resources_upgrade_level / 2)
        counter = 0
        while counter < amount_resources:
            counter +=1
            quality = self.random_resource_quality()
            resource = self.random_resource()
            heroes = resource.random_heroes_on_resource() + self.heroes_upgrade_level
            OutskirtResource.objects.create(outskirt=self, quality=quality, heroes=heroes, resource=resource)
            
    #get random amount of new outskirt resources
    #TODO: maybe add ways to increase
    def random_amount_resources(self):
        amount = random.randint(self.resources_min, self.resources_max)
        return amount
    
    #get a random quality
    #TODO: chance random chances depending on difficulty or player building
    @staticmethod
    def random_resource_quality():
        choices = [x for x in OutskirtResource.QUALITIES if x[0] != OutskirtResource.ABUNDANT]  #remove abundant from tuple
        quality = random.choice(choices)[0]
        return quality
    
    #get random resource
    def random_resource(self):
        townhall = self.town.townhall
        tier = townhall.random_resource_tier()
        category = townhall.random_resource_category()
        resource = get_model("elements", "Resource").objects.filter(category=category, tier=tier).order_by("?")[0]
        return resource
        
    #display outskirts in template
    def display_outskirts(self, hero_id):
        resources = self.outskirtresource_set.all()
        hero = get_model("heroes", "Hero").objects.get(id=hero_id)
        outskirts = []
        for resource in resources:
            outskirts.append(resource.display_outskirt(hero))
        
        return outskirts
        
    
    ##### Form functions
    #get time left for callculating choices (in minutes)
    def time_left(self):
        now = datetime.utcnow().replace(tzinfo=utc)
        
        minutes_left = (self.refresh_at - now).seconds // 60
        
        return minutes_left
        
    
    
class OutskirtResource(models.Model):
    """ available gatherable resources in a town """
    
    DEPLETED = 0.8
    POOR = 0.9
    DECENT = 1
    RICH = 1.1
    OVERFLOWING = 1.2
    ABUNDANT = 1.3
    QUALITIES = (
        (DEPLETED, "Depleted"),
        (POOR, "Poor"),
        (DECENT, "Decent"),
        (RICH, "Rich"),
        (OVERFLOWING, "Overflowing"),
        (ABUNDANT, "Abundant"),
    )
    
    outskirt = models.ForeignKey("towns.Outskirt")
    resource = models.ForeignKey("elements.Resource")
    heroes = models.IntegerField()
    quality = models.FloatField(choices=QUALITIES)
    
    def __unicode__(self):
        return "Resource: %s" % self.resource.name
    
    
    # remove all heroes from resources and give them the rewards
    def remove_heroes(self):
        pass
    
    
    #returns open slots on resource
    def open_slots(self):
        spots_taken = 0 #getspots taken
        spots_left = self.heroes - spots_taken
        return spots_left
    
    
    # make a namedtuple display for OutskirtResource in template
    def display_outskirt(self, hero):
        DisplayOutskirt = namedtuple("DisplayOutskirt", "outskirt income stamina_loss loss room open_slots form")
        income = self.display_income(hero) + " per hour"
        
        if self.resource.stamina_cost == 0:
            stamina_loss = False
            loss = 0
        else:
            stamina_loss = True
            loss = self.display_stamina_loss(hero) + " per hour"
        
        open_slots = self.open_slots()
        if open_slots < 1:
            room = False
        else:
            room = True
        open_slots = str(open_slots) + " spots left"
        
        form = OutskirtForm(hero.id, self, True)
        
        return DisplayOutskirt(outskirt=self, income=income, stamina_loss=stamina_loss, loss=loss, room=room, open_slots=open_slots, form=form)
        
        

    # gives a rounded display for income per hour
    def display_income(self, hero):
        income = hero.gather_income(self.resource.gather_speed, self.quality)
        return str(round(income, 1))
        
    
    #def display stamina cost in template
    def display_stamina_loss(self, hero):
        cost = hero.stamina_loss(self.resource.stamina_cost)
        return str(round(cost, 1))
    
    
    
    

class OutskirtWorker(models.Model):
    """ keeps track of what hero works what workyard for how long """
    
    resource = models.ForeignKey('towns.OutskirtResource')
    hero = models.OneToOneField("heroes.Hero")
    started_at = models.DateTimeField()
    finnished_at = models.DateTimeField()
    
    
    
    
    



