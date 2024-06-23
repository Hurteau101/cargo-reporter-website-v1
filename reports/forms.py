from django import forms
from django.core.validators import FileExtensionValidator
import magic
from .models import AWB

class UploaderForm(forms.Form):
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control-file',
                # 'accept': '.xlsx'
            }
        ),
        label=False,
        validators=[FileExtensionValidator(['xlsx'])]
    )

    def clean(self):
        cleaned_data = super().clean()
        uploaded_file = cleaned_data.get('file')

        if uploaded_file:
            mime = magic.Magic(mime=True)
            file_mime_type = mime.from_buffer(uploaded_file.read(1024))

            accept = ['application/zip']

            if file_mime_type not in accept:
                self.add_error('file', "Invalid File Type")

        return cleaned_data

class RemarkForm(forms.ModelForm):
    class Meta:
        model = AWB
        fields = ["remarks"]

    def __init__(self, *args, **kwargs):
        super(RemarkForm, self).__init__(*args, **kwargs)
        self.fields['remarks'].widget.attrs = {'class': 'form-control'}