from django.urls import path
from .views import home


app_name = 'tweets'
urlpatterns = [
    path('', home, name='home'),
]
