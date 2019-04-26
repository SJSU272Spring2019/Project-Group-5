from django.db import models

# Create your models here.
class DeploymentDetail(models.Model):
    deliverable_id = models.IntegerField(default = 0)
    category = models.CharField(max_length=50)
    project_code= models.CharField(max_length=50)
    course_order = models.CharField(max_length=200)
    curriculum_name = models.CharField(max_length=200)
    curriculum_description = models.CharField(max_length=200)
    course_name = models.CharField(max_length=100)
    course_description = models.CharField(max_length=500)
    days_to_complete_course = models.IntegerField(default=0)
    course_duration = models.CharField(max_length=20)
    course_key_words = models.CharField(max_length=200)
    course_exam = models.CharField(max_length=10)
    approved_audience = models.CharField(max_length=100)
    deployment_status = models.CharField(max_length=50, default='Open')

    def __str__(self):
        return self.curriculum_name