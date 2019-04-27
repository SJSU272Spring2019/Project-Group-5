from django.shortcuts import render
from deliverable_detail.models import Deliverable
from deployment_detail.models import DeploymentDetail
from authenticate.models import UserProfile
from django.db.models import Q
# Create your views here.
# TODO Add 'New" to the queue selection dropdown
# TODO Get functionality in the search box working


def index(request):
    if not request.user.is_authenticated:
        user_message = "Please login to access the Training Management System"
        return render(request, 'login.html', {'user_message': user_message})
    deliverable_records = Deliverable.objects.filter(status='2) Develop')
    return render(request, 'queue_page.html', {'deliverable_records': deliverable_records, 'profile_info':UserProfile.objects.get(username=request.user.username)} )

def create_deliverable(request):
    if not request.user.is_authenticated:
        user_message = "Please login to access the Training Management System"
        return render(request, 'login.html', {'user_message': user_message})
    return render(request, 'detail/create_deliverable.html')

def queue_submit(request):
    if not request.user.is_authenticated:
        user_message = "Please login to access the Training Management System"
        return render(request, 'login.html', {'user_message': user_message})
    if request.POST.get('search'):
        search_terms = request.POST['search_box']
        deliverable_records = Deliverable.objects.filter(
            Q(course_name__contains=request.POST['search_box']) |
            Q(category__contains = request.POST['search_box']) |
            Q(project_lead__contains = request.POST['search_box'])).order_by('status')
        if not deliverable_records:
            if request.POST['search_box'].isdigit():
                deliverable_records = Deliverable.objects.filter(id=int(request.POST['search_box']))
        return render(request,'queue_page.html', {'deliverable_records': deliverable_records, 'search_terms' : search_terms, 'profile_info':UserProfile.objects.get(username=request.user.username)})


    if request.POST.get('deployment_queue'):
        deployment_records = DeploymentDetail.objects.filter(deployment_status='Open').order_by('project_code', 'course_order')
        return render(request, 'deployment_queue.html', {'deployment_records': deployment_records, 'profile_info': UserProfile.objects.get(username=request.user.username)})

    if request.POST.get('create_account'):
        return render(request, 'create_account.html',{'profile_info':UserProfile.objects.get(username=request.user.username)})


    if request.POST.get('create_deliverable'):
        return render(request, 'create_deliverable.html', {'profile_info':UserProfile.objects.get(username=request.user.username)})
    if request.POST.get('selection'):
        if request.POST.get('selection') == 'Develop Queue':
            selection_value = 'Develop Queue'
            deliverable_records = Deliverable.objects.filter(status='2) Develop')
        elif request.POST.get('selection') == 'Record Queue':
            selection_value = 'Record Queue'
            deliverable_records = Deliverable.objects.filter(status='3) Record')
        elif request.POST.get('selection') == 'Post Processing Queue':
            selection_value = 'Post Processing Queue'
            deliverable_records = Deliverable.objects.filter(status='4) Post-Processing')
        elif request.POST.get('selection') == 'Deployment Queue':
            selection_value = 'Deployment Queue'
            deliverable_records = Deliverable.objects.filter(status='5) Deploy')
        elif request.POST.get('selection') == 'Show All Deliverables':
            selection_value = 'Show All Deliverables'
            deliverable_records = Deliverable.objects.all().order_by('status')

    else:
        deliverable_records = Deliverable.objects.filter(status='2) Develop')
    return render(request, 'queue_page.html', {'deliverable_records': deliverable_records, 'selection_value' : selection_value, 'profile_info':UserProfile.objects.get(username=request.user.username)})

def logout(request):
    return render(request, '/', )
