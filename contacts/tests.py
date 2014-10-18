# from django.test import TestCase
import unittest
from contacts.models import *
from contacts.views import *

class test_insert_user(unittest.TestCase):
    
	def test_insert_normal_name(self):
		name = "John Fletcher"
		email = "john.fletcher@fake.com"
		inserted_user = insert_user(name, email)
		self.assertEqual(inserted_user.name, name)
		self.assertEqual(inserted_user.email, email)

	def test_insert_nil_name(self):
		new_fail_user = insert_user(None, None)
		self.assertEqual(new_fail_user, None)

		new_fail_user = insert_user("Bob", None)
		self.assertEqual(new_fail_user, None)

		new_fail_user = insert_user(None, "Bob@bobemail.com")
		self.assertEqual(new_fail_user, None)

	def test_insert_bad_email(self):
		new_fail_user = insert_user("Bob", "asdfsadfsda")
		self.assertEqual(new_fail_user, None)

class test_get_users(unittest.TestCase):

	# try to find the one user of a given name
	def test_get_email_in_db(self):
		name = "Dan Noven"
		email = "dannoven@gmail.com"
		insert_user(name, email)
		find_user = get_users_by_email(email)
		# should only return a size 1 querySet
		self.assertEqual(len(find_user), 1)
		# get_users returns a querySet, so test the name and email of the first element
		self.assertEqual(name, find_user[0].name)
		self.assertEqual(email, find_user[0].email)

	# try to get a set of users of a given name
	def test_many_names_in_db(self):
		name_1 = "John Smith"
		email_1 = "johnjacobsmith@gmail.com"
		name_2 = "John Smith"
		email_2 = "johnsmith@fake.ca"
		insert_user(name_1, email_1)
		insert_user(name_2, email_2)
		find_users = get_users_by_name("John Smith")
		# Should only return a size two querySet
		self.assertEqual(len(find_users), 2)
		self.assertEqual(name_1, find_users[0].name)
		self.assertEqual(name_2, find_users[1].name)

	# find a name not in db
	def test_name_not_in_db(self):
		find_users = get_users_by_name("asdfsdafsadfsda")
		self.assertEqual(len(find_users), 0)

	def test_get_all_users(self):
		users = get_all_users()
		self.assertEqual(len(users), 4)

class test_contact_insert(unittest.TestCase):

	def test_add_bad_contact(self):
		self.assertEqual(None, add_contact(None))

	def test_add_basic_contact(self):
		new_user_name = "Pyramid Head"
		new_user_email = "pyramidhead@silenthill.com"
		insert_user(new_user_name, new_user_email)
		new_contact = add_contact(new_user_email)
		self.assertEqual(new_contact.user_email, new_user_email)
		self.assertEqual(new_contact.contact_name, "")
		self.assertEqual(new_contact.address, "")
		self.assertEqual(new_contact.phone_number, "")
		self.assertEqual(new_contact.email, "")

	def test_add_normal_contact(self):

		new_user_name = "Spiderman"
		new_user_email = "spiderman@uncleben.com"
		insert_user(new_user_name, new_user_email)

		new_contact = add_contact(new_user_email, "John", "123 Fake Street", "12341", "hi@bye.com")
		self.assertEqual(new_contact.user_email, new_user_email)
		self.assertEqual(new_contact.contact_name, "John")
		self.assertEqual(new_contact.address, "123 Fake Street")
		self.assertEqual(new_contact.phone_number, "12341")
		self.assertEqual(new_contact.email, "hi@bye.com")

class test_get_contacts(unittest.TestCase):

	# get the contacts of someone not in the db
	def test_get_contacts_not_in_db(self):
		self.assertEqual(0, len(get_contacts("asdfsdafsadfsda")))

	def test_get_contacts(self):
		# add a new user Spongebob to the db
		new_user_name = "Spongebob"
		new_user_email = "Spongebob@bikinibottom.com"
		insert_user(new_user_name, new_user_email)

		# add two contacts for Spongebob
		add_contact(new_user_email, "John", "123 Fake Street", "12341", "hi@bye.com")
		add_contact(new_user_email, "Jill", "123 Genel Ct", "647555879", "jill@fake.ca")

		# get the contacts for spongebob
		contacts = get_contacts(new_user_email)

		# hopefully we receive two contacts
		self.assertEqual(len(contacts), 2)
		
		# check the first contact's values
		first = contacts[0]
		self.assertEqual(first.contact_name, "John")
		self.assertEqual(first.address, "123 Fake Street")
		self.assertEqual(first.phone_number, "12341")
		self.assertEqual(first.email, "hi@bye.com")

		# check the second contact's values
		second = contacts[1]
		self.assertEqual(second.contact_name, "Jill")
		self.assertEqual(second.address, "123 Genel Ct")
		self.assertEqual(second.phone_number, "647555879")
		self.assertEqual(second.email, "jill@fake.ca")

