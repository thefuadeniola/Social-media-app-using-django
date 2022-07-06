from django.urls import path
from social.views import search_view
app_name = 'search'
urlpatterns =[
    path('', search_view, name='search'),
]