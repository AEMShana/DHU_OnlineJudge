from django.shortcuts import render

from .models import Team
from problemlist.models import ProblemList

def team_detail(request, id):
    team = Team.objects.get(id=id)
    context = {"name": team.name,
                "members": team.members["members"],
                "questionlist": team.bank["bank"]
              }
    return render(request, 'team/detail.html', context)

# Create your views here.
