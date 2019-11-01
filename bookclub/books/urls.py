from django.urls import path

from . import views

app_name = 'books'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/edit', views.edit, name='edit'),
    path('<int:pk>/update', views.update_book, name='update'),
    path('add_book', views.add_book, name='add_book'),
    path('add_bulk', views.add_bulk, name='add_bulk'),

]
