from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.apps import apps
apps.get_app_config('admin').verbose_name = 'Главная панель'
# from pytz import timezone
# Create your models here.
#     let's use existing django-model now
# class User(models.Model) :

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

class LitWork(models.Model):
    verbose_name = u'Литературные произведения'

    owner = models.ForeignKey('auth.User', verbose_name = _(u'Владелец'))
    # author = models.ForeignKey('Author')    this field is described in 'author_work'
    # main information
    title = models.CharField(null=False, blank=False, max_length=100, verbose_name = _(u'Заголовок'))
    sub_title = models.CharField(null=True, blank=True, max_length=100, verbose_name = _(u'Подзаголовок'))
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

class Author_Work(models.Model):
    author = models.ForeignKey('Author')
    work = models.ForeignKey('LitWork')

class Parent_Draft(models.Model):
    main_version = models.ForeignKey('LitWork',related_name='main_version')
    child_version = models.ForeignKey('LitWork',related_name='child_version')