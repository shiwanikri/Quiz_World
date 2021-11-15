from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('home', views.home),
    path('contact', views.contact),
    path('about', views.about),
    path('signup', views.signup, name='signup'),
    path('login', views.handlelogin, name='handlelogin'),
    path('logout', views.handlelogout, name='handlelogout'),
    path('user/<int:uid>', views.user),
    path('layout/<int:uid>', views.layout),
    path('layout_tita/<int:uid>', views.layout_tita),
    path('Register/<int:uid>', views.Register),
    path('Test/<int:uid>', views.Test),
    path('Test/GiveTest/<int:uid>', views.GiveTest),
    path('result/<int:uid>', views.result),
    path('saveans', views.saveans)
]