from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),  # This will match 'student/'
    path('signup/', views.signup, name='signup'),  # This will match 'student/signup/'
    path('login/', views.user_login, name='login'),  # Changed name here
    path('logout/', views.user_logout, name='user_logout'),  # Renamed logout view
    path('dashboard/', views.dashboard, name='dashboard'),  # Directly linking to dashboard view
]
 