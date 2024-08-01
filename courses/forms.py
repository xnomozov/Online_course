from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_recaptcha.fields import ReCaptchaField

from courses.models import CourseComment, ContactMessage, User, Student


class CourseCommentForm(forms.ModelForm):
    class Meta:
        model = CourseComment
        fields = [ 'comment', 'rating']


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['username', 'email_from', 'message', 'subject']


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=100)

    def clean_email(self):
        email = self.data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email doesn't exist")
        return email

    def clean_password(self):
        password = self.data.get('password')
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise forms.ValidationError(" Password doesn't match")
        except User.DoesNotExist:
            raise forms.ValidationError("Email or Password doesn't match")
        return password


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    recaptcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['course', 'phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }
