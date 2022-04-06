from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=30)
    members = models.JSONField(null=True)
    # problemlists = models.JSONField(null=True)

    def __str__(self):
        return self.name

# Create your models here.
