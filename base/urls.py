from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),

    path('room/<str:pk>', views.room, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>', views.UpdateRoom, name='update-room'),
    path('delete-room/<str:pk>', views.DeleteRoom, name='delete-room'),

    path('delete-message/<str:pk>', views.deleteMessage, name='delete-message'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('update-user/', views.updateUser, name='update-user'),
    path('register/', views.registerPage, name='register'),

    path('profile/<str:pk>', views.userProfile, name='user-profile'),

    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activityPage, name='activity')
]