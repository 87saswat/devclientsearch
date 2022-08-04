from django.core import paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Projects, Tag
from .forms import ProjectForm
from .utils import searchProjects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def projects(request):
    projects, search_query = searchProjects(request)

    # implementing paginator------------------------------------------------------>
    # custom_range, projects = paginateProjects(request, projects, 6)
    page = 1  # page number e.g. page-1 or page-2 etc
    results = 3  # 3 results per page
    paginator = Paginator(project, results)
    projects = paginator.page(page)
    # <-------------------------------------------------------- Paginator ends

    context = {'projects': projects,
               'search_query': search_query, }
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Projects.objects.get(id=pk)
    context = {'project': projectObj}
    return render(request, 'projects/single-project.html', context)


@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    context = {'form': form}
    return render(request, "projects/project-form.html", context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('account')

    context = {'form': form, 'project': project}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'delete_template.html', context)
