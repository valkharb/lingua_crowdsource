from django.shortcuts import render
from cabinet.models import LitWork
from django.shortcuts import render, get_object_or_404
# Create your views here.
def lit_work_list(request):
    works = LitWork.objects.all()
    return render(request, 'cabinet/lit_work_list.html', {'works': works})

def work_detail(request, pk):
    work = get_object_or_404(LitWork, pk=pk)
    return render(request, 'cabinet/work_detail.html', {'work': work})