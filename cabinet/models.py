import re
import pymysql
import math
import pymorphy2
from tqdm import tqdm
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.apps import apps
db= pymysql.connect(host='localhost', user='val', passwd='1111', db='diploma_project' , charset='utf8')
apps.get_app_config('admin').verbose_name = 'Главная панель'
import codecs

# from pytz import timezone
# Create your models here.
#     let's use existing django-model now
# class User(models.Model) :

class Paragraph(models.Model):
    verbose_name = u'Абзацы'
    value = models.CharField(verbose_name = _(u'Абзац'), max_length=3000, null=True)
    lit_work = models.ForeignKey('LitWork', verbose_name=_(u'Литературное произведение'))

    def parse_sentences(self, morph):
        cur = db.cursor()
        cur.execute("SET NAMES utf8mb4;")  # or utf8 or any other charset you want to handle
        cur.execute("SET CHARACTER SET utf8mb4;")  # same as above
        cur.execute("SET character_set_connection=utf8mb4;")  # same as above
        sentences = re.split('\n|\.\.\. |\! |\? |\. ', self.value)
        for s in sentences:
            with db:
                cur.execute('INSERT INTO cabinet_sentence (value, paragraph_id) values( "' +s+'", '+str(self.id)+ ')')
                # new_s = Paragraph.objects.create(value=s,paragraph_id=self.id)
            Sentence.objects.latest('id').parse_words(morph)
        return self

class Sentence(models.Model):
    verbose_name = u'Предложения'
    value = models.CharField(verbose_name=_(u'Предложение'), max_length=500, null=True)
    paragraph = models.ForeignKey(Paragraph, verbose_name=_(u'Абзац'))

    def parse_words(self, morph):
        cur = db.cursor()
        cur.execute("SET NAMES utf8mb4;")  # or utf8 or any other charset you want to handle
        cur.execute("SET CHARACTER SET utf8mb4;")  # same as above
        cur.execute("SET character_set_connection=utf8mb4;")  # same as above
        words = re.findall(r"[\w']+", str.lower(self.value))
        POSes = {'NOUN', 'VERB', 'ADJF', 'PRTF', 'GRND', 'NPRO', 'COMP', 'PRTS', 'INTJ', 'PRCL', 'ADJS', 'NUMR',
                 'ADVB'}
        # take infinitives
        normal_words = []
        for nw in words[:-1]:
            parsed = morph.parse(nw)
            # Берем только значимые части речи. Так как вариантов анализа очень много, просто берем самый вероятный.
            for p in parsed:
                normal_words.append(parsed[0].normal_form)
                MarkUp.objects.create(word=nw,
                                      grammem=str(p.tag.POS),
                                      animacy=str(p.tag.animacy),
                                      aspect=str(p.tag.aspect),
                                      case=str(p.tag.case),
                                      involvement=str(p.tag.involvement),
                                      mood=str(p.tag.mood),
                                      number=str(p.tag.number),
                                      person=str(p.tag.person),
                                      tense=str(p.tag.tense),
                                      transitivity=str(p.tag.transitivity),
                                      voice=str(p.tag.voice),
                                      count=0,
                                      sentence_id=self.id)
        # create the dictionary
        normals = set(normal_words)
        dictionary = {w: 0 for w in normals}

        for w in dictionary:
            parsed = morph.parse(w)
            if parsed[0].normal_form in normal_words:
                dictionary[parsed[0].normal_form] += 1
        for w in words:
            for key in dictionary:
                if morph.parse(w)[0].normal_form == key:
                    with db:
                        cur.execute('UPDATE cabinet_markup SET count = ' + str(
                            dictionary[key]) + ' WHERE word = "' + w + '" and sentence_id = ' + str(self.id))
        frequent = {w: dictionary[w] for w in dictionary.keys() if dictionary[w] > 1}
        return self


class Author(models.Model):
    verbose_name = u'Авторы'
    last_name = models.CharField(max_length=50, verbose_name = _(u'Фамилия'))
    first_name = models.CharField(max_length=50, verbose_name = _(u'Имя'))
    second_name = models.CharField(max_length=50, verbose_name = _(u'Отчество'))
    birth_date = models.DateTimeField(blank = True, null = True, verbose_name = _(u'Дата рождения'))
    death_date = models.DateTimeField(blank=True, null=True, verbose_name = _(u'Дата смерти'))
    country = models.CharField(max_length=80, verbose_name = _(u'Страна'))
