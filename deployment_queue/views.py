from django.shortcuts import render
from deployment_detail.models import DeploymentDetail
from django.shortcuts import redirect
from authenticate.models import UserProfile


def deployment_queue(request):
    if not request.user.is_authenticated:
        user_message = "Please login to access the Training Management System"
        return render(request, 'login.html', {'user_message': user_message})
    deployment_records = DeploymentDetail.objects.filter(deployment_status='Open').order_by('project_code', 'course_order')
    return render(request, 'deployment_queue.html', {'deployment_records': deployment_records, 'profile_info':UserProfile.objects.get(username=request.user.username)})


def update_deployment_queue(request):
    if not request.user.is_authenticated:
        user_message = "Please login to access the Training Management System"
        return render(request, 'login.html', {'user_message': user_message})
    if request.POST.get('cancel_deployment_queue'):
        return redirect('/queue')

    if request.POST.get('save_deployment_queue'):
        deployment_records = save_deployment_queue(request)
        return render(request, 'deployment_queue.html', {'deployment_records': deployment_records, 'profile_info':UserProfile.objects.get(username=request.user.username)})

    if request.POST.get('save_exit_deployment_queue'):
        deployment_records = save_deployment_queue(request)
        return redirect('/queue')


def save_deployment_queue(request):
    if not request.user.is_authenticated:
        user_message = "Please login to access the Training Management System"
        return render(request, 'login.html', {'user_message': user_message})
    my_checkboxes = request.POST.getlist('Completed')
    for item in my_checkboxes:
        temp_deployment_record = DeploymentDetail.objects.get(deliverable_id=item)
        temp_deployment_record.deployment_status = 'Complete'
        temp_deployment_record.save()
    deployment_records = DeploymentDetail.objects.filter(deployment_status='Open').order_by('project_code','course_order')
    return deployment_records