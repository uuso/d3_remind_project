from django import forms

class UserInfoForm(forms.Form):
    city = forms.CharField(max_length=14, label="Город проживания", required=False)
    birth_city = forms.CharField(max_length=25, label="Родной город", required=False)
    about = forms.CharField(max_length=256, label="О себе", required=False, widget=forms.Textarea)
