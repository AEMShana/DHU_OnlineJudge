from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ProblemList
from problemset.models import Problem
from django.contrib.auth.decorators import login_required
from .forms import ProblemListForm
from team.models import Team
from team.views import team_detail


def problemlist_detail(request, id):
    prolist = ProblemList.objects.get(id=id)
    problems = []
    for problemID in prolist.members["problems"]:
        problem = {"problemID": problemID, "problemTitle": Problem.objects.filter(
            problemID=problemID)[0].title}
        problems.append(problem)

    context = {"name": prolist.listName,
               "problems": problems}
    return render(request, 'problemlist/detail.html', context)

@login_required(login_url='/userprofile/login/')
def problemlist_create(request, id):
    if request.method == 'POST':
        if request.user.username != "admin":
            return HttpResponse("抱歉，你无权创建题单。")
        problem_list_form = ProblemListForm(data=request.POST)
        
        if problem_list_form.is_valid():
            new_list = problem_list_form.save(commit=False)
            new_list.team = Team.objects.get(id=id)
            new_list.save()            
            return redirect("team:team_list")
        else:
            return HttpResponse("input invalid !")
    else:
        problem_list_form = ProblemListForm()
        context = {'problem_list_form': problem_list_form}
        return render(request, 'problemlist/create.html', context)


