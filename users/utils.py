from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchProfiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains='search_query')
    # search if a profile contains that perticular skills as per the above query. Does the profile has a skill that listed in the query ?
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills))
    return profiles, search_query


def paginateProfiles(request, profiles, results):
    # implementing paginator------------------------------------------------------>
    # custom_range, projects = paginateProjects(request, projects, 6)
    # page = 1  # page number e.g. page-1 or page-2 etc
    page = request.GET.get('page')
    # results = 6  # 3 results per page
    paginator = Paginator(profiles, results)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        # it tells us how many total pages we have (the last page value)
        page = paginator.num_pages
    profiles = paginator.page(page)

 # functionality to not show all the page buttons(e.g. if we have 1000 pages button) we can only see a few e.g. 10 buttons ata  time
    leftIndex = (int(page) - 4)
    rightIndex = (int(page) + 5)

    if leftIndex < 1:
        leftIndex = 1
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    # <-------------------------------------------------------- Paginator ends

    return custom_range, profiles
