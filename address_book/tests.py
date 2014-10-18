# from django.test import TestCase
import unittest
from django.test.client import Client

# from contacts.models import *
# import contacts.views as contacts

from views import *
import json

class test_users(unittest.TestCase):

	# try to get all users
	def test_get_all_users(self):

		c = Client()
		# a get with no argument should retrieve all users
		response = c.get('/users/')

		# json dump our response
		j_obj = json.loads(response.content)

		# a little unsure about how robust this test is, may need fixing
		self.assertEqual(len(j_obj), len(contacts.get_all_users()))

		# want a 200 response code
		self.assertEqual(response.status_code, 200)

	# try to get a user by email
	def test_get_user_by_email(self):
		c = Client()
		# a get with an email arg should retrieve that user
		email_to_get = "Spongebob@bikinibottom.com"
		response = c.get('/users/?mail='+ email_to_get)

		# json dump our response
		j_obj = json.loads(response.content)

		self.assertEqual(j_obj[0]["name"], "Spongebob")
		# want a 200 response code
		self.assertEqual(response.status_code, 200)

	# try to add an improperly formed user
	def test_add_user_fail(self):
		c = Client()
		# our new credentials
		new_name = "Sherlock Holmes"
		new_email = "sherlotlandyardca"
		# post our new user to the server
		response = c.post('/users/', {'name': new_name, 'email': new_email})
		# want a 401 error response code
		self.assertEqual(response.status_code, 401)
	
	# try to add a new user
	def test_add_user(self):
		c = Client()
		# our new credentials
		new_name = "Sherlock Holmes"
		new_email = "sherlockholmes@scotlandyard.ca"
		# post our new user to the server
		response = c.post('/users/', {'name': new_name, 'email': new_email})
		# want a 200 response code
		self.assertEqual(response.status_code, 200)

class test_contacts(unittest.TestCase):

	# get all the contacts of a user
	def test_get_contacts(self):
		# insert a user
		name = "Jack Reacher"
		email = "jack.reacher@usarmy.com"
		inserted_user = contacts.insert_user(name, email)

		# insert two different contacts
		contacts.add_contact(email, "A", "123 Fake Street", "12341", "hi@bye.com")
		contacts.add_contact(email, "B", "444 Fake Street", "55555", "hiya@bye.com")

		# try to get the new contacts using a get
		c = Client()
		# a get with an email arg should retrieve that user
		response = c.get('/contacts/?mail='+ email)

		# json dump our response
		j_obj = json.loads(response.content)

		self.assertEqual(j_obj[0]["contact_name"], "A")
		self.assertEqual(j_obj[1]["contact_name"], "B")

		self.assertEqual(j_obj[0]["address"], "123 Fake Street")
		self.assertEqual(j_obj[1]["address"], "444 Fake Street")

		self.assertEqual(j_obj[0]["phone_number"], "12341")
		self.assertEqual(j_obj[1]["phone_number"], "55555")

		self.assertEqual(j_obj[0]["email"], "hi@bye.com")
		self.assertEqual(j_obj[1]["email"], "hiya@bye.com")

		# want a 200 response code
		self.assertEqual(response.status_code, 200)

