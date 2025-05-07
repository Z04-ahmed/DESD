from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='home'),  # This will match 'student/'
    path('signup/', views.signup, name='signup'),  # This will match 'student/signup/'
    path('login/', views.user_login, name='user_login'),  # Changed name here
    path('logout/', views.user_logout, name='user_logout'),  # Renamed logout view
    path('dashboard/', views.dashboard, name='dashboard'),  # Directly linking to dashboard view
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('create-community-api/', views.create_community_api, name='create_community_api'),
    path('communities/<int:community_id>/delete/', views.delete_community, name='delete_community'),
    path('communities/<int:community_id>/details/', views.community_details, name='community_details')


]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
 