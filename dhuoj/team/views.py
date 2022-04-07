from problemlist.models import ProblemList
from .models import Team
from django.shortcuts import render, redirect
from userprofile.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import TeamForm


def team_detail(request, id):
    team = Team.objects.get(id=id)
    temp = ProblemList.objects.filter(team=team)
    members = team.members["members"]
    problemlists=[]
    for i in range(len(temp)):
        problemlist = temp[i]
        val = {
            "listID": int(problemlist.id),
            "listName": problemlist.listName,
            "problemNumber": len(problemlist.members["problems"])}
        problemlists.append(val)
    for i in range(len(members)):
        user = User.objects.filter(username=members[i])[0]
        members[i] = {
            "name": members[i],
            "id": user.id,
            "profile": Profile.objects.filter(user=user)[0]
        }
    context = {
        "teamID":id,
        "name": team.name,
        "members": members,
        "problemlists": problemlists
    }
    return render(request, 'team/detail.html', context)


def team_list(request):
    temp = Team.objects.all()
    teams = []
    for team in temp:
        val = {
            "id": team.id,
            "name": team.name,
            "user_number": len(team.members['members']),
            "problemlist_number": 0#len(team.problemlists['problemlists'])
        }
        teams.append(val)
    context = {"teams": teams}

    return render(request, 'team/team_list.html', context)

@login_required(login_url='/userprofile/login/')
def team_create(request):
    if request.method == 'POST':
        if request.user.username != 'admin':
            return HttpResponse("抱歉，你无权创建团队。")
        team_form = TeamForm(data=request.POST)
        if team_form.is_valid():
            new_team = team_form.save(commit=False)
            new_team.save()
            return redirect("team:team_list")
        else:
            return HttpResponse("input invalid !")
    else:
        team_form = TeamForm()
        context = {'team_form': team_form}
        return render(request, 'team/create.html', context)
