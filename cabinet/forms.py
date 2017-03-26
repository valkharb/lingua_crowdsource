from django.forms import ModelForm
from .models import LitWork


class WorkForm(ModelForm):
    class Meta:
        model = LitWork
        fields = ('title', 'sub_title', 'file','is_published','publish_title', 'publisher_title',
                  'publish_date','version_type','collection')
