from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.utils import timezone
from apps.core.forms import LoginForm
from apps.core.models import Profile
from apps.campaigns.models import Campaign
from django.shortcuts import get_object_or_404


def update_user_online_status(user, status):
    try:
        profile = Profile.objects.get(user=user)
        profile.is_online = status
        profile.save()
    except Profile.DoesNotExist:
        # TODO: Implement proper error handling
        print("[ERROR] Could not find 'profile' related to 'user'")


# TODO: Modulate context_get better since not all pages will want all this info
# Variable 'page_name' is used by html django pre-processor
# which uses this value passed into context, to generate dynamic 
# sidebar buttons visuals when users change views
def context_get(request, page_name, campaign_pk):
    user = request.user
    user_profile = Profile.objects.filter(user=user).first()

    users = Profile.objects.all()
    users_online = Profile.objects.filter(is_online=True).count()

    if campaign_pk != 0:
        campaign = get_object_or_404(Campaign, id=campaign_pk)
    else:
        campaign = None

    context = {
            'profile': user_profile,
            'users_count': users_online,
            'page_name': page_name,
            'users_list': users,
            'campaign': campaign,
            }
    print(f'content: {context}')

    return context


# FIXME: Configuration page not rendering correctly
@login_required(login_url="login")
def configurations_render(request, id):
    context = context_get(request, 'config', id)
    return render(request, "configurations.html", context)


@login_required(login_url="login")
def chat_render(request, id):
    context = context_get(request, 'chat', id)
    return render(request, "chat.html", context)


@login_required(login_url="login")
def character_sheet_render(request, id):
    context = context_get(request, 'char_sheet', id)
    return render(request, "character_sheet.html", context)


@login_required(login_url="login")
def players_list_render(request, id):
    context = context_get(request, 'players_list', id)
    return render(request, "players_list.html", context)


@login_required(login_url="login")
def dashboard_render(request, id):
    context = context_get(request, 'dashboard', id)
    return render(request, "dashboard.html", context)


def logout_user(request):
    if request.user.is_authenticated:
        update_user_online_status(request.user, False)
        logout(request)
    return redirect('login')


def login_render(request):
    if request.user.is_authenticated:
        return redirect('campaign_list')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Try to authenticate first
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User exists and password is correct
            login(request, user)
            update_user_online_status(user, True)
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
