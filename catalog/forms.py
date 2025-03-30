from django.forms import ModelForm
from catalog.models import Product
from django.forms import BooleanField
from django.core.exceptions import ValidationError

bad_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = "form-check-input"
            else:
                fild.widget.attrs['class'] = "form-control"


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        errors = []

        for word in bad_words:
            if word.lower() in name:
                errors.append(f'Некорректное название товара: "{word}"')

        if errors:
            raise ValidationError(errors)

        return name

    def clean_description(self):
        description = self.cleaned_data['description'].lower()
        errors = []

        for word in bad_words:
            if word.lower() in description:
                errors.append(f'Некорректное слово в описании: "{word}"')

        if errors:
            raise ValidationError(errors)

        return description

    def clean_price(self):
        price = self.cleaned_data['price']

        if price <= 0:
            raise ValidationError('Цена за покупку не может быть отрицательной')

        return price
