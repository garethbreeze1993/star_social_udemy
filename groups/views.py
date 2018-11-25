from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views import generic
from groups.models import Group,GroupMember
from django.shortcuts import get_object_or_404
from django.contrib import messages

class CreateGroup(LoginRequiredMixin,generic.CreateView):
	fields = ('name','description') # from our models.py file group
	model = Group
	
class GroupDetail(generic.DetailView):
	model = Group
	
class ListGroups(generic.ListView):
	model = Group

class JoinGroup(LoginRequiredMixin, generic.RedirectView):
	def get_redirect_url(self,*args,**kwargs):
		return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})
		
	def get(self,request,*args,**kwargs):
		group = get_object_or_404(Group,slug=self.kwargs.get('slug')) # try and get the group into variable or a 404 page

		# above try to get group member with user = to current member and group is equal to group

		try:
			GroupMember.objects.create(user=self.request.user,group=group)

		except IntegrityError:
			messages.warning(self.request,'Warning already a member')
		else:
			messages.success(self.request,'You are now a member!')
		return super().get(request,*args,**kwargs)	


class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
# The function below just redirects us to the group we have just left after leaving the group
	def get_redirect_url(self,*args,**kwargs):
		return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})
	
	def get(self,request,*args,**kwargs):
	
		try:
			membership = GroupMember.objects.filter(
				user=self.request.user,
				group__slug=self.kwargs.get('slug')
				).get()
		except GroupMember.DoesNotExist:
			messages.warning(self.request,'Sorry you are not in this group!')
		else:
			membership.delete()
			messages.success(self.request,'You have left the group!')
		return super().get(request,*args,**kwargs)	
			
	

