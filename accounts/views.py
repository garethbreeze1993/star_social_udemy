from django.shortcuts import render
from django.urls import reverse_lazy
from . import forms
from django.views.generic import CreateView
# Once someone successfuly signed up they will be redirected to login page via reverse lazy

class SignUp(CreateView):
	form_class = forms.UserCreateForm
	success_url = reverse_lazy('login') # after completing the sign up page and hitting submit button you will be directed to login page via name='login'
	template_name = 'accounts/signup.html'
	
	
	