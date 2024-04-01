from datetime import timedelta

from django import forms
from .models import Recipe, Category


class RecipeForm(forms.ModelForm):
    hours = forms.IntegerField(
        required=False, label='Часы', widget=forms.NumberInput(attrs={'min': 0, 'max': 23}))
    minutes = forms.IntegerField(
        required=False, label='Минуты', widget=forms.NumberInput(attrs={'min': 0, 'max': 59}))
    seconds = forms.IntegerField(
        required=False, label='Секунды', widget=forms.NumberInput(attrs={'min': 0, 'max': 59}))

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Категория',
        empty_label='Не выбрано',
    )

    def save(self, commit=True):
        recipe = super().save(commit=False)
        recipe.time = timedelta(
            hours=self.cleaned_data['hours'],
            minutes=self.cleaned_data['minutes'],
            seconds=self.cleaned_data['seconds'],
        )
        if commit:
            recipe.save()
        return recipe

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
