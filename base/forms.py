from django.forms import ModelForm
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User


"""forms module"""
class MyUserCreationForm(UserCreationForm):
    """
    A form for creating a new user, extending Django's built-in UserCreationForm
    and adding the 'name' field.
    """
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    """
    A form for creating or updating a Room instance.
    """
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    """
    A form for creating or updating a User instance.
    """
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
