from django import forms
from ..model.models import UploadedImage, Document

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ('image',)

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'content')