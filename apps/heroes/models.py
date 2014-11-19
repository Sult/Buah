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
    
    #base values
    base_stamina = models.IntegerField()                    #base stamina of a hero (used for calculating max stamina)
    base_hitpoints = models.IntegerField()                  #base hitpoints (increased by heroes hitpoints stat
    
    
    #hero % per point
    hitpoints_per_point = models.FloatField()
    critical_per_point = models.FloatField()
    power_per_point = models.FloatField()
    defense_per_point = models.FloatField()
    block_per_point = models.FloatField()
    hit_chance_per_point = models.FloatField()

    #Trading/Transport Stats
    speed_per_point = models.FloatField()
    cargo_per_point = models.FloatField()
    reputation_per_point = models.FloatField()
    trade_orders_per_point = models.FloatField()
    tax_reduction_per_point = models.FloatField()
    contracts_per_point = models.FloatField()

    #Craftin/Gathering
    crafting_per_point = models.FloatField()
    efficiency_per_point= models.FloatField()
    stamina_per_point = models.FloatField()
    gathering_per_point = models.FloatField()
    endurance_per_point = models.FloatField()
    luck_per_point = models.FloatField()

    
    



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
    SPEED = "speed"
    CARGO = "cargo"                             #volume increase
    REPUTATION = "reputation"                           
    TRADE_ORDERS = "trade_orders"
    TAX_REDUCTION = "tax_reduction"
    CONTRACTS = "contracts"
    #Crafter Attributes
    #WISDOM = "wisdom"
    CRAFTING = "crafting"
    EFFICIENCY = "efficiency"
    STAMINA = "stamina"
    GATHERING = "gathering"
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
        (SPEED, "Speed"),
        (CARGO, "Cargo"),
        (REPUTATION, "Reputation"),
        (TRADE_ORDERS, "Trade Orders"),
        (TAX_REDUCTION, "Tax Reduction"),
        (CONTRACTS, "Contracts"),
        #(WISDOM, "Wisdom"),
        (CRAFTING, "Crafting"),
        (EFFICIENCY, "Efficiency"),
        (STAMINA, "Stamina"),
        (GATHERING, "Gathering"),
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
    speed = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    cargo = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    reputation = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    trade_orders = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    tax_reduction = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    contracts = models.ForeignKey(StatPerLevel, null=True, related_name="+")

    #Craftin/Gathering
    crafting = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    efficiency = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    stamina = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    gathering = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    endurance = models.ForeignKey(StatPerLevel, null=True, related_name="+")
    luck = models.ForeignKey(StatPerLevel, null=True, related_name="+")

    #job attributes
    active = models.BooleanField(default=False)
    
    #items
    hand = models.OneToOneField("elements.Equipment", related_name="+", null=True)
    chest = models.OneToOneField("elements.Equipment", related_name="+", null=True)
    trinket = models.OneToOneField("elements.Equipment", related_name="+", null=True)
    transport = models.OneToOneField("elements.Equipment", related_name="+", null=True)
    
    
    
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
        fields = ["cargo", "reputation", "speed", "trade_orders", "contracts", "tax_reduction"]
        return fields
    
    #retun fields relatedtocrafting and gathering
    @staticmethod
    def craft_attributes():
        fields = ["crafting", "efficiency", "stamina", "gathering", "endurance", "luck"]
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
            
        
######### Attribute Functions ############################
    #get item bonus from 1 item
    def item_bonus(self, item_slot, attribute):
        try:
            return getattr(getattr(self, item_slot), attribute)
        #no item equiped returns no bonus
        except AttributeError:
            return 0
    
    
    #get the attribute bonus from all items
    def total_item_bonus(self, attribute):
        item_slots = ["hand", "chest", "trinket", "transport"]
        total = 0
        for item_slot in item_slots:
            total += self.item_bonus(item_slot, attribute)
        
        return total
        
    
    # get percentage increase from attribute
    def percentage_bonus(self, attribute):
        hero_values = HeroMathValues.current_version(HeroMathValues)
        item_score = self.total_item_bonus(attribute)
        total_score = getattr(self, attribute).level_score(self.level) + item_score
    
        bonus = getattr(hero_values, attribute + "_per_point") * total_score
        #convert bonus to a % modifier (like 32 to 1.32)
        percent_bonus = 1 + bonus / 100
        return percent_bonus
    
    
    #convert positive (increase) bonuse to negative (reduce) bonus
    def negative_percentage_bonus(self, attribute):
        positive_bonus = self.percentage_bonus(attribute)
        #convert te negative bonus (gets cheaper)
        bonus = 1 - (positive_bonus - 1)
        return bonus
    
    
    #calculates the amount of resources gathered in 1 hour
    def gather_income(self, gather_speed, quality):
        #get hero gethering modifier
        gather_bonus = self.percentage_bonus("gathering")
        #speed_bonus = hero.percentage_bonus("gathering")
        income = gather_speed * quality * gather_bonus 
        return income
        
    
    #get current stamina
    def total_stamina(self):
        hero_values = HeroMathValues.current_version(HeroMathValues)
        stamina_bonus = self.percentage_bonus("stamina")
        total = hero_values.base_stamina * stamina_bonus
        return total
    
    
    #stamina cost per hour of working
    def stamina_loss(self, stamina_cost):
        modifier = self.negative_percentage_bonus("endurance")
        cost = stamina_cost * modifier
        return cost
    
        
    

##### Form timer functions ##############
    #get max time (minutes) possible with current stamina
    def max_time_with_stamina(self, stamina_cost):
        stamina = self.total_stamina()
        stamina_loss = self.stamina_loss(stamina_cost) / 60
        if stamina_loss == 0:
            return 9999999
        return stamina / stamina_loss

        
        
        
        


    
    
