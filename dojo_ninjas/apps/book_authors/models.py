from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.
class Book(models.Model):
	name = models.CharField(max_length=255)	
	desc = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now_add=True)	
	#updated_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(default=datetime.now)
	
	def __repr__(self):
		return "\title: {} | desc: {} | created_at: {} | updated_at: {}\n".format(self.name, self.desc, self.created_at, self.updated_at)
		
		
class Author(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	notes = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	#updated_at = models.DateTimeField(auto_now=True, default=datetime.now)
	updated_at = models.DateTimeField(default=datetime.now)
	books = models.ManyToManyField(Book, related_name="authors")
	
	def __repr__(self):
		return "\nfn: {} | ln: {} | email: {} | created_at: {} | updated_at: {}\n".format(self.first_name, self.last_name, self.email, self.created_at, self.updated_at)