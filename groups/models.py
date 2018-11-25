from django.db import models
from django.utils.text import slugify # if you have space in string it will fill with dashes etc so your browser can read it
import misaka # for link embedding
from django.contrib.auth import get_user_model # allows us to get information from the current user using the site
User = get_user_model()
from django.urls import reverse
from django import template
register = template.Library()

class Group(models.Model):
	name = models.CharField(max_length=255, unique=True)
	slug = models.SlugField(allow_unicode=True, unique=True)
	description = models.TextField(blank=True, default='')
	description_html = models.TextField(editable=False, default='', blank=True)
	members = models.ManyToManyField(User,through='GroupMember')
# gets the users from the users that are in the group member class below.	

	def __str__(self):
		return self.name

	def save(self,*args,**kwargs):
		self.slug = slugify(self.name) # when person types in group name with spaces this slugify will
	# change the name so it can be used in URL by browser	
		self.description_html = misaka.html(self.description)
		super().save(*args,**kwargs)
		
	def get_absolute_url(self):
		return reverse('groups:single',kwargs={'slug':self.slug})
	
	class Meta:
		ordering = ['name']	
	
class GroupMember(models.Model):
	group = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
	user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE) # I think this is linked to the instance of getusermodel we created above

	def __str__(self):
		return self.user.username # created when user signs up

	class Meta:
		unique_together = ('group','user')