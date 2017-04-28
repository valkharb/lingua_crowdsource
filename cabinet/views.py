from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from cabinet.models import LitWork, Author, Collection, PublishingHouse
from django.shortcuts import render, get_object_or_404
from .forms import WorkForm, NewWorkForm, UserForm, TextFiltersForm, WordFiltersForm, NewCollForm
from django.shortcuts import redirect
from django.utils import timezone
import pymorphy2
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.contrib.auth.models import User
from django.template import RequestContext


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


def coll_detail(request, pk):
    coll = get_object_or_404(Collection, pk=pk)
    return render(request, 'cabinet/coll_detail.html', {'coll': coll})


def authors_list(request):
    authors = Author.objects.all()
    return render(request, 'cabinet/authors_list.html', {'authors': authors})


def collections_list(request):
    collections = Collection.objects.all()
    return render(request, 'cabinet/collections_list.html', {'collections': collections})


def publishers_list(request):
    publishers = PublishingHouse.objects.all()
    return render(request, 'cabinet/publishers_list.html', {'publishers': publishers})


def account(request, pk):
    try:
        user = User.objects.get(pk=pk)
        works = LitWork.objects.filter(owner=request.user)
        collections = Collection.objects.filter(owner=request.user)
        return render(request, 'cabinet/account.html', {'user': user, 'works': works, 'collections': collections})
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


def statistics(request):
    return render(request, 'cabinet/statistics.html')


def work_filters(request):
    if request.method == "POST":
        form = WorkForm(request.POST)
        if form.is_valid():
            work = form.save(commit=False)
            work.owner_id = request.user.id
            work.published_date = timezone.now()
            work.save()
            return redirect('filters')

        else:
            return render_to_response('cabinet/errors.html', {'form': form})
    else:
        form1 = TextFiltersForm()
        form2 = WordFiltersForm()
    return render(request, 'cabinet/search.html', {'form1': form1, 'form2': form2})


def my_works(request):
    works = LitWork.objects.filter(owner=request.user)
    return render(request, 'cabinet/my.html', {'works': works})


def work_results(request):
    works = LitWork.objects.all()
    return render(request, 'cabinet/results.html', {'works': works})


def work_new(request):
    if request.method == "POST":
        form = NewWorkForm(request.POST)
        if form.is_valid():
            work = form.save(commit=False)
            work.owner_id = request.user.id
            work.published_date = timezone.now()
            work.save()
            return redirect('work_detail', pk=work.pk)

        else:
            return render_to_response('cabinet/errors.html', {'form': form})
    else:
        form = NewWorkForm()
    return render(request, 'cabinet/work_new.html', {'form': form})


def collection_new(request):
    if request.method == "POST":
        form = WorkForm(request.POST)
        if form.is_valid():
            work = form.save(commit=False)
            work.owner_id = request.user.id
            work.created_date = timezone.now()
            work.save()
            return redirect('collections_list')

        else:
            return render_to_response('cabinet/errors.html', {'form': form})
    else:
        form = NewCollForm()
    return render(request, 'cabinet/collection_new.html', {'form': form})


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

def sentences(request, pk):
    work = get_object_or_404(LitWork, pk=pk)
    if request.method == "GET":
        work = LitWork.objects.get(pk=pk)
        count = work.sentences()
        return render(request, 'cabinet/work_detail.html', {'work': work , 'sentences': count})


def analysis(request, pk):
    work = get_object_or_404(LitWork, pk=pk)
    if request.method == "GET":
        work = LitWork.objects.get(pk=pk)
        count = work.analysis()
        return render(request, 'cabinet/work_detail.html', {'work': work, 'analysed': count})


def concordance(request):
    works = LitWork.objects.all()
    form1 = TextFiltersForm()
    form2 = WordFiltersForm()
    request_context = RequestContext(request)
    return render(request, 'cabinet/results.html', {'works': works, 'form1': form1, 'form2': form2})
