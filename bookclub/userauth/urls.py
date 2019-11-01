from django.urls import path

from . import views

app_name = 'userauth'
urlpatterns = [
    path('login/', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_user, name='logout_user'),
]
