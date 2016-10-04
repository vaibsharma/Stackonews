from django.db import models

# Create your models here.
class Check(models.Model):
	status = models.CharField(max_length=128,unique = True)
	
	def __unicode__(self):
		return self.status