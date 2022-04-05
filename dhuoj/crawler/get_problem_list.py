import urllib.request
import bs4
import re
from bs4 import BeautifulSoup


def get_cf_problem_list(page):
    try:
        url = f'https://codeforces.com/problemset/page/{page}'
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'lxml')
    except Exception:
        return []
    try:
        data_dict = {}
        problems = soup.find_all(
            name="table", attrs={"class": "problems"})[0]
        problem_urls = problems.find_all(
            href=re.compile("/problemset/problem/*"))
        problem_list = []
    except Exception:
        return []

    for a in problem_urls:
        s = a['href'].split('/')
        d = (s[-2], s[-1])
        problem_list.append(d)
    return problem_list
