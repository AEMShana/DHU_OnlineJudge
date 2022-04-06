import imp
from django.shortcuts import render, redirect
from django.http import Http404
from .models import Problem
from judgestatus.models import JudgeStatus
import markdown


def render_markdown(text):
    return markdown.markdown(text,
                             extensions=[
                                 'markdown.extensions.extra',
                                 'markdown.extensions.codehilite',
                                 'pymdownx.arithmatex',
                             ]
                             )


def problemlist(request):
    problems = Problem.objects.all()
    problem_info = []

    if request.user.username:
        for problem in problems:
            verdict = ''
            status = JudgeStatus.objects.filter(
                author=request.user, problemID=problem.problemID)
            for statu in status:
                if statu.verdict == 'Accepted':
                    verdict = 'AC'
                    break

            problem_info.append({
                'problemID': problem.problemID,
                'title': problem.title,
                'difficulty': problem.problem_difficulty,
                'verdict': verdict
            })
    else:
        for problem in problems:
            verdict = ''

            problem_info.append({
                'problemID': problem.problemID,
                'title': problem.title,
                'difficulty': problem.problem_difficulty,
                'verdict': verdict
            })
    context = {'problem_info': problem_info}
    return render(request, 'problemset/problemlist.html', context)


def problem(request, problem_id):
    try:
        problem_detail = Problem.objects.get(problemID=problem_id)
    except Problem.DoesNotExist:
        raise Http404('题目不存在！')

    problem_detail.example_list = render_markdown(problem_detail.example_list)

    problem_detail.problem_description = render_markdown(
        problem_detail.problem_description)

    problem_detail.problem_input = render_markdown(
        problem_detail.problem_input)

    problem_detail.problem_output = render_markdown(
        problem_detail.problem_output)

    problem_detail.problem_source = render_markdown(
        problem_detail.problem_source)

    if problem_detail.problem_background == 'NULL':
        problem_detail.problem_background = ''
    else:
        problem_detail.problem_background = render_markdown(
            problem_detail.problem_background)

    context = {
        'problem_detail': problem_detail,
    }
    return render(request, 'problemset/problem.html', context)
