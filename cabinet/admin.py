from django.contrib import admin
from .models import Author
from .models import PublishingHouse
from .models import Collection
from .models import LitWork

admin.site.register(Author)
admin.site.register(PublishingHouse)
admin.site.register(Collection)
admin.site.register(LitWork)

# Register your models here.
