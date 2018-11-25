from django.urls import path
from posts import views

app_name = 'posts'

urlpatterns = [
	path('',views.PostList.as_view(), name='all'),
	path('create/',views.CreatePost.as_view(), name='create'), 
    path("by/<username>/",views.UserPosts.as_view(),name="for_user"), # all the posts listed by that user in listview class
    path("by/<username>/<int:pk>/",views.PostDetail.as_view(),name="single"), # from list click on a post you get to that indvidual post by that user get there via pk
    path("delete/<int:pk>/",views.DeletePost.as_view(),name="delete"), # delete a post is linked via primary key.
]