class test_update_contants(unittest.TestCase):

	# try to update a contact not in the db
	def test_update_contact_not_in_db(self):
		updated_contact = update_contact(-1, "Eggs")
		self.assertEqual(None, updated_contact)

	def test_update_contact(self):
		# add a new user Patrick to the db
		new_user_name = "Patrick"
		new_user_email = "Patrick@bikinibottom.com"
		insert_user(new_user_name, new_user_email)

		# add a contact for Patrick
		add_contact(new_user_email, "John", "123 Fake Street", "12341", "hi@bye.com")

		# get the list of contacts for Patrick
		contacts = get_contacts(new_user_email)

		# get the id of the first contact 
		contact_id = contacts[0].id

		# update our contact name to be "Squidward"
		updated_contact = update_contact(contact_id, "Squidward")
		# check our updated contact
		self.assertEqual(updated_contact.contact_name, "Squidward")

		# repeat this for the other values, ensuring that that other fields weren't
		# inadvertently changed

		# update address
		updated_contact = update_contact(contact_id,"","2 Bikinibottom Ct")
		self.assertEqual(updated_contact.contact_name, "Squidward")
		self.assertEqual(updated_contact.address, "2 Bikinibottom Ct")

		# update phone
		updated_contact = update_contact(contact_id,"","", "1+555-8496")
		self.assertEqual(updated_contact.contact_name, "Squidward")
		self.assertEqual(updated_contact.address, "2 Bikinibottom Ct")
		self.assertEqual(updated_contact.phone_number, "1+555-8496")

		# update email
		updated_contact = update_contact(contact_id,"","", "", "squidward@bikinibottom.com")
		self.assertEqual(updated_contact.contact_name, "Squidward")
		self.assertEqual(updated_contact.address, "2 Bikinibottom Ct")
		self.assertEqual(updated_contact.phone_number, "1+555-8496")
		self.assertEqual(updated_contact.email, "squidward@bikinibottom.com")

class test_delete_contact(unittest.TestCase):

	def test_delete_contact_not_in_db(self):
		former_contact = delete_contact(-1)
		self.assertEqual(False, former_contact)

	def test_delete_contact(self):
		# add a new user Sandy to the db
		new_user_name = "Sandy"
		new_user_email = "Sandy@bikinibottom.com"
		insert_user(new_user_name, new_user_email)

		# add a contact for Sandy
		contacts = add_contact(new_user_email, "John", "123 Fake Street", "12341", "hi@bye.com")

		# get the id of the contact 
		contact_id = contacts.id

		# delete the contact
		delete_contact(contact_id)

		# try to find the deleted contact
		contacts = get_contacts(new_user_email)

		# should be empty
		self.assertEqual(0, len(contacts))

class test_delete_user(unittest.TestCase):

	def test_delete_user_not_in_db(self):
		former_user = delete_user("not_in_db.email.com")
		self.assertEqual(False, former_user)

	def test_delete_user_with_no_contacts(self):
		# add a new user Plankton to the db
		new_user_name = "Plankton"
		new_user_email = "Plankton@bikinibottom.com"
		insert_user(new_user_name, new_user_email)

		# delete the user and its contacts
		delete_user(new_user_email)

		# check the user has no contacts in db
		self.assertEqual(0, len(get_contacts(new_user_email)))

		# check the user has no entry in Users db
		self.assertEqual(0, len(get_users_by_email(new_user_email)))

	def test_delete_user_with_contacts(self):
		# add a new user Plankton to the db
		new_user_name = "Plankton"
		new_user_email = "Plankton@bikinibottom.com"
		insert_user(new_user_name, new_user_email)

		# add contacts for Plankton
		add_contact(new_user_email, "John", "123 Fake Street", "12341", "hi@bye.com")
		add_contact(new_user_email, "Jill", "123 Fake Street", "12341", "hi@bye.com")

		# delete the user and its contacts
		delete_user(new_user_email)

		# check the user has no contacts in db
		self.assertEqual(0, len(get_contacts(new_user_email)))

		# check the user has no entry in Users db
		self.assertEqual(0, len(get_users_by_email(new_user_email)))
