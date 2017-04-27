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

class TextFiltersForm(Form):

    main = 'MN'
    draft = 'DF'
    edition = 'ED'
    list = 'LS'
    none='none'
    version_types = ((none,''),(main, 'Основная редакция'), (draft, 'Черновик'), (edition, 'Редакция'), (list, 'Список'))
    status = django.forms.BooleanField(label='Опубликовано')
    live_status = django.forms.BooleanField(label='Опубликовано при жизни')
    date = django.forms.DateTimeField(label='Дата написания')
    genre = django.forms.CharField(label='Жанр')
    genus = django.forms.CharField(label='Род')
    measure = django.forms.CharField(label='Метр')
    redaction = django.forms.ChoiceField(label='Тип редакции', choices=version_types)
    collection = django.forms.ChoiceField(label='Коллекция')
    published = django.forms.DateTimeField(label='Добавлено')

class WordFiltersForm(Form):
    yes = 1
    no = 2
    unknown = 0
    nomn='NM'
    gent='GN'
    datv='DT'
    accs='AC'
    ablt='AL'
    loct='LC'
    NOUN='NOUN'
    ADJF='ADJF'
    COMP='COMP'
    VERB='VERB'
    PRTF='PRTF'
    GRND='GRND'
    NUMR='NUMR'
    ADVB='ADVB'
    NPRO='NPRO'
    PRED='PRED'
    PREP='PREP'
    CONJ='CONJ'
    PRCL='PRCL'
    INTJ='INTJ'
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
    grammem = django.forms.ChoiceField( label = 'Часть речи', choices = grams)
    animacy = django.forms.ChoiceField(label = 'Одушевленность', choices=rules)# одушевленность
    aspect = django.forms.ChoiceField(label = 'Совершенность', choices=rules)# вид: совершенный или несовершенный
    case = django.forms.ChoiceField( label = 'Падеж', choices = cases)# падеж
    gender = django.forms.ChoiceField( label = 'Род',choices=genders)# род (мужской, женский, средний)
    mood = django.forms.ChoiceField( label = 'Наклонение', choices=moods) # наклонение (повелительное, изъявительное)
    number = django.forms.ChoiceField( label = 'Число', choices=numbers) # число (единственное, множественное)
    person = django.forms.ChoiceField(label = 'Лицо', choices=persons) # лицо (1, 2, 3)
    tense = django.forms.ChoiceField( label = 'Время', choices=numbers) # время (настоящее, прошедшее, будущее)
    transitivity = django.forms.ChoiceField(label = 'Переходность', choices = rules) # переходность (переходный, непереходный)
    voice = django.forms.ChoiceField( label = 'Залог', choices = voices)# залог (действительный, страдательный)

