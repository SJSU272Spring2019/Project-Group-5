from django.shortcuts import render
from . models import DeploymentDetail
from deliverable_detail.models import Deliverable
from authenticate.models import UserProfile
from django.core.files.storage import FileSystemStorage

def index(request): # This line should be removed
    return render(request, 'index.html')  # This line should be removed


def deployment_detail(request):
    if not request.user.is_authenticated:
        user_message = "Please login to access the Training Management System"
        return render(request, 'login.html', {'user_message': user_message})
    return render(request, 'deployment_detail.html')

def deployment_detail_submit(request):
    if not request.user.is_authenticated:
        user_message = "Please login to access the Training Management System"
        return render(request, 'login.html', {'user_message': user_message})

    if request.POST.get('deployment_cancel') == 'Cancel':
        if request.POST['deliverable_id'] != '':
            my_deliverable_detail_record = Deliverable.objects.get(id=int(request.POST['deliverable_id']))
            my_directory = request.POST.get('deliverable_id') + '/'
            try:
                fs = FileSystemStorage()
                list_names = ''
                for filename in fs.listdir(request.POST.get('deliverable_id'))[1]:
                    list_names = list_names + '<a href="http://127.0.0.1:8000/detail/delete_link?delete_file=' + filename + '&deliverable_id=' + request.POST.get('deliverable_id') + '"> Delete File</a> &nbsp; &nbsp; &nbsp; &nbsp;<a href="http://127.0.0.1:8000/media/' + my_directory + filename + '" target="_blank">' + filename + '</a><br><br>'
            except FileNotFoundError:
                list_names = '<div align="center">No attached files</div>'
            return render(request, 'create_deliverable.html', {'my_deliverable_detail_record':my_deliverable_detail_record, 'profile_info':UserProfile.objects.get(username=request.user.username),'my_links': list_names})
        else:
            my_deliverable_detail_record = Deliverable()
            return render(request, 'create_deliverable.html', {'my_deliverable_detail_record': my_deliverable_detail_record, 'profile_info':UserProfile.objects.get(username=request.user.username)})
    elif request.POST.get('deployment_save_close'):
        my_deployment_detail_record = save(request)
        my_directory = request.POST.get('deliverable_id') + '/'
        try:
            fs = FileSystemStorage()
            list_names = ''
            for filename in fs.listdir(request.POST.get('deliverable_id'))[1]:
                list_names = list_names + '<a href="http://127.0.0.1:8000/detail/delete_link?delete_file=' + filename + '&deliverable_id=' + request.POST.get('deliverable_id') + '"> Delete File</a> &nbsp; &nbsp; &nbsp; &nbsp;<a href="http://127.0.0.1:8000/media/' + my_directory + filename + '" target="_blank">' + filename + '</a><br><br>'
        except FileNotFoundError:
            list_names = '<div align="center">No attached files</div>'
        my_deliverable_detail_record = Deliverable.objects.get(id=int(request.POST['deliverable_id']))
        return render(request, 'create_deliverable.html', {'my_deliverable_detail_record':my_deliverable_detail_record, 'profile_info':UserProfile.objects.get(username=request.user.username),'my_links': list_names})
    else:
        my_deployment_detail_record = save(request)
        return render(request, 'deployment_detail.html', {'my_deployment_detail_record': my_deployment_detail_record, 'profile_info':UserProfile.objects.get(username=request.user.username)})


def save(request):
    if not request.user.is_authenticated:
        user_message = "Please login to access the Training Management System"
        return render(request, 'login.html', {'user_message': user_message})

    if request.POST['deliverable_id'] == '':
        my_deliverable_id = 0
    else:
        my_deliverable_id = int(request.POST['deliverable_id'])

    if request.POST['days_to_complete'] == '':
        my_days_to_complete_course = 0
    else:
        try:
            my_days_to_complete_course = int(request.POST['days_to_complete'])
        except(ValueError):
            my_days_to_complete_course=0

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