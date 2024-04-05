from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError

from .models import Recipe, Category


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = Recipe.get_fields()
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'steps': forms.Textarea(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'image': 'Изображение',
            'steps': 'Шаги приготовления',
        }

        error_messages = {
            'time': {
                'invalid': 'Введите время в формате HH:MM:SS',
            },
        }

    categories = forms.ModelMultipleChoiceField(label='Категории',
                                                queryset=Category.objects.all(),
                                                widget=forms.CheckboxSelectMultiple,
                                                error_messages={
                                                    'required': 'Выберите как минимум одну категорию'})

    def clean_time(self):
        time = self.cleaned_data['time']
        if time >= timedelta(hours=24, minutes=0, seconds=0):
            raise ValidationError('Время приготовления не может быть больше 24 часов')
        return time
