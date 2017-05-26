# lingua_crowdsource
# Установка и настройка 

С чего начать:

⦁	Установка python 3.4.3 - https://www.python.org/downloads/release/python-343/

На вкладке Customize ->  Add python.exe to the Path -> Will be installed on local hard drive

⦁	Установка Git - https://git-scm.com/book/ru/v1/%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5-%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-Git

⦁	запустить git bash , выполнить 
	git clone https://github.com/valkharb/lingua_crowdsource.git
  
⦁	Установка MySQL - https://dev.mysql.com/downloads/file/?id=470091 

// может затребовать .NET Framework 4.0 ( https://www.microsoft.com/ru-ru/download/confirmation.aspx?id=17718 )

Кроме того, при установке создать пользователя DBAdmin 
логин: val
пароль: 1111
если параметры будут иными , их необходимо изменить в файле конфигурации manage.py

Переходим в MySQL Command Line Client и создаем базу данных 
create database diploma_project;

⦁	Установить Visual C++ Express - https://www.microsoft.com/ru-ru/download/confirmation.aspx?id=44914

⦁	Перейти в свойства системы и создать новую Environment variable VS100COMNTOOLS = %VS120COMNTOOLS%

⦁	Установить lxml  - lxml-3.7.3.win32-py3.4.exe (md5) - https://pypi.python.org/pypi/lxml/3.7.3

⦁	Устанавливаем зависимости
	pip install django django-modeltranslation modeltranslation django-registration pymysql django-select2 pymorphy2 pynlpl
	
⦁	Мигрируем базу данных
	python manage.py makemigrations cabinet
	python manage.py migrate
  
⦁	запускаем сервер командой python manage.py runserver 0.0.0.0:8000
