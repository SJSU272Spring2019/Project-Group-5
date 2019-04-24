from django.shortcuts import render
from deployment_detail.models import DeploymentDetail


def deployment_queue(request):
    deployment_records = DeploymentDetail.objects.filter(deployment_status='Open').order_by('project_code', 'course_order')
    return render(request, 'deployment_queue.html', {'deployment_records': deployment_records})



def update_deployment_queue(request):
    my_checkboxes = request.POST.getlist('Completed')
    for item in my_checkboxes:
        temp_deployment_record = DeploymentDetail.objects.get(deliverable_id=item)
        temp_deployment_record.deployment_status = 'Complete'
        temp_deployment_record.save()
    deployment_records = DeploymentDetail.objects.filter(deployment_status='Open').order_by('project_code', 'course_order')
    return render(request, 'deployment_queue.html', {'deployment_records': deployment_records})
