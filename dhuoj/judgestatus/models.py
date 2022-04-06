from unittest import result
from django.db import models
from django.contrib.auth.models import User


class JudgeStatus(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    detail = models.JSONField(null=True)
