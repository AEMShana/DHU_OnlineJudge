from django.shortcuts import render
from .models import ProblemList

def problemlist_detail(request, id):
    prolist = ProblemList.objects.get(id=id)
    context = {"name": prolist.listName, "problems": prolist.members["problems"]}
    return render(request, 'problemlist/detail.html', context)
