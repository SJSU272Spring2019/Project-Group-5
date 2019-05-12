from django.shortcuts import render
from django.http import HttpResponse
from . models import Deliverable
from datetime import datetime
from deployment_detail.models import DeploymentDetail
from authenticate.models import UserProfile
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
import smtplib, ssl

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        user_message = "Please login to access the Training Management System"
        return render(request, 'login.html', {'user_message': user_message})
    return render(request, 'create_deliverable.html', {'profile_info': UserProfile.objects.get(username=request.user.username) })



def deliverable_detail_submit(request):
    if not request.user.is_authenticated:
        user_message = "Please login to access the Training Management System"
        return render(request, 'login.html', {'user_message': user_message})

    if request.POST.get('deploy_button'):
        my_deliverable_detail_record = save_detail(request)
        temp_deployment_record = DeploymentDetail.objects.filter(deliverable_id=my_deliverable_detail_record.id)
        if not temp_deployment_record:
            # deliverable_record = Deliverable.objects.get(id=int(request.POST['deliverable_id']))
            my_deployment_detail_record = DeploymentDetail()
            my_deployment_detail_record.deliverable_id = my_deliverable_detail_record.id
            my_deployment_detail_record.course_name = request.POST['course_name']
            my_deployment_detail_record.course_description = request.POST['course_description']
            my_deployment_detail_record.category = request.POST['category']
            my_deployment_detail_record.project_code = request.POST['project_code']
        else:
            my_deployment_detail_record = temp_deployment_record[0]

        return render(request, 'deployment_detail.html', {'my_deployment_detail_record':my_deployment_detail_record, 'profile_info': UserProfile.objects.get(username=request.user.username)})
    if request.POST.get('cancel_button'):
        deliverable_records = Deliverable.objects.filter(status='2) Develop')
        return render(request, 'queue_page.html', {'deliverable_records': deliverable_records , 'profile_info': UserProfile.objects.get(username=request.user.username)})
    if request.POST.get('save'):
        my_deliverable_detail_record=save_detail(request)
        my_directory = request.POST.get('deliverable_id') + '/'
        try:
            fs = FileSystemStorage()
            list_names = ''
            for filename in fs.listdir(request.POST.get('deliverable_id'))[1]:
                list_names = list_names + '<a href="http://127.0.0.1:8000/detail/delete_link?delete_file=' + filename + '&deliverable_id=' + request.POST.get('deliverable_id') + '"> Delete File</a> &nbsp; &nbsp; &nbsp; &nbsp;<a href="http://127.0.0.1:8000/media/' + my_directory + filename + '" target="_blank">' + filename + '</a><br><br>'
        except FileNotFoundError:
            list_names = '<div align="center">No attached files</div>'
        return render(request, 'create_deliverable.html', {'my_deliverable_detail_record': my_deliverable_detail_record, 'profile_info': UserProfile.objects.get(username=request.user.username),'my_links': list_names})
    if request.POST.get('save_exit'):
        my_deliverable_detail_record = save_detail(request)
        deliverable_records = Deliverable.objects.filter(status='2) Develop')
        return render(request, 'queue_page.html', {'deliverable_records': deliverable_records, 'profile_info': UserProfile.objects.get(username=request.user.username)})
    if request.POST.get('upload_file'):
        my_deliverable_detail_record = save_detail(request)
        try:
            my_directory = request.POST.get('deliverable_id') + '/'
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            fs.delete(my_directory + uploaded_file.name)
            name = fs.save(my_directory + uploaded_file.name, uploaded_file)
        except MultiValueDictKeyError:
            print('MultiValueDictKeyError')

        try:
            fs = FileSystemStorage()
            list_names = ''
            for filename in fs.listdir(request.POST.get('deliverable_id'))[1]:
                list_names = list_names + '<a href="http://127.0.0.1:8000/detail/delete_link?delete_file=' + filename + '&deliverable_id=' + request.POST.get('deliverable_id') + '"> Delete File</a> &nbsp; &nbsp; &nbsp; &nbsp;<a href="http://127.0.0.1:8000/media/' + my_directory + filename + '" target="_blank">' + filename + '</a><br><br>'

        except FileNotFoundError:
            list_names = '<div align="center">No attached files</div>'
        deliverable_records = Deliverable.objects.filter(status='2) Develop')
        return render(request, 'create_deliverable.html', {'my_deliverable_detail_record': my_deliverable_detail_record,'profile_info': UserProfile.objects.get(username=request.user.username),'my_links': list_names})


def save_detail(request):
    if not request.user.is_authenticated:
        user_message = "Please login to access the Training Management System"
        return render(request, 'login.html', {'user_message': user_message})
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
        # if this is a new item being saved into status of record send a notification to everyone with a role of Media Services

    else:
        my_queryset = Deliverable.objects.filter(id=int(request.POST['deliverable_id']))
        my_deliverable_detail_record = my_queryset[0]
        previous_status = my_deliverable_detail_record.status
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

