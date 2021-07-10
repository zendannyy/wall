from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
	path('', views.index),
	path('login', views.login),
	path('register', views.register),
	path('dash', views.dash),		# tbd if I need this
	path('wall/create', views.create),
	path('message', views.message),
	path('comment', views.comment),
	# path('uncomment/<int:message_id>', views.uncomment),
	path('destroy', views.destroy),
	path('logout', views.logout),


]
