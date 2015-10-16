from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate
    
from django.utils.safestring import mark_safe

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=75, required=True)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=100, required=True)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if not email or not password:
            return self.cleaned_data
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                pass
            else:
                user=None
        except User.DoesNotExist:
            user=None

        if user is None:
            self._errors["email"] = self.error_class(["Incorrect email/password!"])

        else:
            if not user.is_active:
                self._errors["email"] = self.error_class(["Inactive Account!"])

        #user = authenticate(email=email, password=password)
        return self.cleaned_data

class RegistrationForm(forms.Form):
    """
    forms used for registration.
    """
    register_email = forms.EmailField(label="register_email", max_length=60, required=True)
    register_password = forms.CharField(label="register_password", max_length=15, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="confirm_password", max_length=15, required=True,
                                       widget=forms.PasswordInput)
    # You can add a function to clean password (if any password restrictions)
    def clean_register_email(self):
        email = self.cleaned_data.get('register_email')
        try:
 
            user = User.objects.get(email=email)
            self._errors["register_email"] = self.error_class(["Account with this email id already exists!"])
        except Exception, e:
            pass
        return self.cleaned_data
            
    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('register_password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(("The two password fields didn't match."))
        return password2

