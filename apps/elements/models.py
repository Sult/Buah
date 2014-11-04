from django.db import models
from django.db.models import Max                #to get a maxvalue in queryset



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
        
        
       
       
        
        
class Item(models.Model):
    """ Data every item has. No matter the shape or size """
    
    name = models.CharField(max_length=63)
    description = models.TextField()
    level = models.IntegerField()
    volume = models.FloatField()
    item_weight = models.FloatField()
    
    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name




class WarriorEquipment(Item):
    """ Items a warrior hero can equip """
    
    WEAPON = "weapon"
    ARMOR = "armor"
    SHIELD = "shield"
    WARRIORSLOTS = (
        (WEAPON, "Weapon"),
        (ARMOR, "Armor"),
        (SHIELD, "Shield"),
    )

    slot = models.CharField(max_length=15, choices=WARRIORSLOTS)
    
    #warrior
    strength = models.IntegerField(default=0)
    hitpoints = models.IntegerField(default=0)
    critical = models.IntegerField(default=0)
    power = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    block = models.IntegerField(default=0)
    hit_chance = models.IntegerField(default=0)
    
    
    
    
    
    


class TraderEquipment(Item):
    """ equipment for a trader hero """
    
    TRANSPORT = "transport"
    DOCUMENT = "document"
    AMULET = "amulet"
    TRADERSLOTS = (
        (TRANSPORT, "Transport"),
        (DOCUMENT, "Document"),
        (AMULET, "Amulet"),
    )
    
    slot = models.CharField(max_length=15, choices=TRADERSLOTS)
    #trader
    charisma = models.IntegerField(default=0)
    movement_speed = models.IntegerField(default=0)
    cargo = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    trade_orders = models.IntegerField(default=0)
    tax_reduction = models.IntegerField(default=0)
    contracts = models.IntegerField(default=0)
    
    
    
    
class CrafterEquipment(Item):
    """ Items a crafter hero can equip """
    
    TOOL = "tool"
    COMPENDIUM = "compendium"
    TRINKET = "trinket"
    CRAFTERSLOTS = (
        (TOOL, "Tool"),
        (COMPENDIUM, "Compendium"),
        (TRINKET, "Trinket"),
    )
    
    slot = models.CharField(max_length=15, choices=CRAFTERSLOTS)
    #crafter
    wisdom = models.IntegerField(default=0)
    crafting_speed = models.IntegerField(default=0)
    efficiency = models.IntegerField(default=0)
    multitasking = models.IntegerField(default=0)
    gathering_speed = models.IntegerField(default=0)
    endurance = models.IntegerField(default=0)
    luck = models.IntegerField(default=0)




