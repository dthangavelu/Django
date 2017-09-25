from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import bcrypt


# Create your models here.

class UserManager(models.Manager):
	def login_validator(self, postData):
		errors = {}		
		form_username = postData['username']			
		form_pwd = postData['password']
		
		users = User.objects.filter(username = form_username)
		
		if not users:
			errors['username'] = "Username not found in system. Please register!"			
		else:
			isCorrectPwd = bcrypt.checkpw( form_pwd.encode(), users[0].password.encode())			
			if isCorrectPwd == False:
				errors['password'] = "Invalid password. Please try again!"
		return errors	
		
		# if users == []:
			# errors['email'] = "Email not found in system. Please register!"			
		# else:
			# isCorrectPwd = bcrypt.checkpw( form_pwd.encode(), users[0].password.encode())			
			# if isCorrectPwd == False:
				# errors['password'] = "Invalid password. Please try again!"
		# return errors		
		
class User(models.Model):	
	name = models.CharField(max_length=255)	
	username = models.CharField(max_length=255, unique=True)	
	password = models.CharField(max_length=255)	
	created_at = models.DateTimeField(auto_now_add=True)	
	updated_at = models.DateTimeField(default=datetime.now)	
	objects = UserManager()
	
	def __repr__(self):
		return "\nfn: {} | ln: {} | email: {} | password: {}\n".format(self.first_name, self.last_name, self.email, self.password)
	
	
class TravelPlan(models.Model):
	destination = models.CharField(max_length=255)	
	travel_start_date = models.DateTimeField(auto_now=True)
	travel_end_date = models.DateTimeField(auto_now=True)
	travel_panned_by = models.ForeignKey(User, related_name = "planned_travel")
	joined_users = models.ManyToManyField(User, related_name="joined_travels")
	created_at = models.DateTimeField(auto_now_add=True)	
	updated_at = models.DateTimeField(default=datetime.now)	
	description = models.CharField(max_length=255, default="desc")
	
	def __repr__(self):
		return "\deatination: {} | start date: {} | end date: {} | userid: {}\n".format(self.destination, self.travel_start_date, self.travel_end_date, self.travel_panned_by)
	
	