from django.forms import ModelForm
import django
from django.forms import Form
from .models import LitWork, Collection, MarkUp, Tags,PublishingHouse
from django.contrib.auth.models import User
import pymorphy2


class TagForm(ModelForm):
    class Meta:
        model = Tags
        fields = '__all__'

class PubForm(ModelForm):
    class Meta:
        model = PublishingHouse
        fields = '__all__'

class WorkForm(ModelForm):
    class Meta:
        model = LitWork
        fields = '__all__'
        file = django.forms.FileField(label='Текст произведения', widget=django.forms.FileInput(attrs={'class':'file_upload'}))

class WordForm(ModelForm):
    class Meta:
        model = MarkUp
        exclude = ('word','count', 'sentence',)

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

class TextFiltersForm(Form):
    main = 'MN'
    draft = 'DF'
    edition = 'ED'
    list = 'LS'
    none='none'
    version_types = ((none,''),(main, 'Основная редакция'), (draft, 'Черновик'), (edition, 'Редакция'), (list, 'Список'))
    status = django.forms.BooleanField(label='Опубликовано', widget=django.forms.CheckboxInput(attrs={'data-name':'is_published', 'class':'filter work'}))
    live_status = django.forms.BooleanField(label='Опубликовано при жизни', widget=django.forms.CheckboxInput(attrs={'data-name':'is_published_alive', 'class':'filter work'}))
    date = django.forms.DateField(label='Дата написания', widget=django.forms.DateInput(attrs={'data-name':'wrote_date', 'class':'filter work'}))
    genre = django.forms.CharField(label='Жанр', widget=django.forms.TextInput(attrs={'data-name':'genre', 'class':'filter work'}))
    genus = django.forms.CharField(label='Род', widget=django.forms.TextInput(attrs={'data-name':'genus', 'class':'filter work'}))
    measure = django.forms.CharField(label='Метр', widget=django.forms.TextInput(attrs={'data-name':'measure', 'class':'filter work'}))
    redaction = django.forms.ChoiceField(label='Тип редакции', choices=version_types, widget=django.forms.Select(attrs={'data-name':'version_type', 'class':'filter work'}))
    collection = django.forms.ChoiceField(label='Коллекция', widget=django.forms.Select(attrs={'data-name':'collection', 'class':'filter work'}))
    published = django.forms.DateField(label='Добавлено', widget=django.forms.DateInput(attrs={'data-name':'created_date', 'class':'filter work'}))

class WordFiltersForm(Form):
    morph = pymorphy2.MorphAnalyzer()
    yes = 1
    no = 2
    unknown = 0
    nomn= morph.lat2cyr('NM')
    gent=morph.lat2cyr('GN')
    datv=morph.lat2cyr('DT')
    accs=morph.lat2cyr('AC')
    ablt=morph.lat2cyr('AL')
    loct=morph.lat2cyr('LC')
    NOUN=morph.lat2cyr('NOUN')
    ADJF=morph.lat2cyr('ADJF')
    COMP=morph.lat2cyr('COMP')
    VERB=morph.lat2cyr('VERB')
    PRTF=morph.lat2cyr('PRTF')
    GRND=morph.lat2cyr('GRND')
    NUMR=morph.lat2cyr('NUMR')
    ADVB=morph.lat2cyr('ADVB')
    NPRO=morph.lat2cyr('NPRO')
    PRED=morph.lat2cyr('PRED')
    PREP=morph.lat2cyr('PREP')
    CONJ=morph.lat2cyr('CONJ')
    PRCL=morph.lat2cyr('PRCL')
    INTJ=morph.lat2cyr('INTJ')
    none='empty'
    grams = ((none,''),(NOUN,'существительное'),(ADJF,'прилагательное'),(COMP,'компаратив'),(VERB,'глагол'),
     (PRTF,'причастие'),(GRND,'деепричастие'),(NUMR,'числительное'),(ADVB,'наречие'),(NPRO,'местоимение - существительное'),
     (PRED,'предикатив'),(PREP,'предлог'),(CONJ,'союз'),(PRCL,'частица'),(INTJ,'междометие'))
    cases = ((none,''),(nomn,'Именительный'),(gent,'Родительный'),(datv,'Дательный'),(accs,'Винительный'),(ablt,'Творительный'),(loct,'Предложный'))
    moods = ((none,''),(yes, 'Повелительное'), (no, 'Изъявительное'))
    voices = ((none,''),(yes, 'Действительный'), (no, 'Страдательный'))
    rules = ((none,''),(yes, 'Да'), (no, 'Нет'))
    genders = ((none,''),(yes,'Женский'), (no,'Мужской'),(unknown, 'Средний'))
    persons = ((none,''),(yes, '1'), (no, '2'), (unknown, '3'))
    tenses = ((none,''),(yes, 'Настоящее'), (no, 'Прошедшее'), (unknown, 'Будущее'))
    numbers =  ((none,''),(yes, 'Единственное'),(no, 'Множественное'))
    grammem = django.forms.ChoiceField( label = 'Часть речи', choices = grams, widget=django.forms.Select(attrs={'data-name':'grammem', 'class':'filter word'}))
    animacy = django.forms.ChoiceField(label = 'Одушевленность', choices=rules, widget=django.forms.Select(attrs={'data-name':'animacy', 'class':'filter word'}))# одушевленность
    aspect = django.forms.ChoiceField(label = 'Совершенность', choices=rules, widget=django.forms.Select(attrs={'data-name':'aspect', 'class':'filter word'}))# вид: совершенный или несовершенный
    case = django.forms.ChoiceField( label = 'Падеж', choices = cases, widget=django.forms.Select(attrs={'data-name':'case', 'class':'filter word'}))# падеж
    gender = django.forms.ChoiceField( label = 'Род',choices=genders, widget=django.forms.Select(attrs={'data-name':'gender', 'class':'filter word'}))# род (мужской, женский, средний)
    mood = django.forms.ChoiceField( label = 'Наклонение', choices=moods, widget=django.forms.Select(attrs={'data-name':'mood', 'class':'filter word'})) # наклонение (повелительное, изъявительное)
    number = django.forms.ChoiceField( label = 'Число', choices=numbers, widget=django.forms.Select(attrs={'data-name':'number', 'class':'filter word'})) # число (единственное, множественное)
    person = django.forms.ChoiceField(label = 'Лицо', choices=persons, widget=django.forms.Select(attrs={'data-name':'person', 'class':'filter word'})) # лицо (1, 2, 3)
    tense = django.forms.ChoiceField( label = 'Время', choices=numbers, widget=django.forms.Select(attrs={'data-name':'tense', 'class':'filter word'})) # время (настоящее, прошедшее, будущее)
    transitivity = django.forms.ChoiceField(label = 'Переходность', choices = rules, widget=django.forms.Select(attrs={'data-name':'transitivity word', 'class':'filter word'})) # переходность (переходный, непереходный)
    voice = django.forms.ChoiceField( label = 'Залог', choices = voices, widget=django.forms.Select(attrs={'data-name':'voice', 'class':'filter word'}))# залог (действительный, страдательный)

