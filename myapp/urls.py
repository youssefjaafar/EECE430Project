from django.urls import path
from.import views

urlpatterns = [
    path('homevideo', views.home, name='homevideo')
]