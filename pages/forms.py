from django.conf import settings
from django import forms
from django.core.mail import send_mail


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "fs-0 border-700"})

    def send_email(self):
        message = f'FROM: {self.cleaned_data.get("email")}\n'
        message += f'SUBJECT: {self.cleaned_data.get("subject")}\n\n'
        message += self.cleaned_data.get("message")

        send_mail(
            subject=self.cleaned_data.get("subject"),
            message=message,
            from_email=self.cleaned_data.get("email"),
            recipient_list=[settings.EMAIL_RECIPIENT_ADDRESS],
        )
