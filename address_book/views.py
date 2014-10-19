from django.http import HttpResponse
import contacts.views as contacts
import json

# methods relating to the Users table
def users(request):
	# GET gets some user or all users
	if request.method == "GET":
		req_mail = request.GET.get('mail', '')

		# if no email supplied, get all users
		if (req_mail == ''):
			find_user = contacts.get_all_users()
			ret = user_to_json(find_user)

		# otherwise find the specified user
		else:
			find_user = contacts.get_users_by_email(req_mail)
			ret = user_to_json(find_user)

		return HttpResponse(json.dumps(ret), content_type="application/json")

	# POST adds a new user
	if request.method == "POST":
		# name and email are in the post payload
		name = request.POST["name"]
		email = request.POST["email"]
		ret = contacts.insert_user(name, email)
		
		# if insertion failed return error code
		if ret == None:
			return HttpResponse(status=401)
		# valid insert
		else:
			return HttpResponse(status=200)

# methods relating to the Contacts table
def address_contacts(request):
	# GET gets some contact
	if request.method == "GET":
		req_mail = request.GET.get('mail', '')

		# no email supplied, throw error
		if (req_mail == ''):
			return HttpResponse(status=401)
			
		else:
			# find the given contact
			find_contacts = contacts.get_contacts(req_mail)
			# parse it
			ret = contacts_to_json(find_contacts)
			# return it
			return HttpResponse(json.dumps(ret), content_type="application/json")

	# adding some contact
	if request.method == "POST":
		# data is in the post payload
		user_email = request.POST["user_email"]
		contact_name = request.POST["contact_name"]
		address = request.POST["address"]
		phone_number = request.POST["phone_number"]
		email = request.POST["email"]

		ret = contacts.add_contact(user_email, contact_name, address, phone_number, email)
		
		# if insertion failed return error code
		if ret == None:
			return HttpResponse(status=401)
		# valid insert
		else:
			return HttpResponse(status=200)

# given a Contacts QuerySet, return that QuerySet in dictionary format
def contacts_to_json(find_user):
	d = {}
	ret = []
	# querySet can't be serialized so convert
	# it to a dictionary

	for x in range(len(find_user)):
		# user_email=user_email, contact_name=contact_name, address=address, phone_number=phone, email
		d["contact_name"] = find_user[x].contact_name
		d["address"] = find_user[x].address
		d["phone_number"] = find_user[x].phone_number
		d["email"] = find_user[x].email
		ret.append(d.copy())

	return ret

# given a user QuerySet, return that QuerySet in dictionary format
def user_to_json(find_user):
	d = {}
	ret = []
	# querySet can't be serialized so convert
	# it to a dictionary

	for x in range(len(find_user)):
		d["name"] = find_user[x].name
		d["email"] = find_user[x].email
		ret.append(d.copy())

	return ret