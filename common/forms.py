from django import forms
from .models import UserProfile

class ProfileCreationForm(forms.ModelForm):
    class Meta:
        fields = ('age', )
        # fields = ['age']
        model = UserProfile