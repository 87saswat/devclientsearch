from unicodedata import name
from .models import Projects, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchProjects(request):
    search_query = ''
    if request.GET.get('search_query'):

        search_query = request.GET.get('search_query')
    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Projects.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )  # owner of (Project)  table go to the parent table(Profile) attribute by owner.name( of Profile.name attribute)

    return projects, search_query


def paginateProjects(request, projects, results):
    # implementing paginator------------------------------------------------------>
    # custom_range, projects = paginateProjects(request, projects, 6)
    # page = 1  # page number e.g. page-1 or page-2 etc
    page = request.GET.get('page')
    # results = 6  # 3 results per page
    paginator = Paginator(projects, results)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        # it tells us how many total pages we have (the last page value)
        page = paginator.num_pages
    projects = paginator.page(page)

 # functionality to not show all the page buttons(e.g. if we have 1000 pages button) we can only see a few e.g. 10 buttons ata  time
    leftIndex = (int(page) - 4)
    rightIndex = (int(page) + 5)

    if leftIndex < 1:
        leftIndex = 1
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    # <-------------------------------------------------------- Paginator ends

    return custom_range, projects
