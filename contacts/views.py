from django.shortcuts import render
from models import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# return None if new_name is invalid
# return the new user object otherwise
def insert_user(new_name, new_email):

	# check email validity
	try:
		validate_email(new_email)
	except ValidationError:
		return None

	# else add our new user
	if (new_name != None) and (new_email != None):
		new_user = Users(name=new_name, email=new_email)
		new_user.save()
		return new_user

	return None

# get a queryset of all users
def get_all_users():
	return Users.objects.filter()

# Get the user(s) of a given name
def get_users_by_name(find_name):
	find = Users.objects.filter(name=find_name)
	return find

# get the user of the given email
def get_users_by_email(find_email):
	find = Users.objects.filter(email=find_email)
	return find

# add the given contact to Contacts. Need a user_id at least
def add_contact(user_email, contact_name="", address="", phone="", email=""):
	if user_email == None:
		return None

	new_contact = Contacts(user_email=user_email, contact_name=contact_name, address=address, phone_number=phone, email=email)
	new_contact.save()
	return new_contact

# given the user email, return the contacts of that user email 
def get_contacts(user_email):
	find = Contacts.objects.filter(user_email=user_email)
	return find

# update the contact of id contact_id with the provided params
def update_contact(contact_id, contact_name="", address="", phone_number="", email=""):

	try:
		find = Contacts.objects.get(id=contact_id)
	except Contacts.DoesNotExist: 
		return None

	if (contact_name != ""):
		find.contact_name = contact_name
		find.save()
	if (address != ""):
		find.address = address
		find.save()
	if (address != ""):
		find.address = address
		find.save()
	if (phone_number != ""):
		find.phone_number = phone_number
		find.save()
	if (email != ""):
		find.email = email
		find.save()

	return find

# delete the contact of the given id
# return True if delete successful, false otherwise
def delete_contact(contact_id):

	try:
		find = Contacts.objects.get(id=contact_id)
	except Contacts.DoesNotExist: 
		return False

	find.delete()
	return True

# delete the user of the given email and all its contacts
# return True if delete successful, false otherwise
def delete_user(user_email):
	try:
		find = Users.objects.get(email=user_email)
	except Users.DoesNotExist: 
		return False

	contacts = get_contacts(user_email)
	
	for c in contacts:
		delete_contact(c.id)

	find.delete()
	return True