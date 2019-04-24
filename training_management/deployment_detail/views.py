from django.shortcuts import render
from . models import DeploymentDetail
from deliverable_detail.models import Deliverable

def index(request):
    return render(request, 'index.html')


def deployment_detail(request):
    return render(request, 'deployment_detail.html')

def deployment_detail_submit(request):
    if request.POST.get('deployment_cancel') == 'Cancel':
        if request.POST['deliverable_id'] != '':
            my_deliverable_detail_record = Deliverable.objects.get(id=int(request.POST['deliverable_id']))
            return render(request, 'create_deliverable.html', {'my_deliverable_detail_record':my_deliverable_detail_record})
        else:
            my_deliverable_detail_record = Deliverable()
            return render(request, 'create_deliverable.html', {'my_deliverable_detail_record': my_deliverable_detail_record})
    elif request.POST.get('deployment_save_close'):
        my_deployment_detail_record = save(request)
        my_deliverable_detail_record = Deliverable.objects.get(id=int(request.POST['deliverable_id']))
        return render(request, 'create_deliverable.html', {'my_deliverable_detail_record':my_deliverable_detail_record})
    else:
        my_deployment_detail_record = save(request)
        return render(request, 'deployment_detail.html', {'my_deployment_detail_record': my_deployment_detail_record})


def save(request):
    if request.POST['deliverable_id'] == '':
        my_deliverable_id = 0
    else:
        my_deliverable_id = int(request.POST['deliverable_id'])

    if request.POST['days_to_complete'] == '':
        my_days_to_complete_course = 0
    else:
        my_days_to_complete_course = int(request.POST['days_to_complete'])

    my_course_exam = "course_exam" in request.POST
    if my_course_exam:
        exam_boolean = 'true'
    else:
        exam_boolean = 'false'
    my_queryset = DeploymentDetail.objects.filter(deliverable_id=my_deliverable_id)
    if not my_queryset:
        my_deployment_detail_record = DeploymentDetail(deliverable_id=my_deliverable_id,category=request.POST['category'],project_code=request.POST['project_code'],course_order=request.POST['course_order'],curriculum_name=request.POST['curriculum_name'],curriculum_description=request.POST['curriculum_description'],course_name=request.POST['course_name'],course_description=request.POST['course_description'],days_to_complete_course=my_days_to_complete_course,course_duration=request.POST['course_duration'],course_key_words=request.POST['course_key_words'], course_exam= exam_boolean, approved_audience=request.POST['approved_audience'])
        my_deployment_detail_record.save()
    else:
        my_queryset[0].category = request.POST['category']
        my_queryset[0].project_code = request.POST['project_code']
        my_queryset[0].course_order = request.POST['course_order']
        my_queryset[0].curriculum_name = request.POST['curriculum_name']
        my_queryset[0].curriculum_description = request.POST['curriculum_description']
        my_queryset[0].course_name = request.POST['course_name']
        my_queryset[0].course_description = request.POST['course_description']
        my_queryset[0].days_to_complete_course = my_days_to_complete_course
        my_queryset[0].course_duration = request.POST['course_duration']
        my_queryset[0].course_key_words = request.POST['course_key_words']
        my_queryset[0].course_exam = exam_boolean
        my_queryset[0].approved_audience = request.POST['approved_audience']
        my_deployment_detail_record = my_queryset[0]
        my_deployment_detail_record.save()
    return my_deployment_detail_record