from django import forms


class NoteForm(forms.Form):
    title = forms.CharField(label="title", max_length=128, widget=forms.TextInput())
    deadline_date = forms.DateTimeField(label="deadline_date")
    content = forms.CharField(label="content",  widget=forms.TextInput())

