from django.db import models
from django.db.models import Max                #to get a maxvalue in queryset

import random

#abstract class used for versioncontrol
class VersionControl(models.Model):
    """ abstract class that holds versionnumbers and the version functionality """
    
    version = models.IntegerField(unique=True)
    
    class Meta:
        abstract = True
        
        
    def __unicode__(self):
        number_list = [int(char) for char in str(self.version)]
        number_list = number_list[::-1]                         #reverse list
        version = ""
        for index in range(0, len(number_list), 2):
            try:
                version = str(number_list[index+1]) + str(number_list[index]) + "." + version
            except IndexError:
                version = str(number_list[index]) + "." + version
        
        version = version[:-1]                                  # Remove trailing dot(last charactter) of full string
        return "Version: %s" % version
    
    
    #returns latest version
    @staticmethod
    def current_version(version_model):
        latest_dict = version_model.objects.all().aggregate(Max("version"))     #get dict with highest version value
        latest = version_model.objects.get(version=latest_dict['version__max'])
        #extra **kwargs things?
        return latest
        
        


class SpawnOutskirt(models.Model):
    """ depending on difficulty has different basic spawnrates """
    
    difficulty = models.IntegerField(unique=True)                       #difficulties 1 to 18
    tier_1 = models.IntegerField()
    tier_2 = models.IntegerField()
    tier_3 = models.IntegerField()
    tier_4 = models.IntegerField()
    
    def __unicode__(self):
        return "Outskirt difficulty: %d" % self.difficulty
    
    
    #total value of all 3 fields
    def total_from_tiers(self):
        total = self.tier_1 + self.tier_2 + self.tier_3 + self.tier_4
        return total
    
    
    
    



############ Items #############
        
        
class Item(models.Model):
    """ Data every item has. No matter the shape or size """
    
    name = models.CharField(max_length=63, unique=True)
    description = models.TextField()
    volume = models.FloatField()
    
    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name
        


class Equipment(Item):
    """ Items a hero can equip """
    
    HAND = "hand"
    CHEST = "chest"
    TRINKET = "trinket"
    TRANSPORT = "transport"
    CATEGORIES = (
        (HAND, "Hand"),
        (CHEST, "Chest"),
        (TRINKET, "Trinket"),
        (TRANSPORT, "Transport"),
    )
    
    
    category = models.CharField(max_length=15, choices=CATEGORIES)
    
    hitpoints = models.IntegerField(default=0)
    critical = models.IntegerField(default=0)
    power = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    block = models.IntegerField(default=0)
    hit_chance = models.IntegerField(default=0)

    #Trading/Transport Stats
    speed = models.IntegerField(default=0)
    cargo = models.IntegerField(default=0)
    reputation = models.IntegerField(default=0)
    trade_orders = models.IntegerField(default=0)
    tax_reduction = models.IntegerField(default=0)
    contracts = models.IntegerField(default=0)

    #Craftin/Gathering
    crafting = models.IntegerField(default=0)
    efficiency = models.IntegerField(default=0)
    stamina = models.IntegerField(default=0)
    gathering = models.IntegerField(default=0)
    endurance = models.IntegerField(default=0)
    luck = models.IntegerField(default=0)






class Resource(Item):
    """ Basic (gatherable) items """
    
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3
    TIER_4 = 4
    TIERS = (
        (TIER_1, "Tier 1"),
        (TIER_2, "Tier 2"),
        (TIER_3, "Tier 3"),
        (TIER_4, "Tier 4"),
    )
    
    METAL = "metal"
    STONE = "stone"
    WOOD = "wood"
    ANIMAL = "animal"
    FOOD = "food"
    CATEGORIES = (
        (METAL, "Metal"),
        (STONE, "Stone"),
        (WOOD, "Wood"),
        (ANIMAL, "Animal"),
        (FOOD, "Food"),
    )
    
    category = models.CharField(max_length=15, choices=CATEGORIES)
    tier = models.IntegerField(choices=TIERS)
    location = models.CharField(max_length=31, unique=True)
    heroes_min = models.IntegerField()
    heroes_max = models.IntegerField()
    gather_speed = models.FloatField()                              #base speed of gathering this resource per hour
    stamina_cost = models.FloatField()                              #hunger costs per hour of gathering
    
    
    def __unicode__(self):
        return "%s(%s)" % (self.location, self.resource.name)

    
    #get random amount of heroes on 1 resource
    #TODO: maybe add ways to increase
    def random_heroes_on_resource(self):
        amount = random.randint(self.heroes_min, self.heroes_max)
        return amount
    
    
    
    
    
    
    
    
    

