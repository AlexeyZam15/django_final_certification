from datetime import timedelta

from django import forms
from .models import Recipe, Category, RecipeCategory


class RecipeForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Категория',
        empty_label='Не выбрано',
        blank=True,
        required=False,
    )

    class Meta:
        model = Recipe
        fields = Recipe.get_fields()
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'steps': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'image': 'Изображение',
            'steps': 'Шаги приготовления',
        }
