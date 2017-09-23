from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)	
	created_at = models.DateTimeField(auto_now_add=True)	
	updated_at = models.DateTimeField(default=datetime.now)
		
	#def __repr__(self):
	#	return "\nfn: {} | ln: {} | email: {} | created_at: {} | updated_at: {}\n".format(self.first_name, self.last_name, self.email, self.created_at, self.updated_at)