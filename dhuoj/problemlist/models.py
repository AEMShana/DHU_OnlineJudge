from django.db import models
from team.models import Team

class ProblemList(models.Model):
    listName = models.CharField(max_length=30)
    members = models.JSONField(null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.listName