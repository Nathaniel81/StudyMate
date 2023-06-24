from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.db.models import Q
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
"""
This is a Django web application with several views defined in the code. 
The views are responsible for rendering the appropriate HTML templates 
when a user makes a request to the server. 
The application supports user registration and login, as well as the creation, 
updating, and deletion of chat rooms and messages.
"""

def loginPage(request):
    """
    Renders the login page when the user navigates to the URL specified in the urlpattern. 
    If the user is already authenticated, they will be redirected to the home page. 
    If the user submits the login form, the view will attempt to authenticate the user 
    with the provided credentials, and redirect to the home page if successful.
    """
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            # print(user)
        except:
            messages.error(request, 'User does not exit')
    
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
     """Logs out the current user and redirects them to the home page."""
     logout(request)
     return redirect('home')

def registerPage(request):
    """
    Renders the registration page when the user navigates to the URL specified in the urlpattern.
    If the user submits the registration form, the view will attempt to create a new user with the 
    provided information and log them in if successful.
    """

    form = MyUserCreationForm()
    # form = UserForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    # context = {'form': form}
    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    """
    Renders the home page, which displays a list of chat rooms and recent messages. 
    The view filters the chat rooms based on a search query submitted by the user, 
    and limits the number of topics and messages displayed.
    """
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q))
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(room__topic__name__icontains=q)
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    """
    Renders the chat room page, which displays a list of messages and participants in the room. 
    If the user submits a message, the view will create a new message and add the user to the list
    of participants in the room.
    """
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()#.order_by('-created')
    participants = room.participants.all()
    # print(participants)
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room=room,
            body=request.POST.get('message')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    context = {'room': room, 'messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    """
    Renders the user profile page, which displays information about the user 
    and their chat room and message history.
    """
    user = User.objects.get(id=pk)
    user_bio = user.bio
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    context = {'bio': user_bio, 'user': user, 'rooms': rooms, 'topics': topics, 'room_messages': room_message}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    """
    Renders the chat room creation form. If the user submits the form, 
    the view will create a new chat room with the provided information.
    """

    topics = Topic.objects.all()
    form = RoomForm()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description =request.POST.get('description') 
        )
        # print(request.POST)
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def UpdateRoom(request, pk):
    """
    Renders the chat room update form. If the user submits the form, 
    the view will update the chat room with the provided information.
    """

    topics = Topic.objects.all()
    room = Room.objects.get(id=pk)
    form = RoomForm(request.POST, instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #  form.save()
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def DeleteRoom(request, pk):
    """Deletes the specified message"""
    obj = Room.objects.get(id=pk)
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        obj.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': obj})

@login_required(login_url='login')
def deleteMessage(request, pk):
    """
    Deletes the specified message and redirects the user back to the chat room. 
    Only the user who created the message is allowed to delete it.
    """
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'message': message})

@login_required(login_url='login')
def updateUser(request):
    """View function to update the current user's profile."""
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form' : form})

def topicsPage(request):
    """Renders the topics page that displays all the available topics."""
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    """Renders the activity page that displays all the user's activity."""
    # messages = Message.objects.all()
    # room = Room.objects.filter()
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})
