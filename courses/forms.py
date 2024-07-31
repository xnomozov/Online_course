from django import forms

from courses.models import CourseComment


class CourseCommentForm(forms.ModelForm):
    class Meta:
        model = CourseComment
        fields = ['name', 'email', 'comment', 'rating']


class EmailForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    email_from = forms.EmailField()

