from django.urls import path
from .views import home, profile


app_name = 'tweets'
urlpatterns = [
    path('', home, name='home'),
    path('user/<str:username>/', profile, name='profile')
]
