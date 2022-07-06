from django.urls import path
from .views import (PostistView, PostDetailView, delete_post, 
                    delete_comment, AddFollower, RemoveFollower,
                    Addlike, Removelike, search_view)

app_name = 'posts'
urlpatterns = [
    path('', PostistView.as_view(), name='post-list'),
    path('<str:pk>/',PostDetailView.as_view(), name='post-detail'),
    path('<str:pk>/delete', delete_post, name='delete-post'),
    path('comment/delete/<int:id>/', delete_comment, name='comment-delete'),
    path('<str:pk>/like/', Addlike.as_view(), name='like'),
    path('<str:pk>/dislike/', Removelike.as_view(), name='dislike'),
    path('search/', search_view, name='search')
]