from django.shortcuts import render
from deliverable_detail.models import Deliverable
from deployment_detail.models import DeploymentDetail
from authenticate.models import UserProfile
# Create your views here.
# TODO Add 'New" to the queue selection dropdown
# TODO Get functionality in the search box working


def index(request):
    deliverable_records = Deliverable.objects.filter(status='2) Develop')
    profile_info = UserProfile.objects.get(username=request.user.username)
    return render(request, 'queue_page.html', {'deliverable_records': deliverable_records, 'role':profile_info.role})

def create_deliverable(request):
    return render(request, 'detail/create_deliverable.html')

def queue_submit(request):
    if request.POST.get('search'):
        search_terms = request.POST['search_box']
        deliverable_records = Deliverable.objects.filter(course_name__contains=request.POST['search_box'])
        if not deliverable_records:
            if request.POST['search_box'].isdigit():
                deliverable_records = Deliverable.objects.filter(id=int(request.POST['search_box']))
        return render(request,'queue_page.html', {'deliverable_records': deliverable_records, 'search_terms' : search_terms})


    if request.POST.get('deployment_queue'):
        deployment_records = DeploymentDetail.objects.filter(deployment_status='Open').order_by('project_code', 'course_order')
        return render(request, 'deployment_queue.html', {'deployment_records': deployment_records})

    if request.POST.get('create_account'):
        return render(request, 'create_account.html')


    if request.POST.get('create_deliverable'):
        return render(request, 'create_deliverable.html')
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
    return render(request, 'queue_page.html', {'deliverable_records': deliverable_records, 'selection_value' : selection_value})

