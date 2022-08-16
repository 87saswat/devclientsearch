

from django.shortcuts import render, redirect
from .models import Profile, Message
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, ProfileForm, SkillForm

from .utils import searchProfiles, paginateProfiles

# Create your views here.


def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 6)
    context = {'profiles': profiles, 'search_query': search_query,
               'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {'profile': profile, 'topSkills': topSkills,
               'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    # request.user gives us the logged in user's details and .profile give the details of profile because of onetoone relationship
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.projects_set.all()
    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):

    profile = request.user.profile  # loggedin user's profile(one to one)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


def registerUser(request):
    page = 'register'

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(
                request, 'Profile craeted successfully!! Redirecting to Profile')
            login(request, user)

            return redirect('profiles')
        else:
            messages.error(request, "An error occured during registration")
    form = CustomUserCreationForm()
    context = {'page': page, "form": form}
    return render(request, 'users/login-register.html', context)


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Username doesnot exists!!")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request, "users/login-register.html")


def logoutUser(request):
    logout(request)
    messages.success(request, "User sucessfully loggedout")
    return redirect('projects')


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill created successfully!!")
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():

            form.save()
            messages.success(request, "Skill updated successfully!!")
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):

    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, "Skill deleted successfully!!")
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete-objects.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


def viewMessage(request):
    context = {}
    return render(request, 'users/message.html', context)
