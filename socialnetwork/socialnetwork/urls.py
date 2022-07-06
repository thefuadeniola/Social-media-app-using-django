"""socialnetwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from social.views import profile, AddFollower, RemoveFollower, FollowerList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('landing.urls')),
    path('posts/', include('social.urls')),
    path('search/', include('search.urls')),
    path('<str:pk>/', profile, name='profile'),
    path('<str:pk>/follow', AddFollower.as_view(),),
    path('<str:pk>/unfollow', RemoveFollower.as_view(),),
    path('<str:pk>/followers', FollowerList.as_view(), name='follower-list' ),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
handler404 = 'social.views.handle_not_found'