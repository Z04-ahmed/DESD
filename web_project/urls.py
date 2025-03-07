# web_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),   # Django admin URL
    path('student/', include('student_management.urls')),  # Include URLs from the student app
    
    # Add other app routes here
]
