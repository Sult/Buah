from django.db import models
from django.utils.timezone import utc
from django.contrib.auth.models import User
#from django.template import defaultfilters


from apps.elements.models import VersionControl
#import apps.towns.models as apps_towns

import random
from collections import OrderedDict, namedtuple
from datetime import datetime, timedelta


class HeroMathValues(VersionControl):
    """ Holds numbers used in hero related equations and functions. to balance and provide a smooth system """
    
    #hero creation
    pass
    



class HeroName(models.Model):
    """ list of random names to give heroes """
    
    name = models.CharField(max_length=63)
    
    def __unicode__(self):
        return self.name




class StatPerLevel(models.Model):
    """ to calculate stats per level """
    
    VERY_BAD = "very_bad"
    BAD = "bad"
    DECENT = "decent"
    GOOD = "good"
    EXCELLENT = "excellent"
    QUALITY = (
        (VERY_BAD, "Very Bad"),
        (BAD, "Bad"),
        (DECENT, "Decent"),
        (GOOD, "Good"),
        (EXCELLENT, "Excellent"),
    )

    #Warrior Attributes
    #STRENGTH = "strength"
    HITPOINTS = "hitpoints"
    CRITICAL = "critical"
    POWER = "power"
    DEFENSE = "defense"
    BLOCK = "block"
    HIT_CHANCE = "hit_chance"
    #Trader Attributes
    #CHARISMA = "charisma"
    MOVEMENT_SPEED = "movement_speed"
    CARGO = "cargo"
    WEIGHT = "weight"
    TRADE_ORDERS = "trade_orders"
    TAX_REDUCTION = "tax_reduction"
    CONTRACTS = "contracts"
    #Crafter Attributes
    #WISDOM = "wisdom"
    CRAFTING_SPEED = "crafting_speed"
    EFFICIENCY = "efficiency"
    MULTITASKING = "multitasking"
    GATHERING_SPEED = "gathering_speed"
    ENDURANCE = "endurance"
    LUCK = "luck"
    ATTRIBUTES = (
        #(STRENGTH, "Strength"),
        (HITPOINTS, "Hitpoints"),
        (CRITICAL, "Critical"),
        (POWER, "Power"),
        (DEFENSE, "Defense"),
        (BLOCK, "Block"),
        (HIT_CHANCE, "Hit Chance"),
        #(CHARISMA, "Charisma"),
        (MOVEMENT_SPEED, "Movement Speed"),
        (CARGO, "Cargo"),
        (WEIGHT, "Weight"),
        (TRADE_ORDERS, "Trade Orders"),
        (TAX_REDUCTION, "Tax Reduction"),
        (CONTRACTS, "Contracts"),
        #(WISDOM, "Wisdom"),
        (CRAFTING_SPEED, "Crafting Speed"),
        (EFFICIENCY, "Efficiency"),
        (MULTITASKING, "Multitasking"),
        (GATHERING_SPEED, "Gathering Speed"),
        (ENDURANCE, "Endurance"),
        (LUCK, "Luck"),
    )
    
    quality = models.CharField(max_length=31, choices=QUALITY)
    attribute = models.CharField(max_length=31, choices=ATTRIBUTES)
    start_value = models.IntegerField()
    multiplier = models.FloatField()
    level_bonus = models.FloatField()
    
    class Meta:
        unique_together = ["quality", "attribute"]
        
    
    def __unicode__(self):
        return "%s: %s" % (self.attribute, self.quality)
    
    
    #calculate score based on hero level
    def level_score(self, level):
        sum_level = level * (level + 1) / 2                         # 1 + 2 + 3 +.... +n
        bonus_level = self.level_bonus * level
        result =  int(round((sum_level + bonus_level) * self.multiplier + self.start_value, 0))
        return result
    