#     could be drop_down_list

class PublishingHouse(models.Model):
    verbose_name = u'Издательства'
    title = models.CharField(max_length=80, verbose_name = _(u'Издательство'))
    country = models.CharField(max_length=80, verbose_name = _(u'Страна'))
#     what else?

class Collection(models.Model):
    verbose_name = u'Коллекции'
    title = models.CharField(max_length=200, verbose_name = _(u'Коллекция'))
    owner = models.ForeignKey('auth.User', verbose_name = _(u'Владелец'))
    created_date = models.DateTimeField(
        default=timezone.now, verbose_name = _(u'Дата создания'))
    updated_date = models.DateTimeField(
        blank = True, null=True, verbose_name = _(u'Дата последнего обновления'))
    is_open = models.BooleanField(default = False, verbose_name = _(u'Доступность'))

class MarkUp(models.Model):
    word = models.CharField( blank=False, max_length=100, verbose_name = _(u'Слово'))
    grammem = models.CharField( blank=False, max_length=100, verbose_name = _(u'Часть речи'))
    animacy = models.CharField(blank=False, max_length=100, verbose_name = _(u'Одушевленность'))# одушевленность
    aspect = models.CharField( blank=False, max_length=100, verbose_name = _(u'Вид'))# вид: совершенный или несовершенный
    case = models.CharField( blank=False, max_length=100, verbose_name = _(u'Падеж'))# падеж
    gender = models.CharField( blank=False, max_length=100, verbose_name = _(u'Род'))# род (мужской, женский, средний)
    involvement = models.CharField( blank=False, max_length=100, verbose_name = _(u'Говорящий')) # включенность говорящего в действие
    mood = models.CharField( blank=False, max_length=100, verbose_name = _(u'Наклонение')) # наклонение (повелительное, изъявительное)
    number = models.CharField( blank=False, max_length=100, verbose_name = _(u'Число')) # число (единственное, множественное)
    person = models.CharField( blank=False, max_length=100, verbose_name = _(u'Лицо')) # лицо (1, 2, 3)
    tense = models.CharField( blank=False, max_length=100, verbose_name = _(u'Время')) # время (настоящее, прошедшее, будущее)
    transitivity = models.CharField( blank=False, max_length=100, verbose_name = _(u'Переходность')) # переходность (переходный, непереходный)
    voice = models.CharField( blank=False, max_length=100, verbose_name = _(u'Залог'))# залог (действительный, страдательный)
    count = models.IntegerField( blank=False, verbose_name = _(u'Встречается в тексте'))
    sentence = models.ForeignKey('Sentence', verbose_name=_(u'Предложение'))

