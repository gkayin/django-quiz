from django.forms import ModelForm
from .models import Levelup

class LevelupForm(ModelForm):
    class Meta:
        model = Levelup
        fields = ['title', 'memo', 'important']
