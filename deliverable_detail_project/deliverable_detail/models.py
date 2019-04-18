from django.db import models

class Deliverable(models.Model):

    course_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    project_lead = models.CharField(max_length=50)
    project_code = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    course_duration = models.CharField(max_length=50)
    course_description = models.CharField(max_length=200)
    notes = models.CharField(max_length=300)
    content_complete_date = models.DateTimeField(null=True)
    record_date = models.DateTimeField(null=True)
    processing_complete_date = models.DateTimeField(null=True)
    post_processing_complete_date = models.DateTimeField(null=True)
    target_deploy_date = models.DateTimeField(null=True)


    def __str__(self):
        return self.course_name
