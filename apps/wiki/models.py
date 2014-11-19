from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User



class Page(models.Model):
    """ a wiki page/article """
    
    title = models.CharField(max_length=31, unique=True)
    content = models.TextField()
    author = models.ForeignKey(User)
    tags = TaggableManager()
    
    def __unicode__(self):
        return self.title
        
        
    





