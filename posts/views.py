from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.http import Http404
from posts.models import Post
from braces.views import SelectRelatedMixin
from . import forms
from django.contrib.auth import get_user_model
User = get_user_model() # When someone is logged in to a session going to be able to use that current user
# to call things of that.

from django.contrib import messages



# List of groups a user is in
class PostList(SelectRelatedMixin, generic.ListView):
	model = Post
	select_related = ('user','group')
# Above is a tuple of related things to the model how we relate models to each other	

class UserPosts(generic.ListView):
	model = Post
	template_name = 'posts/user_post_list.html'
	
	def get_queryset(self):
		try:
			self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )	
		except User.DoesNotExist:
			raise Http404
		else:
			return self.post_user.posts.all()
			
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['post_user'] = self.post_user
		return context
		
class PostDetail(SelectRelatedMixin,generic.DetailView):
	model = Post
	select_related = ('user','group')

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(user__username__iexact=self.kwargs.get('username'))
		
# Get the query set for actual post then make sure user is equal to username and is exactly correct		


class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
	fields = ('message','group')
	model = Post
	
	def form_valid(self,form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user # connect post to a user
		self.object.save()
		return super().form_valid(form) # super connects to class you inherit from so maybe generic.createview

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
	model = Post
	select_related = ('user','group')
	success_url = reverse_lazy('posts:all')
	
	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(user_id=self.request.user.id)
		
	def delete(self,*args,**kwargs):
		messages.success(self.request,'Post Deleted')
		return super().delete(*args,**kwargs)
		