from django.shortcuts import render_to_response
from cabinet.models import LitWork
from django.shortcuts import render, get_object_or_404
from .forms import WorkForm
from django.shortcuts import redirect
from django.utils import timezone
# Create your views here.
def lit_work_list(request):
    works = LitWork.objects.all()
    return render(request, 'cabinet/lit_work_list.html', {'works': works})

def work_detail(request, pk):
    work = get_object_or_404(LitWork, pk=pk)
    return render(request, 'cabinet/work_detail.html', {'work': work})


def work_new(request):
    if request.method == "POST":
        form = WorkForm(request.POST)
        if form.is_valid():
            work = form.save(commit=False)
            work.owner_id = request.user.id
            work.published_date = timezone.now()
            work.save()
            return redirect('work_detail', pk=work.pk)

        else: return render_to_response('cabinet/errors.html', {'form': form})
    else:
        form = WorkForm()
    return render(request, 'cabinet/work_new.html', {'form': form})

def work_edit(request, pk):
        work = get_object_or_404(LitWork, pk=pk)
        if request.method == "POST":
            form = WorkForm(request.POST, instance=work)
            if form.is_valid():
                work = form.save(commit=False)
                work.owner_id = request.user.id
                work.published_date = timezone.now()
                work.save()
                return redirect('work_detail', pk=work.pk)
        else:
            form = WorkForm(instance=work)
        return render(request, 'cabinet/work_new.html', {'form': form})
def mark_up(request, pk):
    work = get_object_or_404(LitWork, pk=pk)
    if request.method == "GET":
        work_to_mark = LitWork.objects.get(pk=pk)
        work_to_mark.mark_up()
    return render(request, 'cabinet/work_detail.html', {'work': work})