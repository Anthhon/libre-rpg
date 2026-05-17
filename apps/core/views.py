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


def update_user_online_status(user: User, is_online: bool) -> None:
    """
    Update the online status of a user's profile.

    Uses a single UPDATE query to avoid fetching the profile first.
    If the profile does not exist, the error is logged but not raised,
    assuming the post‑save signal creates it automatically.
    """
    updated_profile = Profile.objects.filter(user=user).update(is_online=is_online)
    if not updated_profile:
        logger.error("Profile not found for user %s when updating online status", user.username)


def get_page_name(request):
    """
    Returns the current URL name to the template context,
    useful for sidebar highlighting or body classes.
    """
    if not request.resolver_match:
        return None
    return request.resolver_match.url_name


def get_user_profile(user):
    """Returns user_profile objects for authenticated users"""
    user_profile = Profile.get_from(user)
    return user_profile


def get_campaign(campaign_id: int = 0):
    """Returns campaign object with prefetched (masters, players) data"""
    if campaign_id == 0:
        return None

    campaign = Campaign.objects.prefetch_related('masters', 'players').get(id=campaign_id)
    return campaign


@login_required(login_url="login")
def configurations_render(request, id):
    profile = get_user_profile(request.user)
    campaign = get_campaign(campaign_id=id)

    # TODO: Get local and global ip and set display them

    return render(request, "configurations.html", {
        'profile': profile,
        'campaign': campaign,
        'page_name': get_page_name(request),
        })


@login_required(login_url="login")
def chat_render(request, id):
    profile = get_user_profile(request.user)
    campaign = get_campaign(campaign_id=id)

    return render(request, "chat.html", {
        'profile': profile,
        'campaign': campaign,
        'page_name': get_page_name(request),
        })


@login_required(login_url="login")
def character_sheet_render(request, id):
    profile = get_user_profile(request.user)
    campaign = get_campaign(campaign_id=id)

    return render(request, "character_sheet.html", {
        'profile': profile,
        'campaign': campaign,
        'page_name': get_page_name(request),
        })


@login_required(login_url="login")
def players_list_render(request, id):
    profile = get_user_profile(request.user)
    campaign = get_campaign(campaign_id=id)

    # Get all the current participants of the current campaign 
    # with a 'is_master' flag to identify masters
    masters_qs = campaign.masters.all()
    players_qs = campaign.players.all()
    players_list = []
    for master in masters_qs:
        players_list.append((master, True))
    for player in players_qs:
        players_list.append((player, False))

    return render(request, "players_list.html", {
        'profile': profile,
        'campaign': campaign,
        'players_list': players_list,
        'page_name': get_page_name(request),
        })


@login_required(login_url="login")
def dashboard_render(request, id):
    profile = get_user_profile(request.user)
    campaign = get_campaign(campaign_id=id)

    return render(request, "dashboard.html", {
        'profile': profile,
        'campaign': campaign,
        'page_name': get_page_name(request),
        })


def logout_user(request):
    """Log out the current user and mark them as offline."""
    if request.user.is_authenticated:
        update_user_online_status(request.user, False)
        logout(request)
    return redirect('login')


def login_render(request):
    """
    Handle login and automatic account creation.

    - If the user is already authenticated, redirect to the campaign list.
    - On POST: validate credentials; if they do not exist, create a new user.
    - On GET: display the login form.
    """
    if request.user.is_authenticated:
        return redirect('campaign_list')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        # Check if any field is empty
        if not username or not password:
            form.add_error(None, "Both username and password are required.")
            return render(request, "welcome.html", {'form': form})

        # Attempt authentication (user exists and password is correct)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            update_user_online_status(user, True)
            return redirect('campaign_list')

        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            # User exists but password is incorrect
            # Authentication failed
            if username and password:
                # Check if user exists
                user_exists = User.objects.filter(username=username).exists()
                if user_exists:
                    # User exists but password is wrong
                    form.add_error('password', "Password must be at least 6 characters long.")
                    return render(request, "welcome.html", {'form': form})
                else:
                    try:
                        # Ensure minimum password length for new accounts
                        if len(password) < 6:
                            form.add_error('password', "Password must be at least 6 characters long.")
                            return render(request, "welcome.html", {'form': form})

                        # Create new user
                        # Warning: this also creates a new profile, since
                        # the user model sends a signal to a 'post_save' type
                        # receiver which get a new model in put the user on it
                        user = User.objects.create_user(username=username, password=password)
                        login(request, user)
                        update_user_online_status(user, True)
                        return redirect('campaign_list')
                    except Exception as e:
                        logger.exception("Failed to create user %s", username)
                        form.add_error(None, "Unable to create new account. Please try again.", username)
                        return render(request, "welcome.html", {'form': form})
    else:
        form = LoginForm()

    return render(request, "welcome.html", {'form': form})
