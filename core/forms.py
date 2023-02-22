from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': "Your Name"}))
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'placeholder': "Your Email"}))
    message = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'placeholder': "write us a message"}))