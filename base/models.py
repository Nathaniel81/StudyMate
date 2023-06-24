from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser

# Custom user model extending Django's AbstractUser

"""models module"""
class User(AbstractUser):
    """
    Custom user model with additional fields.
    """
    # Additional fields for the user
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    
    avatar = models.ImageField(null=True, default='avatar.svg')
    # Configuring the email field as the username for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

#Model representing a topic for discussions
class Topic(models.Model):
    """
    Model representing a discussion topic.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Model representing a chat room
class Room(models.Model):
    """
    Model representing a chat room.
    """
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    participants = models.ManyToManyField(User, related_name = 'participants', blank=True)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
    	ordering = ['-updated', '-created']

# Model representing a message within a room
class Message(models.Model):
    """
    Model representing a chat message.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]
    class Meta:
    	ordering = ['-updated', '-created']
