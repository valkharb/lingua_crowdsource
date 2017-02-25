from django.shortcuts import render
from cabinet.models import LitWork
# Create your views here.
def lit_work_list(request):
    works = LitWork.objects.all()
    return render(request, 'cabinet/lit_work_list.html', {'works': works})