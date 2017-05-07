import lxml
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from cabinet.models import LitWork, Author, Collection, Marks, MarkUp, Sentence, Paragraph, Word,PublishingHouse, Tags , Search
from django.shortcuts import render, get_object_or_404
from .forms import WorkForm, UserForm, TextFiltersForm, WordFiltersForm, NewCollForm, WordForm, TagForm, PubForm, MarkForm
from django.shortcuts import redirect
from django.utils import timezone
import pymorphy2
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.contrib.auth.models import User
import pymysql
db= pymysql.connect(host='localhost', user='val', passwd='1111', db='diploma_project' , charset='utf8')
import json
from django.db.models import Count, Avg
from django.utils.http import is_safe_url
from pynlpl.formats import folia


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
    p_count = len(Paragraph.objects.filter(lit_work_id=pk))
    ids = Paragraph.objects.values_list('id', flat=True).filter(lit_work_id=pk)
    sentences = Sentence.objects.filter(paragraph_id__in=set(ids))
    s_count = len(sentences)
    s_ids =  Sentence.objects.values_list('id', flat=True).filter(paragraph_id__in=set(ids))
    aaa = Sentence.objects.annotate(num=Count('word'))
    w_count = aaa.aggregate(Avg('num'))
    w_pars = Paragraph.objects.annotate(count = Count('sentence'))
    p_length = w_pars.aggregate(Avg('count'))
    if p_length['count__avg']:
        p_length['count__avg'] = round(p_length['count__avg'])
    if w_count['num__avg']:
        w_count['num__avg'] = round(w_count['num__avg'])
    return render(request, 'cabinet/work_detail.html', {'work': work, 's_count': s_count, 'w_count':w_count['num__avg'],
                                                        'p_count':p_count, 'p_length':p_length['count__avg']})

def coll_detail(request, pk):
    coll = get_object_or_404(Collection, pk=pk)
    return render(request, 'cabinet/coll_detail.html', {'coll': coll})

def pub_detail(request, pk):
    pub = get_object_or_404(PublishingHouse, pk=pk)
    return render(request, 'cabinet/pub_detail.html', {'pub': pub})

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
        publishers  = PublishingHouse.objects.filter(owner = request.user)
        searches = Search.objects.filter(owner=request.user)
        return render(request, 'cabinet/account.html', {'user': user, 'works': works, 'collections': collections, 'publishers': publishers, 'searches':searches})
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

def view_paragraph(request,pk):
    word = get_object_or_404(MarkUp, pk=pk)
    return render(request, 'cabinet/view_paragraph.html', {'word': word})

def word_edit(request,pk):
    word = get_object_or_404(MarkUp, pk=pk)
    if request.method == "POST":
        form = WordForm(request.POST, instance=word)
        if form.is_valid():
            word = form.save(commit=False)
            word.save()
            return redirect('view_paragraph', pk=word.pk)
        else:
            return render_to_response('cabinet/errors.html', {'form': form})
    else:
        form = WordForm(instance=word)
        return render(request, 'cabinet/word_edit.html', {'form': form})

def work_new(request):
    if request.method == "POST":
        form = WorkForm(request.POST, request.FILES)
        morph = pymorphy2.MorphAnalyzer()
        if form.is_valid():
            work = form.save(commit=False)
            work.owner_id = request.user.id
            work.published_date = timezone.now()
            work.save()
            work.mark_up(morph)
            return redirect('work_detail', pk=work.pk)
        else:
            return render_to_response('cabinet/errors.html', {'form': form})
    else:
        form = WorkForm()
        return render(request, 'cabinet/work_new.html', {'form': form})

def add_tag(request, id, type):
    if request.method == "POST":
        POST = request.POST.copy()
        POST['el_type'] = type
        POST['el_id'] = id
        form = TagForm(POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.save()
            next = request.GET.get('next', '/')
            # check that next is safe
            if not is_safe_url(next):
                next = '/'
            return redirect(next)
        else:
            return render_to_response('cabinet/errors.html', {'form': form})
    else:
        form = TagForm()
        return render(request, 'cabinet/add_tag.html', {'form': form})

def save_search(request):
    Search.objects.create(data=request.body.decode('utf-8'),
                          owner=request.user,
                          created_date=timezone.now())

def add_mark(request, pk, type):
    if request.method == "POST":
        POST = request.POST.copy()
        POST['object_type'] = type
        POST['object'] = pk
        form = MarkForm(POST)
        if form.is_valid():
            mark = form.save(commit=False)
            author = request.user
            mark.save()
            next = request.GET.get('next', '/')
            # check that next is safe
            if not is_safe_url(next):
                next = '/'
            return redirect(next)
        else:
            return render_to_response('cabinet/errors.html', {'form': form})
    else:
        form = MarkForm()
        return render(request, 'cabinet/add_mark.html', {'form': form})

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

def pub_new(request):
    if request.method == "POST":
        form = PubForm(request.POST)
        if form.is_valid():
            work = form.save(commit=False)
            work.owner_id = request.user.id
            work.created_date = timezone.now()
            work.save()
            return redirect('publishers_list')

        else:
            return render_to_response('cabinet/errors.html', {'form': form})
    else:
        form = PubForm()
    return render(request, 'cabinet/pub_new.html', {'form': form})

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

def parent_model(self):
    return self._meta.object_name

def concordance(request):
    params = json.loads(request.body.decode('utf-8'))
    work_query = params['work']
    params['word']['value'] = params['word'].pop('title')
    word_query = params['word']
    # final2 = Word.objects.filter(**word_query)
    params['word']['word'] = params['word'].pop('value')
    mark_query = params['word']
    final1 = LitWork.objects.filter(**work_query)
    final2 = MarkUp.objects.filter(**mark_query)
    words = MarkUp.objects.values_list('word', flat=True).distinct().filter(**mark_query)
    ids = MarkUp.objects.values_list('id', flat=True).filter(word__in=words)
    tags = Tags.objects.filter(el_type='word').filter(el_id__in=set(ids))
    form1 = TextFiltersForm()
    form2 = WordFiltersForm()
    return render(request, 'cabinet/results.html', {'works': final1, 'words': final2, 'tags': tags, 'form1': form1, 'form2': form2})

def cql(request):
    return render(request, 'cabinet/cql.html')

def cql_search(request):
    from pynlpl.formats import fql, cql
    params = json.loads(request.body.decode('utf-8'))
    doc = folia.Document(id='doc')
    text = folia.Text(doc, id='doc.text')
    sentences = Sentence.objects.all()
    for s in sentences:
        sen = text.append(folia.Sentence(doc,id=doc.id + '.s.'+str(s.id)))
        words = Word.objects.filter(Sentence_id=s.id)
        for w in words:
            sen.append(folia.Word(doc,id=doc.id + '.s.'+str(s.id)+'.w.'+str(w.id), text=w.value))
    doc.append(text)
    query = fql.Query(cql.cql2fql(params['title']))
    texts = query(doc)
    return render(request, 'cabinet/cql_results.html', {'texts': texts})
