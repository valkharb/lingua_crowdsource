from django.forms import ModelForm
from .models import LitWork


class WorkForm(ModelForm):
    class Meta:
        model = LitWork
        fields = ('title', 'sub_title')