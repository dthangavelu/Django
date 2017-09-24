from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import bcrypt


# Create your models here.

class UserManager(models.Manager):
	def login_validator(self, postData):
		errors = {}		
		form_email = postData['email']	
		form_email = form_email.lower()
		form_pwd = postData['password']
		
		users = User.objects.filter(email = form_email)
		
		if users == []:
			errors['email'] = "Email not found in system. Please register!"			
		else:
			isCorrectPwd = bcrypt.checkpw( form_pwd.encode(), users[0].password.encode())			
			if isCorrectPwd == False:
				errors['password'] = "Invalid password. Please try again!"
		return errors		
		
class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)	
	password = models.CharField(max_length=255)	
	created_at = models.DateTimeField(auto_now_add=True)	
	updated_at = models.DateTimeField(default=datetime.now)
	#manager = UserManager()
	#objects = model.Manager()
	objects = UserManager()
	
	#def __repr__(self):
	#	return "\nfn: {} | ln: {} | email: {} | password: {}\n".format(self.first_name, self.last_name, self.email, self.password)