from django.db import models
 

class SecurityKeymodel(models.Model):
    email= models.EmailField( max_length=254)       #signupemail
    securitykey= models.BigIntegerField()
    def __str__(self):
        return self.email


class UserComplaint(models.Model):
    datetime = models.DateTimeField(auto_now_add=False, auto_now=True)
    email= models.EmailField( max_length=254)       
    hostel= models.TextField()
    block= models.CharField( max_length=2)
    floor= models.SmallIntegerField()
    roomno= models.SmallIntegerField()
    cmplnttype= models.TextField()
    complaint= models.TextField()
    class Meta:
        ordering = ['-datetime']
    def __str__(self):
        return self.cmplnttype 

class UserMessFeedback(models.Model):
    datetime = models.DateTimeField(auto_now_add=False, auto_now=True)
    email= models.EmailField( max_length=254)       
    hostel= models.CharField( max_length=20)
    block= models.CharField( max_length=5)
    floor= models.SmallIntegerField()
    hygieneissue=  models.CharField( max_length=20)
    hygieneissueTXT= models.TextField(default="")
    qualityissue=  models.CharField( max_length=20)
    qualityissueTXT= models.TextField(default="")
    messrating= models.SmallIntegerField()
    suggestions= models.TextField(default="")
    class Meta:
        ordering = ['-datetime']
    def __str__(self):
        return str(self.messrating)    

class NewsEvents(models.Model):
    date = models.DateField( auto_now=False, auto_now_add=False)
    event= models.TextField()
    details= models.TextField()
    class Meta:
        ordering = ['-date']
    def __str__(self):
        return self.event              

    
    
# Create your models here.
