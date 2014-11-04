from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.contrib.admin import widgets 



class RegistrationForm(UserCreationForm):
    """
    edit the User Registration form to add an emailfield
    """

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        #add custom errormessages
        self.fields['username'].error_messages = {'invalid': 'Invalid username'}
    
    #make sure username is lowered and unique
    def clean_username(self):
        username = self.cleaned_data.get('username')
        username = username.capitalize()
        try:
            User.objects.get(username=username)
            raise forms.ValidationError("This username is already in use.")
        except User.DoesNotExist:
            pass
            
        return username


    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'This email address is already in use.')
        return email
    
    
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user
    


class LoginForm(forms.Form):
    """create login form with placeholders for fields"""

    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Username:', "class": "login_input"}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password:', "class": "login_input"}))
    
    def clean(self):
        username = self.cleaned_data.get('username')
        username = username.capitalize()
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Login invalid")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        username = username.capitalize()
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user



