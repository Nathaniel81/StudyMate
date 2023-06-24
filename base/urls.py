from django.urls import path
from . import views

"""
This module contains all URL patterns for the chat application.

The urlpatterns list maps URL patterns to their corresponding view functions.

URL Patterns:
- /login/: The login page.
- /logout/: The logout page.
- /register/: The registration page.
- /: The homepage.
- /room/<str:pk>/: The page for a specific chat room.
- /profile/<str:pk>/: The user profile page.
- /create-room/: The page for creating a new chat room.
- /update-room/<str:pk>/: The page for updating an existing chat room.
- /delete-room/<str:pk>/: The page for deleting an existing chat room.
- /delete-message/<str:pk>/: The page for deleting a specific message.
- /update-user/: The page for updating the current user's profile.
- /topics/: The page listing all available chat topics.
- /activity/: The page listing all recent chat activity.

"""

# URL patterns
urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    # Room detail page
    path('room/<str:pk>', views.room, name='room'),
    # Create room page
    path('create-room/', views.createRoom, name='create-room'),
    # Update room page
    path('update-room/<str:pk>', views.UpdateRoom, name='update-room'),
    # Delete room page
    path('delete-room/<str:pk>', views.DeleteRoom, name='delete-room'),
    # Delete message action
    path('delete-message/<str:pk>', views.deleteMessage, name='delete-message'),
    # User login page
    path('login/', views.loginPage, name='login'),
    # User logout action
    path('logout/', views.logoutUser, name='logout'),
    # Update user profile page
    path('update-user/', views.updateUser, name='update-user'),
    # User registration page
    path('register/', views.registerPage, name='register'),
    # User profile page
    path('profile/<str:pk>', views.userProfile, name='user-profile'),
    # Topics page
    path('topics/', views.topicsPage, name='topics'),
    # Activity page
    path('activity/', views.activityPage, name='activity')
]
