from django.shortcuts import render
from .models import ProblemList
from problemset.models import Problem


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
