from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
	return render(request, 'index.html')


def register(request):
	"""registering and grabbing user id registration flow
	based off the model"""
	errors = User.objects.validator(request.POST)
	if len(errors) > 0:
		print("after first second")
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	else:
		# Create User
		hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
		user = User.objects.create(
			first_name=request.POST['first_name'],
			last_name=request.POST['last_name'],
			email=request.POST['email'], password=hash_pw
			# password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt().decode())
		)
		request.session['user_id'] = user.id
		request.session['first_name'] = user.first_name
		return redirect('/wall/create')


def login(request):
	"""email and pw, avoid bcrypt salt error
	check for email, then compare pw form field with db stored pw"""
	# see if the username provided exists in the database
	user = User.objects.filter(
		email=request.POST['email'])  # why are we using filter here instead of get
	if len(user) > 0:		# if this isn't triggered, inner else statement executes
		logged_user = user[0]
		# print(logged_user.password)
		# use bcrypt's check_password_hash method, passing the hash from db and the pw from the form
		if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
			# if we get True after checking the password, we have to put the user id in session
			request.session['user_id'] = logged_user.id
			return redirect('/dash')
			# return redirect('/wall/create')
		else:
			messages.error(request, 'Email or password did not match')
		# if the passwords don't match, redirect back to a safe route
		return redirect("/")


def dash(request):
	context = {
		"logged_user": User.objects.get(id=request.session['user_id'])
	}
	return render(request, 'create.html', context)


def create(request):
	"""users can create post"""
	context = {
		# 'first_name': request.session['first_name'],
		'messages': Message.objects.all(),
		'comments': Message.objects.all(),
	}
	return render(request, 'create.html', context)


def message(request):
	"""posted messages"""
	print('creating post')
	if request.method == 'POST':
		new_message = Message.objects.create(
			message_text=request.POST['message'],		# this matches name="message" in create.html
			user=User.objects.get(id=request.session['user_id'])
		)
		new_message.save()
	return redirect('/wall/create')


def comment(request):
	"""post comments"""
	if request.method == 'POST':
		new_comment = Comment.objects.create(
			comment_text=request.POST['comment'],
			user=User.objects.get(id=request.session['user_id']),			# changed this from user to user_id
			message=Message.objects.get(id=request.POST['message_id'])		# changed this from message to message_id
			# message=Message.objects.get(id=message_id)
		)
		new_comment.save()

	return redirect('/wall/create')


def destroy(request):
	"""clear a session"""
	request.session.clear()
	return redirect('/')


def logout(request):
	"""logout session, back to home page"""
	request.session.flush()
	print(request.session)
	return redirect('/')

