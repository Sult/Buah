from django.db import models
from django.contrib.auth.models import User


#News flashs on index page
class NewsArticle(models.Model):
    """ News bulletins where body holds html code """
    
    title = models.CharField(max_length=63)
    body = models.TextField()
    
    made_by = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)                  #False willonly show when logged in
    
    def __unicode__(self):
        return "%s by %s" % (self.title, self.made_by)


    
    
    
    
