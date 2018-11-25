from django.db import models
from django.urls import reverse # when the user creates a post what do you send them back to
from django.conf import settings

import misaka

from groups.models import Group # so we can connect a post to an actual group 

from django.contrib.auth import get_user_model
User = get_user_model() # connect the current post to current user that is logged in

class Post(models.Model):
	user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE) # in templates it will be group.posts
	created_at = models.DateTimeField(auto_now=True) # automatically generated
	message = models.TextField()
	message_html = models.TextField(editable=False) # user cannot edit this as we are grabbing it from the message above and doing stuff to it
	group = models.ForeignKey(Group, related_name='posts', null=True, blank=True, on_delete=models.CASCADE) # connecting a post to a group and relating it by the name posts

	def __str__(self):
		return self.message
		
	def save(self, *args, **kwargs):
		self.message_html = misaka.html(self.message)
		super().save(*args, **kwargs)
		
	def get_absolute_url(self):
		return reverse('posts:single', kwargs={'username':self.user.username, 'pk':self.pk})
		
	class Meta:
		ordering = ['-created_at'] # puts most recently created post at top of page
		unique_together = ['user','message'] # each message is uniquely linked to a user
	



# Create your models here.
