from django.db import models
#from taggit.managers import TaggableManager
from django.contrib.auth.models import User




    
    


#News flashs on index page
class Article(models.Model):
    """ Article baseclass for help pages and news """
    
    NEWS = "news"
    HEROES = "heroes"
    BUILDINGS = "buildings"
    ACTIVITIES = "activities"
    CATEGORIES = (
        (NEWS, "News"),
        (HEROES, "Heroes"),
        (BUILDINGS, "Buildings"),
        (ACTIVITIES, "Activities"),
    )
    
    category = models.CharField(max_length=31, choices=CATEGORIES)
    public = models.BooleanField(default=False)                         #False willonly show when logged in
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    #tags = TaggableManager()

    title = models.CharField(max_length=63)
    slug = models.SlugField()
    body = models.TextField()

    def __unicode__(self):
        return "%s by %s" % (self.title, self.made_by)

    
    
        
        
        
class ArticleImage(models.Model):
    """ Images (mostly used for articles) """
    
    article = models.ForeignKey(Article)
    image = models.ImageField(upload_to="articles", blank=True)
    


    
    




    
    
    
    
