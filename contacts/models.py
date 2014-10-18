from django.db import models

class Users(models.Model):
	name = models.CharField(max_length=30)
	email = models.EmailField(primary_key=True)

class Contacts(models.Model):
	# user_email serves as the link between a Contact and User entry
	user_email = models.EmailField()
	# the actual contact info
	contact_name = models.CharField(max_length=30)
	address = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=30)
	email = models.EmailField()
