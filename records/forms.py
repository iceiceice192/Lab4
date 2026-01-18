from django import forms
from .models import Record

class RecordForm(forms.ModelForm):
    # Добавили required=False, чтобы при редактировании не требовало выбор хранилища
    storage = forms.ChoiceField(
        choices=[('db','БД'),('json','JSON'),('xml','XML')],
        required=False  # <--- ВОТ ЭТО ИСПРАВЛЕНИЕ
    )
    class Meta:
        model = Record
        fields = ['name', 'email', 'description']