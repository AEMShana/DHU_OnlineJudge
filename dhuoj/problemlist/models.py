from django.db import models

class ProblemList(models.Model):
    listName = models.CharField(max_length=30)
    members = models.JSONField(null=True)

    def __str__(self):
        return self.listName