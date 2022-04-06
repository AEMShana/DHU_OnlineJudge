from unittest import result
from django.db import models
from django.contrib.auth.models import User


class JudgeStatus(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    problemID = models.TextField(max_length=20, null=True)
    verdict = models.TextField(max_length=50, null=True)
    detail = models.JSONField(null=True)
