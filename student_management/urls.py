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
    path('notifications/', views.notifications, name='notifications'),
    path('create-community-api/', views.create_community_api, name='create_community_api'),
    path('communities/<int:community_id>/delete/', views.delete_community, name='delete_community'),
    path('communities/<int:community_id>/details/', views.community_details, name='community_details'),
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.create_event, name='create_event'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('event/<int:event_id>/details/', views.get_event_details, name='get_event_details'),
    path('event/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('events/join/<int:event_id>/', views.join_event, name='join_event'),
    path('events/leave/<int:event_id>/', views.leave_event, name='leave_event'),
    


]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
 