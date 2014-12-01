from django.db import models
from django.utils.timezone import utc
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist



class InventoryItem(models.Model):
    """ som shit bjorn gaat me uitleggen wat nuttig is hier """ 

    item = models.OneToOneField("elements.Item")
    amount = models.IntegerField()
    
    class Meta:
        abstract = True
    

        
    
    

class HeroInventory(models.Model):
    """ hero inventory space. Is limited by volume  """
    
    hero = models.OneToOneField("heroes.Hero")
    volume_current = models.FloatField()                        #as shortcut instead of calculations of possible hundreds to thousands of objects
    
    def __unicode__(self):
        return "Hero Inventory"
    
    #add a item to inventory (no autmatied stacking)
    def add_item(self, item, amount):
        #get volume to add 
        volume = item.volume * amount
        max_volume = self.hero.total_cargo_space()
        if self.volume_current + volume <= max_volume:
            HeroItem.objects.create(heroinventory=self, item=item, amount=amount)
            return True
        else:
            return False
    
    


class HeroItem(InventoryItem):
    """ items in a heroes inventory """
    
    heroinventory = models.ForeignKey("itemcontrol.HeroInventory")
    
    def __unicode__(self):
        return "%s. Item: %s" % (self.heroinventory.hero.name, self.item.name)
    
    
        

    


class Storehouse(models.Model):
    """ city storehouse """
    
    town = models.ForeignKey("towns.Town")
    user = models.OneToOneField(User)
    
    def __unicode__(self):
        return "%ss storehouse in %s " % (self.user.username, self.town.name)


    #add a item to inventory (no autmatied stacking)
    def add_item(self, item, amount):
        StorehouseItem.objects.create(storehouse=self, item=item, amount=amount)
        
    
    
    


class StorehouseItem(InventoryItem):
    """ meer bjorn spuugsel jeweetwel met ballen en haring """
    
    storehouse = models.ForeignKey("itemcontrol.Storehouse")
    
    def __unicode__(self):
        return "Storehouse item of %s" % self.storehouse.user.username
    
    
    








