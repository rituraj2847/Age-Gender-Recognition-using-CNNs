from django import forms

from .models import UploadedImage


class UserImage(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput, required=True)

    class Meta:
        model = UploadedImage
        fields = ['image']
