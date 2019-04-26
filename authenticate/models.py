from django.db import models


class UserProfile(models.Model):
    username = models.CharField(max_length=15)
    role = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    topic_interest = models.CharField(max_length=50)
    notes = models.CharField(max_length=300)

    def __str__(self):
        return self.username
