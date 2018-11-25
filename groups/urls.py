from django.urls import path
from groups import views

app_name = 'groups'

urlpatterns = [
	path('',views.ListGroups.as_view(), name='group_list'),
	path("posts/in/<slug>/",views.GroupDetail.as_view(), name='single'), # this will be /posts/in/group name in slug form
	path('create/',views.CreateGroup.as_view(), name='create'),
	path('join/<slug>',views.JoinGroup.as_view(),name='join'),
	path('leave/<slug>',views.LeaveGroup.as_view(),name='leave'),

]
