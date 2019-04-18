from django.shortcuts import render
from deliverable_detail.models import Deliverable
# Create your views here.

def index(request):
    deliverable_records = Deliverable.objects.filter(status='2) Develop')
    return render(request, 'queue_page.html', {'deliverable_records': deliverable_records})

def create_deliverable(request):
    return render(request, 'detail/create_deliverable.html')

def queue_submit(request):
    if request.POST.get('create_deliverable'):
        return render(request, 'create_deliverable.html')
