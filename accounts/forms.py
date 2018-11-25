from django.contrib.auth import get_user_model # this returns the user model currently active in this project
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
	class Meta():
		fields = ('username','email','password1','password2')
		model = get_user_model() 
		
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['username'].label = 'Display Name' # just changing the label from username to display name on the form when the user tries to sign update
		self.fields['email'].label = 'Email Address'
		
		
			