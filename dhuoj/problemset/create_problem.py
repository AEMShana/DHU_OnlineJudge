from cgitb import reset
from .models import Problem, ProblemExample
from crawler.get_problem_detail import get_cf_problem_detail
from crawler.get_problem_list import get_cf_problem_list


def create_cf_problem(problemSet, problemId):
    problem_dict = get_cf_problem_detail(problemSet, problemId)
    problemID = problemSet + problemId
    title = problem_dict['Title']
    problem_background = 'NULL'
    problem_description = problem_dict['Problem Description']
    problem_input = problem_dict['Input']
    problem_output = problem_dict['Output']
    problem_note = 'NULL'
    if 'Note' in problem_dict:
        problem_note = problem_dict['Note']
    time_limit = int(problem_dict['Time Limit'].split(' ')[0]) * 1000
    memory_limit = int(problem_dict['Memory Limit'].split(' ')[0])
    problem_difficulty = 0
    problem_source = problem_dict['Source']
    if len(Problem.objects.filter(problemID=problemID)) == 0:
        prob = Problem(
            problemID=problemID,
            title=title,
            problem_background=problem_background,
            problem_description=problem_description,
            problem_input=problem_input,
            problem_output=problem_output,
            problem_note=problem_note,
            time_limit=time_limit,
            memory_limit=memory_limit,
            problem_difficulty=problem_difficulty,
            problem_source=problem_source
        )
        prob.save()


def create_cf_problems(page):
    cf_problem_list = get_cf_problem_list(page)
    cf_problem_list = set(cf_problem_list)
    for d in cf_problem_list:
        print(d)
        create_cf_problem(problemSet=d[0], problemId=d[1])