class LitWork(models.Model):
    verbose_name = u'Литературные произведения'

    owner = models.ForeignKey('auth.User', verbose_name = _(u'Владелец'))
    # author = models.ForeignKey('Author')    this field is described in 'author_work'
    # main information
    title = models.CharField(null=False, blank=False, max_length=100, verbose_name = _(u'Заголовок'))
    sub_title = models.CharField(null=True, blank=True, max_length=100, verbose_name = _(u'Подзаголовок'))
    file = models.FileField(null=True,blank=False, verbose_name = _(u'Текст работы'))

    # publish dates
    # Дата с учетом введения текста типа "Начало 1998"
    wrote_date = models.CharField(blank=True, null=False, max_length=50, verbose_name = _(u'Дата написания'))
    # Дата точная/восстановленная
    wrote_date_type = models.BooleanField(default=True, verbose_name = _(u'Дата точная/восстановленная'))
    # Если дата восстановлена, то кем?
    wrote_date_source = models.CharField(null=True, blank=True, max_length=150, verbose_name = _(u'Кем восстановлено?'))
    # Тут все по названию ясно
    is_published = models.BooleanField(default=False, verbose_name = _(u'Опубликовано?'))

    # Если опубликовано:
    # поля могут быть пустыми, тк надо учитывать, что текст может быть не опубликован
    #  при жизни автора или нет
    is_published_alive = models.BooleanField(default=False, verbose_name = _(u'Опубликовано при жизни автора?'))
    # кто опубликовал
    publish_title = models.CharField(null=True, blank=True, max_length=100, verbose_name = _(u'Наименование сборника'))
    publish_date = models.DateTimeField(null=True, blank=True, verbose_name = _(u'Дата публикации'))
    publisher_title = models.ForeignKey('PublishingHouse', verbose_name=_(u'Издательство'))
    # страницы одной строкой, т.к. по идее ячейка несет только информативный характер
    # в крайнем случае парсим как инт и через " - "
    publish_pages = models.CharField(null=True, blank=True, max_length=20, verbose_name = _(u'Страницы'))

    # если не опубликовано:

    # сведения об архиве
    archive_title = models.CharField(null=True, blank=True, max_length=100, verbose_name = _(u'Архив'))
    # etc

    # самое страшное - редакция - основная или нет
    main = 'MN'
    draft = 'DF'
    edition = 'ED'
    list = 'LS'
    is_main_version = models.BooleanField(default=False, verbose_name = _(u'Основная редакция?'))
    version_types = ((main,'Основная редакция'),(draft,'Черновик'),(edition,'Редакция'),(list,'Список'))
    version_type = models.CharField(null=False, blank=False,
                                    choices=version_types, default=main, max_length=50, verbose_name = _(u'Тип редакции'))
    # перенесено в отдельную таблицу.
    # parent_version = models.ForeignKey('LitWork')

    published = 'PB'
    unpublished ='UPB'
    locked = 'LCK'
    status_types = ((published,'Опубликовано'),(unpublished,'Не опубликовано'),(locked,'Защищено авторским правом'))
    work_status = models.CharField(null=False,blank=False,
                                   choices=status_types, default=published, max_length=50, verbose_name = _(u'Авторское право'))

    is_editable = models.BooleanField(default=False, verbose_name = _(u'Доступен для редактирования?'))
    collection = models.ForeignKey('Collection', blank=True, null=True, verbose_name = _(u'Коллекция'))

    created_date = models.DateTimeField(default=timezone.now, verbose_name = _(u'Дата создания'))
    published_date = models.DateTimeField(blank=True, null=True, verbose_name = _(u'Дата публикации в кабинете'))
    updated_date = models.DateTimeField(blank = True, null=True, verbose_name = _(u'Дата изменения'))

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def mark_up(self, morph):

        # take the text from attachment
        with open(self.file.path, 'r') as work:
            work.seek(0)
            data = work.read()
            work.close()
        # parse text by symbol characters and put it to the array
        # разбиваем тексты сначала на абзацы. Будем их сохранять в базе последовательно
        paragraphs = data.split('\n')
        for p in paragraphs:
            new_p = Paragraph.objects.create( value = p,
                                      lit_work_id = self.id )
            new_p.save()
            new_p.parse_sentences(morph)


        # TODO: ЗАКИДЫВАТЬ ЧИСЛО СЛОВ ПО ТЕКСТУ В БАЗУ
        return self

    def sentences(self):
        # take the text from attachment
        with open(self.file.path, 'r') as work:
            work.seek(0)
            work = codecs.open(self.file.path, "r", "utf_8_sig")
            data = work.read().replace('\n', '')
            work.close()
            data = data.replace('? ','.')
            data = data.replace('! ', '.')
            sentences = data.replace('... ', '.').split('.')
        return len(sentences)

    def analysis(self):
        # take the text from attachment
        with open(self.file.path, 'r') as work:
            work.seek(0)
            work = codecs.open(self.file.path, "r", "utf_8_sig")
            data = work.read()
            work.close()
            paragraphs = data.split('\n')
        return len(paragraphs)

    def concordance(self):
        # take the text from attachment
        with open(self.file.path, 'r') as work:
            work.seek(0)
            data = work.read().replace('\n', '')
            work.close()
        return data

class Author_Work(models.Model):
    author = models.ForeignKey('Author')
    work = models.ForeignKey('LitWork')

class Parent_Draft(models.Model):
    main_version = models.ForeignKey('LitWork',related_name='main_version')
    child_version = models.ForeignKey('LitWork',related_name='child_version')