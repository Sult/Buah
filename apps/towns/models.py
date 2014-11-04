from django.db import models
from django.utils.timezone import utc
from django.db.models import get_model
from django.contrib.auth.models import User


from apps.elements.models import VersionControl

import random
from datetime import datetime, timedelta




class TownMathValues(VersionControl):
    """ Holds numbers used in building related equations and functions. to balance and provide a smooth system """
    
    #Tavern numbers
    tavern_refresh_min = models.IntegerField()                      #in seconds
    tavern_refresh_max = models.IntegerField()                      #in seconds 
    tavern_heroes_min = models.IntegerField()
    tavern_heroes_max = models.IntegerField()
    
    
    


    
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


class Tavern(models.Model):
    """ Taverns are the place where new aquireable heroes spawn """
    
    now = datetime.utcnow().replace(tzinfo=utc)

    town = models.OneToOneField(Town)
    last_refresh = models.DateTimeField(default=now)
    next_refresh = models.IntegerField(default=0)                           # seconds to new refresh
    
    def __unicode__(self):
        return "Tavern in %s" % self.town.name
    
    
    #check if tavernheroes need to be refreshed
    def check_for_refresh(self):
        refresh_at = self.last_refresh + timedelta(seconds=self.next_refresh)
        now = datetime.utcnow().replace(tzinfo=utc)
        if now > refresh_at:
            self.refresh_hero_list()
            

    #refresh the existing set of available heroes
    def refresh_hero_list(self):
        self.delete_related_heroes()                                        #delete all old TavernHeroes
        self.next_refresh = self.random_refresh_timer()                     #get refresh timer
        self.last_refresh = datetime.utcnow().replace(tzinfo=utc)
        self.save()
        
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
        seconds = random.randint(town_values.tavern_refresh_min, town_values.tavern_refresh_max)
        return seconds
        
        
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
    
    tavern = models.ForeignKey(Tavern)
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
            
    



class OutskirtBuilding(models.Model):
    """ Townhalls are used to increase spawnrate of a certain Resource Tier of gathering fields """
    NONE = 0
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3
    TIER_4 = 4
    TIERS = (
        (NONE, "No Focus"),
        (TIER_1, "Tier 1"),
        (TIER_2, "Tier 2"),
        (TIER_3, "Tier 3"),
        (TIER_4, "Tier 4"),
    ) 
    
    TOWNHALL = "townhall"
    BARRACKS = "barracks"
    TRADEHOUSE = "tradehouse"
    BUILDINGS = (
        (TOWNHALL, "Townhall"),
        (BARRACKS, "Barracks"),
        (TRADEHOUSE, "Tradehouse"),
    )
    
    town = models.ForeignKey(Town)
    building = models.CharField(max_length=31, choices=BUILDINGS)
    level = models.IntegerField()
    focus = models.IntegerField(choices=TIERS, default=NONE)
    
    class Meta:
        unique_together = ["town", "building"]
    
    def __unicode__(self):
        return "Town: %s. Building: %s. Focus: Tier %d." % (self.town.name, self.building, self.focus)
    
    
    #get a random resource Field
    def random_resource_field(self):
        pass
    
    
    
    
    
    
    
    
    
    
    



