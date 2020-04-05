from django import forms
from .models import Author, BookCreator


class AuthorForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput) # переопределили стандартный виджет

    def put_some_action(self):
        """Функции, какие-то обработчики формы."""
        pass

    class Meta:
        model = Author
        fields = '__all__'


class BookCreatorForm(forms.ModelForm):
    class Meta:
        model = BookCreator
        fields = '__all__'
