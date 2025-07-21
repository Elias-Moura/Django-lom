from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from collections import defaultdict

from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_erros = defaultdict(list)
        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'preparation_time',
                  'preparation_time_unit', 'servings', 'servings_unit',
                  'preparation_steps', 'cover')
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                ),
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                ),
            ),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        cleaned_data = self.cleaned_data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if title == description:
            self._my_erros['description'].append('Cannot be equal to title')
            self._my_erros['title'].append('Cannot be equal to description')

        if self._my_erros:
            raise forms.ValidationError(self._my_erros)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            self._my_erros['title'].append('Must have at least 5 chars.')

        return title

    def check_field_is_a_positive_number(self, field_name):
        message = 'Must be a positive number'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_erros[field_name].append(message)

        return field_value

    def clean_preparation_time(self):
        return self.check_field_is_a_positive_number('preparation_time')

    def clean_servings(self):
        return self.check_field_is_a_positive_number('servings')
