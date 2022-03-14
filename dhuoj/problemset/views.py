from django.shortcuts import render, redirect
from .models import Problem, ProblemExample
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
    problems = Problem.objects.all()[:50]
    problem_info = []
    for problem in problems:
        problem_info.append({'problemID': problem.problemID, 'title': problem.title,
                            'difficulty': problem.problem_difficulty})

    context = {'problem_info': problem_info}
    return render(request, 'problemset/problemlist.html', context)


def problem(request, problem_id):
    problem_detail = Problem.objects.get(problemID=problem_id)
    example_list = ProblemExample.objects.filter(problem=problem_detail)

    for example in example_list:
        example.input_example = render_markdown(
            "```\n" + example.input_example + "\n```")
        example.output_example = render_markdown(
            "```\n" + example.output_example + "\n```")

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
        'example_list': example_list,
    }
    return render(request, 'problemset/problem.html', context)
