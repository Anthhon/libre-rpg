from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from apps.core.forms import LoginForm
from apps.core.models import Profile
from django.contrib.sessions.models import Session
from django.utils import timezone


# FIXME: Check a solid way to count ONLY authenticated users
def logged_users_count():
    # Get all (non expired) active sessions
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())

    # Return count of active_sessions
    return len(active_sessions) - 1


def context_get(request, page_name):
    user = request.user
    user_profile = Profile.objects.filter(user=user).first()
    users_count = logged_users_count()

    context = {
            'profile': user_profile,
            'users_count': users_count,
            'page_name': page_name,
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
def dashboard_render(request):
    context = context_get(request, 'dashboard')
    return render(request, "dashboard.html", context)


@login_required(login_url="login")
def logout_user(request):
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
            return redirect('chat')
        else:
            # Authentication failed
            if username and password:
                # Check if user exists
                user_exists = User.objects.filter(username=username).exists()

                if user_exists:
                    # User exists but password is wrong
                    # TODO: Implement proper error message
                    print("ERROR: User exists but password is wrong")
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