class Hero(models.Model):
    """ player heroes. Used to perform allsorts of actions """
    
    #general stats
    name = models.CharField(max_length=63, blank=True)
    town = models.ForeignKey('towns.Town', null=True)    
    user = models.ForeignKey(User, null=True)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    created = models.DateTimeField(null=True)
    
    #Combat Stats
    hitpoints = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    critical = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    power = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    defense = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    block = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    hit_chance = models.ForeignKey(StatPerLevel, null=True, related_name="+")

    #Trading/Transport Stats
    movement_speed = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    cargo = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    weight = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    trade_orders = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    tax_reduction = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    contracts = models.ForeignKey(StatPerLevel, null=True, related_name="+")

    #Craftin/Gathering
    crafting_speed = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    efficiency = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    multitasking = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    gathering_speed = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    endurance = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    luck = models.ForeignKey(StatPerLevel, null=True, related_name="+")

    #job attributes
    active = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "Hero"
    
    
    #return fields related to combat
    @staticmethod
    def combat_attributes():
        fields = ["hitpoints", "hit_chance", "power", "critical", "defense", "block"]
        return fields
    
    
    #return fields related to trade and transport
    @staticmethod
    def trade_attributes():
        fields = ["cargo", "weight", "movement_speed", "trade_orders", "contracts", "tax_reduction"]
        return fields
    
    #retun fields relatedtocrafting and gathering
    @staticmethod
    def craft_attributes():
        fields = ["crafting_speed", "efficiency", "multitasking", "gathering_speed", "endurance", "luck"]
        return fields
        
    #returns all attribute fields
    @staticmethod
    def all_attributes_fields():
        combat = Hero.combat_attributes()
        trade = Hero.trade_attributes()
        craft = Hero.craft_attributes()
        return combat + trade + craft
    
    
    
############ HERO CREATION #################
    
    #return a random StatsPerLevel object based on attribute
    @staticmethod
    def random_quality(attribute):
        stat = StatPerLevel.objects.filter(attribute=attribute).order_by("?")[0]
        return stat

    
    #get a random hero name
    @staticmethod
    def random_hero_name():
        return HeroName.objects.all().order_by("?")[0].name
    
    
    #Generate a random hero template
    #These will be used as buyable objects in a tavern. And will be the source of player actions
    @staticmethod
    def create_random_hero():
        all_attributes = Hero.all_attributes_fields()
        hero = Hero.objects.create()
        
        for field in all_attributes:
            setattr(hero, field, Hero.random_quality(field))
        
        hero.save()
        return hero
    
    
    # set a combination of fields+ values for a new hero
    # example of fields: [["crafting_speed", decent], ["efficiency", bad], ["multitasking", ver_bad], ["gathering_speed", decent], ["endurance", bad], ["luck", very_bad]]
    def set_hero_starting_attributes(self, fields):
        for field in fields:
            value = StatPerLevel.objects.get(attribute=field[0], quality=field[1])
            setattr(self, field[0], value)
        self.save()
        

####### HERO VIEW FUNCTIONS ###########
    #get attribute value
    @staticmethod
    def get_attribute_scores():
        scores = {}
        scores[StatPerLevel.VERY_BAD] = -2
        scores[StatPerLevel.BAD] = -1
        scores[StatPerLevel.DECENT] = 0 
        scores[StatPerLevel.GOOD] = 1
        scores[StatPerLevel.EXCELLENT] = 2
        return scores
        
        
    #simplified quality view for a hero. (only categories are combat/trade/construction
    def get_category_score(self, category):
        if category == "combat":
            fields = self.combat_attributes()
        elif category == "trade":
            fields = self.trade_attributes()
        elif category == "crafting":
            fields = self.craft_attributes()
        
        scores = self.get_attribute_scores()
        total = 0
        for field in fields:
            total += scores[getattr(self, field).quality]
        
        return total
    
    
    #convert the score into a readable quality
    @staticmethod
    def view_category_score(score):
        if score < -7:
            return "Very Bad"
        elif score > -8 and score < -2:
            return "Bad"
        elif score > -3 and score < 3:
            return "Decent"
        elif score > 2 and score < 8:
            return "Good"
        elif score > 7:
            return "Excellent"
        else:
            return "Foutjes"
    

    # View combat score in template
    def view_combat_score(self):
        return self.view_category_score(self.get_category_score("combat"))
    
    # view trading score in template
    def view_trade_score(self):
        return self.view_category_score(self.get_category_score("trade"))
    
    #view crafting score in template
    def view_crafting_score(self):
        return self.view_category_score(self.get_category_score("crafting"))
            
                    
    # returns an ordered dictionary with the fields as keys and corrosponding values
    def get_attribute_values(self, fields):
        combat_list = OrderedDict()
        for field in fields:
            key = field.replace("_", " ")
            combat_list[key.title()] = getattr(self, field)
        return combat_list

    
    
    
    #returns a list of namedtuples for combat/trading/crafting stats
    def view_hero_attributes(self):
        HeroAttributes = namedtuple("HeroAttributes", "category, values")
        categories = ["combat", "trade", "craft"]
        hero_attributes = []
        
        for category in categories:
            fields = getattr(self, category + "_attributes")()
            values = self.get_attribute_values(fields)
            hero_attributes.append(HeroAttributes(category=category, values=values))
        
        return hero_attributes
            
        
    #def created_shortdate(self):
        #return defaultfilters.date(self.created, "SHORT_DATETIME_FORMAT")
        
        
        
        
        
        
        
        
        
        


    
    