# If the existing record is being changed from some other status to Record - send a notification.  Need to replicate this in the save new section above in case a new record is saves as record
        if my_deliverable_detail_record.status == '3) Record' and previous_status != '3) Record':
            email_body = 'There is a new Sales Training Deliverable ready to be recorded.  Please contact ' + my_deliverable_detail_record.project_lead + ' for more information.  The Deliverable ID is: ' + str(my_deliverable_detail_record.id)
            my_profileset = UserProfile.objects.filter(role='Media Services')
            to_address = ''
            for my_profile in my_profileset:
                my_userset = User.objects.filter(username=my_profile.username)
                to_address = to_address + my_userset[0].email +','
            from_address = "trainingmanagementcmpe272"
            password = 'rakeshranjan'
            my_subject = 'Training Management System Notification: New deliverable ready to record'
            my_message = 'Subject: {}\n\n{}'.format(my_subject, email_body)
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
            server.login(from_address, password)
            server.sendmail('braddfoy@gmail.com', to_address, my_message )
            server.quit()
# end notification code


    return my_deliverable_detail_record

def queue_page(request):
    if not request.user.is_authenticated:
        user_message = "Please login to access the Training Management System"
        return render(request, 'login.html', {'user_message': user_message})
    return render(request, 'queue_page.html', {'profile_info': UserProfile.objects.get(username=request.user.username)})


def deliverable_link(request):
    if not request.user.is_authenticated:
        user_message = "Please login to access the Training Management System"
        return render(request, 'login.html', {'user_message': user_message})
    try:
        my_directory = request.GET['deliverable_id'] + '/'
        fs = FileSystemStorage()
        list_names = ''
        for filename in fs.listdir(request.GET['deliverable_id'])[1]:
            list_names = list_names + '<a href="http://127.0.0.1:8000/detail/delete_link?delete_file=' + filename + '&deliverable_id=' + request.GET['deliverable_id'] + '"> Delete File</a> &nbsp; &nbsp; &nbsp; &nbsp;<a href="http://127.0.0.1:8000/media/' + my_directory + filename + '" target="_blank">' + filename + '</a><br><br>'
    except FileNotFoundError:
        list_names = '<div align="center">No attached files</div>'
    my_deliverable_detail_record = Deliverable.objects.filter(id=int(request.GET['deliverable_id']))
    return render(request, 'create_deliverable.html', {'my_deliverable_detail_record': my_deliverable_detail_record[0], 'profile_info': UserProfile.objects.get(username=request.user.username),'my_links': list_names})


def delete_link(request):
    if not request.user.is_authenticated:
        user_message = "Please login to access the Training Management System"
        return render(request, 'login.html', {'user_message': user_message})
    my_directory = request.GET['deliverable_id'] + '/'
    try:
        fs = FileSystemStorage()
        fs.delete(my_directory + request.GET['delete_file'])
        list_names = ''
        for filename in fs.listdir(request.GET['deliverable_id'])[1]:
            list_names = list_names + '<a href="http://127.0.0.1:8000/detail/delete_link?delete_file=' + filename + '&deliverable_id=' + request.GET['deliverable_id'] + '"> Delete File</a> &nbsp; &nbsp; &nbsp; &nbsp;<a href="http://127.0.0.1:8000/media/' + my_directory + filename + '" target="_blank">' + filename + '</a><br><br>'
    except FileNotFoundError:
        list_names = '<div align="center">No attached files</div>'
    my_deliverable_detail_record = Deliverable.objects.filter(id=int(request.GET['deliverable_id']))
    return render(request, 'create_deliverable.html', {'my_deliverable_detail_record': my_deliverable_detail_record[0],
                                                       'profile_info': UserProfile.objects.get(
                                                           username=request.user.username), 'my_links': list_names})


# remove everything below this line
def upload_button(request):
    context = {}
    if request.method == 'POST':
        my_directory = '23/'
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save('23/' + uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        context['fname'] = name
        list_names = ''
        for filename in fs.listdir('23')[1]:
            list_names = list_names + '<a href="http://127.0.0.1:8000/detail/delete_link?delete_file=' + filename + '&deliverable_id=' + request.GET['deliverable_id'] + '"> Delete File</a> &nbsp; &nbsp; &nbsp; &nbsp;<a href="http://127.0.0.1:8000/media/' + my_directory + filename + '" target="_blank">' + filename + '</a><br><br>'
        context['myLinks'] = list_names
        print(uploaded_file.name)
        print(uploaded_file.size)
    return render(request, 'index.html', context)
# remove end