from django.db import models
from django.db.models import get_model
from django.contrib.auth.models import User

from apps.elements.models import VersionControl

from datetime import datetime, timedelta
from django.utils.timezone import utc



class UserMathValues(VersionControl):
    """ holds the user balance controls. Startinggold, max maount of heroes etc """
    
    #starting values
    starting_munny = models.IntegerField()                          #(25k or something)
    
    #heroes
    heroes_owned_max = models.IntegerField()                                      #maximum owned heroes
    heroes_owned_per_level = models.FloatField()                                  #increases maximum owned heroes based on level
    heroes_active_max = models.IntegerField()                                     #Maximum heroes active on jobs
    heroes_active_per_level = models.FloatField()                                 #maximum active heroes increased by level
    
    
    




class Profile(models.Model):
    """ extender user profile that yields game related data like guild """
    
    user = models.OneToOneField(User, unique=True)
    
    #player relations
    #guild = models.ForeignKey("users.guild")
    #alliance = models.ForeignKey('users.alliance')
    
    #overalstats
    munny = models.FloatField()
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    
    def __unicode__(self):
        return self.user.username


######### CREATE NEW USER FUNCTION #################
    # create new profile
    @staticmethod
    def create_profile(user):
        user_values = UserMathValues.current_version(UserMathValues)
        profile = Profile.objects.create(
            user=user,
            munny=user_values.starting_munny,
        )
        # add starting heroes
        profile.create_starting_heroes()
        return profile
    
    
    #create the standard combat focused hero
    @staticmethod
    def get_hero_attributes_and_qualities(category, quality):
        statperlevel = get_model("heroes", "StatPerLevel")
        very_bad = statperlevel.VERY_BAD
        bad = statperlevel.BAD
        decent = statperlevel.DECENT
        good = statperlevel.GOOD
        if category == "combat":
            if quality == "good":
                return [["hitpoints", good], ["hit_chance", decent], ["power", decent], ["critical", bad], ["defense", decent], ["block", decent]]
            else:
                return [["hitpoints", decent], ["hit_chance", bad], ["power", bad], ["critical", very_bad], ["defense", bad], ["block", bad]]
        elif category == "trading":
            if quality == "good":
                return [["cargo", decent], ["reputation", decent], ["speed", good], ["trade_orders", decent], ["contracts", decent], ["tax_reduction", bad]]
            else:
                return [["cargo", bad], ["reputation", bad], ["speed", decent], ["trade_orders", bad], ["contracts", bad], ["tax_reduction", very_bad]]
        elif category == "crafting":
            if quality == "good":
                return [["crafting", good], ["efficiency", decent], ["stamina", bad], ["gathering", good], ["endurance", decent], ["luck", bad]]
            else:
                return [["crafting", decent], ["efficiency", bad], ["stamina", very_bad], ["gathering", decent], ["endurance", bad], ["luck", very_bad]]
    
    
    
    #create starting heroes (one of each category focused)
    def create_starting_heroes(self):
        warrior = [["combat", "good"], ["trading", "bad"], ["crafting", "bad"]]
        trader = [["combat", "bad"], ["trading", "good"], ["crafting", "bad"]]
        crafter = [["combat", "bad"], ["trading", "bad"], ["crafting", "good"]]
        heroes = [warrior, trader, crafter]
        town = get_model("towns", "Town").objects.get(name="Inverness")
        for hero in heroes:
            new = get_model("heroes", "Hero").objects.create()
            for category in hero:
                fields = self.get_hero_attributes_and_qualities(category[0], category[1])
                new.set_hero_starting_attributes(fields)
            
            #add user and other values
            new.user = self.user
            new.created = datetime.utcnow().replace(tzinfo=utc)
            new.town=town
            new.name = new.random_hero_name()
            new.hitpoints_current = new.total_hitpoints()
            new.stamina_current = new.total_stamina()
            new.save()


###### User modify functions    #############

    #update munny for player. value has always already taken into account the reputations
    #for paying munny make sure its a negative number
    #TODO: taxes to guild or tribe needs to be build
    def update_munny(self, munny):
        self.munny += munny
        self.save()
    
    
    #add xp to character
    #TODO: Possible bonus xp from who knows what
    def add_xp(self, amount):
        #check for possible bonuses/penalties
        self.xp += amount
        self.save()
    
    
    #Get maximum amount of heroes owned
    def maximum_owned_heroes(self):
        user_values = UserMathValues.current_version(UserMathValues)
        base = user_values.heroes_owned_max 
        from_levels = round(user_values.heroes_owned_per_level * self.level)
        print int(base + from_levels)
        return int(base + from_levels)
        
    
    #get maximum active heroes
    def maximum_active_heroes(self):
        user_values = UserMathValues.current_version(UserMathValues)
        base = user_values.heroes_active_max
        from_levels = round(user_values.heroes_active_per_level * self.level)
        return int(base + from_levels)
    
    
    #get current amount of active heroes    
    def active_heroes(self):
        return get_model("heroes", "Hero").objects.filter(user=self.user, active=True).count()
    
    
    #get owned heroes
    def owned_heroes(self):
        return get_model("heroes", "Hero").objects.filter(user=self.user).count()

    
    # see if you have room for another hero
    def new_hero_available(self):
        if self.owned_heroes() < self.maximum_owned_heroes():
            return True
        else:
            return False


    # see if player has enough munny to buy
    def has_enough_munny(self, value):
        if self.munny > value:
            return True
        else:
            return False





class Npc(models.Model):
    """ Non Playing Character. Can be used as questgivers town owners and more """
    
    name = models.CharField(max_length=31, unique=True)
    description = models.TextField(blank=True)
    tribe = models.ForeignKey('users.Tribe')
    
    def __unicode__(self):
        return "NPC: %s" % self.name

    
    
    
class Group(models.Model):
    """ Base for a group of players or NPCs """
    
    name = models.CharField(max_length=31, unique=True)
    description = models.TextField(blank=True)
    office = models.ForeignKey("towns.Town", null=True)
    
    class Meta:
        abstract = True
    


class Tribe(Group):
    """ The tribes are NPC groupes. They "own" the most of the lower difficulty town """
    
    CRAFTING = "crafting"
    TRADING = "trading"
    COMBAT = "combat"
    FOCUS = (
        (CRAFTING, "crafting"),
        (TRADING, "trading"),
        (COMBAT, "combat"),
    )
    
    leader = models.OneToOneField(Npc, null=True, related_name="+")
    likes = models.ForeignKey('self', related_name="+", null=True)
    hates = models.ForeignKey('self', related_name="+", null=True)
    focus = models.CharField(max_length=15, choices=FOCUS)



class Guild(models.Model):
    """ Guilds ingame """
    
    pass
    


class Alliance(models.Model):
    """ allaince is a coopperation between guilds """
    
    pass
