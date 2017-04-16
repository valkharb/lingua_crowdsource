from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from cabinet.models import LitWork
from django.shortcuts import render, get_object_or_404
from .forms import WorkForm
from .forms import UserForm
from .forms import FiltersForm
from django.shortcuts import redirect
from django.utils import timezone
import pymorphy2
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.contrib.auth.models import User

def reset_confirm(request, uidb36=None, token=None):
    return password_reset_confirm(request, template_name='registration/password_reset_confirm.html',
        uidb36=uidb36, token=token, post_reset_redirect=reverse('cabinet:login'))


def reset(request):
    return password_reset(request, template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_email.txt',
        post_reset_redirect=reverse('cabinet:login'))

def base(request):
    return render(request, 'registration/base.html')

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Правильный пароль и пользователь "активен"
        auth.login(request, user)
        # Перенаправление на "правильную" страницу
        return HttpResponseRedirect("/account/loggedin/")
    else:
        # Отображение страницы с ошибкой
        return HttpResponseRedirect("/account/invalid/")

def logout(request):
    auth.logout(request)
    # Перенаправление на страницу.
    return HttpResponseRedirect("/account/loggedout/")


def lit_work_list(request):
    works = LitWork.objects.all()
    return render(request, 'cabinet/lit_work_list.html', {'works': works})

def work_detail(request, pk):
    work = get_object_or_404(LitWork, pk=pk)
    return render(request, 'cabinet/work_detail.html', {'work': work})

def account(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return render(request, 'cabinet/account.html', {'user': user})
    except  User.DoesNotExist:
        get_object_or_404(User, pk=pk)

def account_form(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.last_name = user.last_name
            user.first_name = user.first_name
            user.email = user.email
            user.save()
            return redirect('account', pk=user.pk)
    else:
        form = UserForm(instance=user)
    return render(request, 'cabinet/account_form.html', {'form': form})

def work_search(request):
    works = LitWork.objects.all()
    return render(request, 'cabinet/search.html', {'works': works})

def work_filters(request):
    if request.method == "POST":
        form = WorkForm(request.POST)
        if form.is_valid():
            work = form.save(commit=False)
            work.owner_id = request.user.id
            work.published_date = timezone.now()
            work.save()
            return redirect('filters')

        else: return render_to_response('cabinet/errors.html', {'form': form})
    else:
        form = FiltersForm()
    return render(request, 'cabinet/search.html', {'form': form})

def work_results(request):
    work_filters(request)
    works = LitWork.objects.all()
    return render(request, 'cabinet/results.html', {'works': works})

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
        morph = pymorphy2.MorphAnalyzer()
        work_to_mark.mark_up(morph)
    return render(request, 'cabinet/work_detail.html', {'work': work})