from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Dojo(models.Model):
	name = models.CharField(max_length=255)
	city = models.CharField(max_length=255)
	state = models.CharField(max_length=2)
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __repr__(self):
		return "\nname: {} | city: {} | state: {} | created_at: {} | updated_at: {}\n".format(self.name, self.city, self.state, self.created_at, self.updated_at)

class Ninja(models.Model):
	first_name = models.CharField(max_length=255, null=True)
	last_name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	dojo = models.ForeignKey(Dojo, related_name="ninjas")
	
	def __repr__(self):
		return "\nfn: {} | ln: {} | dojo_id: {} | created_at: {} | updated_at: {}\n".format(self.first_name, self.last_name, self.dojo, self.created_at, self.updated_at)