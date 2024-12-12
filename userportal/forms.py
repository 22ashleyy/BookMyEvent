from django import forms

from userportal.models import Event


class eventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Title'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Event Date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Event Description'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control small-textarea', 'placeholder': 'Event Amount'}),
            'status': forms.Select(attrs={'class': 'form-control small-textarea', 'placeholder': 'Event Status'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Event Image'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Event Category'}),
        }

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)