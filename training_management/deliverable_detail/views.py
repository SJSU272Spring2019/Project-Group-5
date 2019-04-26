from django.shortcuts import render
from django.http import HttpResponse
from . models import Deliverable
from datetime import datetime
from deployment_detail.models import DeploymentDetail

# Create your views here.
def index(request):
    return render(request, 'create_deliverable.html')



def deliverable_detail_submit(request):
    if request.POST.get('deploy_button'):
        temp_deployment_record = DeploymentDetail.objects.filter(deliverable_id=int(request.POST['deliverable_id']))
        if not temp_deployment_record:
            # deliverable_record = Deliverable.objects.get(id=int(request.POST['deliverable_id']))
            my_deployment_detail_record = DeploymentDetail()
            my_deployment_detail_record.deliverable_id = request.POST['deliverable_id']
            my_deployment_detail_record.course_name = request.POST['course_name']
            my_deployment_detail_record.course_description = request.POST['course_description']
            my_deployment_detail_record.category = request.POST['category']
            my_deployment_detail_record.project_code = request.POST['project_code']
        else:
            my_deployment_detail_record = temp_deployment_record[0]

        return render(request, 'deployment_detail.html', {'my_deployment_detail_record':my_deployment_detail_record})
    if request.POST.get('cancel_button'):
        deliverable_records = Deliverable.objects.filter(status='2) Develop')
        return render(request, 'queue_page.html', {'deliverable_records': deliverable_records})
    if request.POST.get('save'):
        my_deliverable_detail_record=save_detail(request)
        return render(request, 'create_deliverable.html', {'my_deliverable_detail_record': my_deliverable_detail_record})
    if request.POST.get('save_exit'):
        my_deliverable_detail_record = save_detail(request)
        deliverable_records = Deliverable.objects.filter(status='2) Develop')
        return render(request, 'queue_page.html', {'deliverable_records': deliverable_records})


def save_detail(request):
    if request.POST['content_complete_date'] == '':
        temp_content_complete_date = None
    else:
        temp_content_complete_date = datetime.strptime(request.POST['content_complete_date'], '%m/%d/%Y')

    if request.POST['record_date'] == '':
        temp_record_date = None
    else:
        temp_record_date = datetime.strptime(request.POST['record_date'], '%m/%d/%Y')

    if request.POST['post_processing_complete_date'] == '':
        temp_post_processing_complete_date = None
    else:
        temp_post_processing_complete_date = datetime.strptime(request.POST['post_processing_complete_date'],
                                                               '%m/%d/%Y')

    if request.POST['target_deploy_date'] == '':
        temp_target_deploy_date = None
    else:
        temp_target_deploy_date = datetime.strptime(request.POST['target_deploy_date'], '%m/%d/%Y')

    if request.POST['deliverable_id'] == '':
        my_deliverable_detail_record = Deliverable(course_name=request.POST['course_name'],
                                                   category=request.POST['category'],
                                                   project_lead=request.POST['project_lead'],
                                                   project_code=request.POST['project_code'],
                                                   status=request.POST['status'],
                                                   course_duration=request.POST['course_duration'],
                                                   course_description=request.POST['course_description'],
                                                   notes=request.POST['notes'],
                                                   content_complete_date=temp_content_complete_date,
                                                   record_date=temp_record_date,
                                                   post_processing_complete_date=temp_post_processing_complete_date,
                                                   target_deploy_date=temp_target_deploy_date)
        my_deliverable_detail_record.save()
        my_deliverable_detail_record.deliverable_id = my_deliverable_detail_record.id
        my_deliverable_detail_record.save()

    else:
        my_queryset = Deliverable.objects.filter(id=int(request.POST['deliverable_id']))
        my_deliverable_detail_record = my_queryset[0]
        my_deliverable_detail_record.course_name = request.POST['course_name']
        my_deliverable_detail_record.category = request.POST['category']
        my_deliverable_detail_record.project_lead = request.POST['project_lead']
        my_deliverable_detail_record.project_code = request.POST['project_code']
        my_deliverable_detail_record.status = request.POST['status']
        my_deliverable_detail_record.course_duration = request.POST['course_duration']
        my_deliverable_detail_record.course_description = request.POST['course_description']
        my_deliverable_detail_record.notes = request.POST['notes']
        my_deliverable_detail_record.content_complete_date = temp_content_complete_date
        my_deliverable_detail_record.record_date = temp_record_date
        my_deliverable_detail_record.post_processing_complete_date = temp_post_processing_complete_date
        my_deliverable_detail_record.target_deploy_date = temp_target_deploy_date
        my_deliverable_detail_record.save()

    return my_deliverable_detail_record



def queue_page(request):
    return render(request, 'queue_page.html')


def deliverable_link(request):
    my_deliverable_detail_record = Deliverable.objects.filter(id=int(request.GET['deliverable_id']))
    return render(request, 'create_deliverable.html', {'my_deliverable_detail_record': my_deliverable_detail_record[0]})

