# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-10 10:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('second_name', models.CharField(max_length=50, verbose_name='Отчество')),
                ('birth_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата рождения')),
                ('death_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата смерти')),
                ('country', models.CharField(max_length=80, verbose_name='Страна')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата изменения')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
        ),
        migrations.CreateModel(
            name='Author_Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabinet.Author', verbose_name='Автор')),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Коллекция')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата последнего обновления')),
                ('is_open', models.BooleanField(default=False, verbose_name='Доступность')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
        ),
        migrations.CreateModel(
            name='LitWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('sub_title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Подзаголовок')),
                ('file', models.FileField(null=True, upload_to='', verbose_name='Текст работы')),
                ('wrote_date', models.CharField(blank=True, max_length=50, verbose_name='Дата написания')),
                ('wrote_date_type', models.BooleanField(default=True, verbose_name='Дата точная/восстановленная')),
                ('wrote_date_source', models.CharField(blank=True, max_length=150, null=True, verbose_name='Кем восстановлено?')),
                ('is_published', models.BooleanField(default=False, verbose_name='Опубликовано?')),
                ('is_published_alive', models.BooleanField(default=False, verbose_name='Опубликовано при жизни автора?')),
                ('publish_title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Наименование сборника')),
                ('publish_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации')),
                ('publish_pages', models.CharField(blank=True, max_length=20, null=True, verbose_name='Страницы')),
                ('archive_title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Архив')),
                ('is_main_version', models.BooleanField(default=False, verbose_name='Основная редакция?')),
                ('version_type', models.CharField(choices=[('DF', 'Черновик'), ('ED', 'Редакция'), ('LS', 'Список')], default='DF', max_length=50, verbose_name='Тип редакции')),
                ('work_status', models.CharField(choices=[('PB', 'Опубликовано'), ('UPB', 'Не опубликовано'), ('LCK', 'Защищено авторским правом')], default='PB', max_length=50, verbose_name='Авторское право')),
                ('is_editable', models.BooleanField(default=False, verbose_name='Доступен для редактирования?')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('published_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации в кабинете')),
                ('updated_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата изменения')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabinet.Author', verbose_name='Основной автор')),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cabinet.Collection', verbose_name='Коллекция')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
        ),
        migrations.CreateModel(
            name='Marks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object', models.IntegerField(verbose_name='Объект')),
                ('object_type', models.CharField(max_length=100, verbose_name='Тип объекта')),
                ('field', models.CharField(choices=[('N', '')], max_length=100, verbose_name='Поле')),
                ('value', models.CharField(max_length=100, verbose_name='Значение')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
        ),
        migrations.CreateModel(
            name='MarkUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100, verbose_name='Слово')),
                ('grammem', models.CharField(max_length=100, verbose_name='Часть речи')),
                ('animacy', models.CharField(max_length=100, verbose_name='Одушевленность')),
                ('aspect', models.CharField(max_length=100, verbose_name='Вид')),
                ('case', models.CharField(max_length=100, verbose_name='Падеж')),
                ('gender', models.CharField(max_length=100, verbose_name='Род')),
                ('involvement', models.CharField(max_length=100, verbose_name='Говорящий')),
                ('mood', models.CharField(max_length=100, verbose_name='Наклонение')),
                ('number', models.CharField(max_length=100, verbose_name='Число')),
                ('person', models.CharField(max_length=100, verbose_name='Лицо')),
                ('tense', models.CharField(max_length=100, verbose_name='Время')),
                ('transitivity', models.CharField(max_length=100, verbose_name='Переходность')),
                ('voice', models.CharField(max_length=100, verbose_name='Залог')),
                ('count', models.IntegerField(verbose_name='Встречается в тексте')),
            ],
        ),
        migrations.CreateModel(
            name='Paragraph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=3000, null=True, verbose_name='Абзац')),
                ('lit_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabinet.LitWork', verbose_name='Литературное произведение')),
            ],
        ),
        migrations.CreateModel(
            name='Parent_Draft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_version_id', models.IntegerField(verbose_name='Идентификатор')),
                ('main_version_title', models.CharField(max_length=500, verbose_name='Заголовок')),
            ],
        ),
        migrations.CreateModel(
            name='PublishingHouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Издательство')),
                ('country', models.CharField(max_length=80, verbose_name='Страна')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата изменения')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=1500, verbose_name='Параметры')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата изменения')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=500, null=True, verbose_name='Предложение')),
                ('paragraph', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabinet.Paragraph', verbose_name='Абзац')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('CS', 'Пользовательский'), ('LG', 'Лингвистический'), ('LB', 'Словарный'), ('PS', 'Стиховедческий'), ('NL', 'Нарратологический')], default='LG', max_length=50, verbose_name='Категория')),
                ('content', models.CharField(max_length=50, verbose_name='Описание')),
                ('author_type', models.CharField(choices=[('ur', 'Пользовательский'), ('ss', 'Системный')], default='ss', max_length=50, verbose_name='Авторство')),
                ('el_type', models.CharField(max_length=50, verbose_name='Тип объекта')),
                ('el_id', models.IntegerField(verbose_name='Объект')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата изменения')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=500, null=True, verbose_name='Предложение')),
                ('Sentence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabinet.Sentence', verbose_name='Предложение')),
                ('mark_up', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='cabinet.MarkUp', verbose_name='Вероятный разбор')),
            ],
        ),
        migrations.AddField(
            model_name='markup',
            name='sentence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabinet.Sentence', verbose_name='Предложение'),
        ),
        migrations.AddField(
            model_name='litwork',
            name='parent_version',
            field=models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.CASCADE, to='cabinet.Parent_Draft', verbose_name='Основная редакция'),
        ),
        migrations.AddField(
            model_name='litwork',
            name='publisher_title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabinet.PublishingHouse', verbose_name='Издательство'),
        ),
        migrations.AddField(
            model_name='author_work',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabinet.LitWork', verbose_name='Произведение'),
        ),
    ]
