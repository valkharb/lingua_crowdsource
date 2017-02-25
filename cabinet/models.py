from django.db import models
from django.utils import timezone
# from pytz import timezone
# Create your models here.
#     let's use existing django-model now
# class User(models.Model) :

class Author(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    birth_date = models.DateTimeField(blank = True, null = True)
    death_date = models.DateTimeField(blank=True, null=True)
    country = models.CharField(max_length=80)
#     could be drop_down_list

class PublishingHouse(models.Model):
    title = models.CharField(max_length=80)
    country = models.CharField(max_length=80)
#     what else?

class Collection(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey('auth.User')
    created_date = models.DateTimeField(
        default=timezone.now)
    updated_date = models.DateTimeField(
        blank = True, null=True)
    is_open = models.BooleanField(default = False)

class LitWork(models.Model):

    owner = models.ForeignKey('auth.User')
    # author = models.ForeignKey('Author')    this field is described in 'author_work'
    # main information
    title = models.CharField(null=False, blank=False, max_length=100)
    sub_title = models.CharField(null=True, blank=True, max_length=100)
    # publish dates
    # Дата с учетом введения текста типа "Начало 1998"
    wrote_date = models.CharField(blank=True, null=False, max_length=50)
    # Дата точная/восстановленная
    wrote_date_type = models.BooleanField(default=True)
    # Если дата восстановлена, то кем?
    wrote_date_source = models.CharField(null=True, blank=True, max_length=150)
    # Тут все по названию ясно
    is_published = models.BooleanField(default=False)

    # Если опубликовано:
    # поля могут быть пустыми, тк надо учитывать, что текст может быть не опубликован
    #  при жизни автора или нет
    is_published_alive = models.BooleanField(default=False)
    # кто опубликовал
    publish_title = models.CharField(null=True, blank=True, max_length=100)
    publish_date = models.DateTimeField(null=True, blank=True)
    publisher_title = models.CharField(null=True, blank=True, max_length=100)
    # страницы одной строкой, т.к. по идее ячейка несет только информативный характер
    # в крайнем случае парсим как инт и через " - "
    publish_pages = models.CharField(null=True, blank=True, max_length=20)

    # если не опубликовано:

    # сведения об архиве
    archive_title = models.CharField(null=True, blank=True, max_length=100)
    # etc

    # самое страшное - редакция - основная или нет
    main = 'MN'
    draft = 'DF'
    edition = 'ED'
    list = 'LS'
    is_main_version = models.BooleanField(default=False)
    version_types = ((main,'Основная редакция'),(draft,'Черновик'),(edition,'Редакция'),(list,'Список'))
    version_type = models.CharField(null=False, blank=False,
                                    choices=version_types, default=main, max_length=50)
    # перенесено в отдельную таблицу.
    # parent_version = models.ForeignKey('LitWork')

    published = 'PB'
    unpublished ='UPB'
    locked = 'LCK'
    status_types = ((published,'Опубликовано'),(unpublished,'Не опубликовано'),(locked,'Защищено авторским правом'))
    work_status = models.CharField(null=False,blank=False,
                                   choices=status_types, default=published, max_length=50)

    is_editable = models.BooleanField(default=False)
    collection = models.ForeignKey('Collection', blank=True, null=True)

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank = True, null=True)


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