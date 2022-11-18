from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registrar/', views.registar, name='registrar'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('eliminar/<str:pk>/',views.eliminar_todo, name='eliminar_todo'),
    path('editar/<str:pk>/',views.editar_todo, name='editar_todo'),
]
