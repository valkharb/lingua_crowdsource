from django.forms import ModelForm
import django
from django.forms import Form
from .models import LitWork, Collection
from django.contrib.auth.models import User


class WorkForm(ModelForm):
    class Meta:
        model = LitWork
        fields = ('title', 'sub_title', 'file','is_published','publish_title', 'publisher_title',
                  'publish_date','version_type','collection')

class NewWorkForm(ModelForm):
    class Meta:
        model = LitWork
        fields = '__all__'

class NewCollForm(ModelForm):
    class Meta:
        model = Collection
        fields = '__all__'

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name','email')

class FiltersForm(Form):
    main = 'MN'
    draft = 'DF'
    edition = 'ED'
    list = 'LS'
    version_types = ((main, 'Основная редакция'), (draft, 'Черновик'), (edition, 'Редакция'), (list, 'Список'))
    title = django.forms.CharField(label='Название произведения')
    status = django.forms.BooleanField(label='Опубликовано')
    live_status = django.forms.BooleanField(label='Опубликовано при жизни')
    date = django.forms.DateTimeField(label='Дата написания')
    genre = django.forms.CharField(label='Жанр')
    genus = django.forms.CharField(label='Род')
    measure = django.forms.CharField(label='Метр')
    redaction = django.forms.ChoiceField(label='Тип редакции', choices=version_types)
    collection = django.forms.ChoiceField(label='Коллекция')
    published = django.forms.DateTimeField(label='Добавлено')

