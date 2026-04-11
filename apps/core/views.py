from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from apps.core.forms import LoginForm
from apps.core.models import Profile
from django.contrib.sessions.models import Session
from django.utils import timezone


def context_get(request, page_name):
    user = request.user
    user_profile = Profile.objects.filter(user=user).first()
    users = Profile.objects.all()
    users_online = Profile.objects.filter(is_online=True).count()

    context = {
            'profile': user_profile,
            'users_count': users_online,
            'page_name': page_name,
            'users_list': users,
            }
    print(f'content: {context}')

    return context


@login_required(login_url="login")
def configurations_render(request):
    context = context_get(request, 'config')
    return render(request, "configurations.html", context)


@login_required(login_url="login")
def chat_render(request):
    context = context_get(request, 'chat')
    return render(request, "chat.html", context)


@login_required(login_url="login")
def players_list_render(request):
    context = context_get(request, 'players_list')
    return render(request, "players_list.html", context)


@login_required(login_url="login")
def dashboard_render(request):
    context = context_get(request, 'dashboard')
    return render(request, "dashboard.html", context)


def update_user_online_status(user):
    try:
        profile = Profile.objects.get(user=user)
        profile.is_online = not profile.is_online  # Toggle 'is_online' status
        profile.save()
    except Profile.DoesNotExist:
        # TODO: Implement proper error handling
        print("[ERROR] Could not find 'profile' related to 'user'")


@login_required(login_url="login")
def logout_user(request):
    update_user_online_status(request.user)
    logout(request)
    return redirect('login')


def login_render(request):
    if request.user.is_authenticated:
        return redirect('chat')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Try to authenticate first
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User exists and password is correct
            login(request, user)
            update_user_online_status(user)
            return redirect('chat')
        else:
            # Authentication failed
            if username and password:
                # Check if user exists
                user_exists = User.objects.filter(username=username).exists()
                if user_exists:
                    # User exists but password is wrong
                    # TODO: Implement proper error message
                    print("[ERROR] User exists but password is wrong")
                else:
                    # Create new user
                    # Warning: this also creates a new profile, since
                    # the user model sends a signal to a 'post_save' type
                    # receiver which get a new model in put the user on it
                    user = User.objects.create_user(
                            username=username,
                            password=password
                            )
                    login(request, user)
                    return redirect('chat')
            else:
                # TODO: Implement proper missing info message
                print("ERROR: Fill all the fields before submiting it!")

            return render(request, "welcome.html", {'form': form})
    else:
        form = LoginForm()

    return render(request, "welcome.html", {'form': form})
