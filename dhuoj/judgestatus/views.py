from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import Http404
from .models import JudgeStatus
import time


def status_list(request, user_name):
    status = JudgeStatus.objects.filter(author__username=user_name)
    status_list = []
    for statu in status:
        val = {
            "user_name": user_name,
            "status_id": statu.detail['result'][0]['id'],
            "verdict": statu.detail['result'][0]['verdict'],
            "programmingLanguage": statu.detail['result'][0]["programmingLanguage"],
            "timeConsumedMillis": str(statu.detail['result'][0]['timeConsumedMillis']) + ' ms',
            "memoryConsumedBytes": str(statu.detail['result'][0]['memoryConsumedBytes']//1024) + ' KB',
            "problem": statu.detail['result'][0]['problem']['name'],
            "submit_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(statu.detail['result'][0]["creationTimeSeconds"]))
        }
        status_list.append(val)
    context = {"status_list": status_list}
    return render(request, 'status/user_status_list.html', context)
