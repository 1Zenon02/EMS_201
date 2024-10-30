from django import forms
from .models import *



class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    birth_date = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'address', 'phone_number', 'birth_date']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Check if the two passwords match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn’t match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # Hash the password
        if commit:
            user.save()
        return user

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email', 'phone_number', 'address',
            'salary_rate'
        ]
        
class EmployeeForm(forms.ModelForm):
    birth_date = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}))
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'birth_date', 'role',
                  'salary_rate']
        widgets = {
            'role': forms.HiddenInput(attrs={'value': 'employee'})  # Set role to employee by default
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'})
        }
class SignInForm(forms.Form):
    pass

class SignOutForm(forms.Form):
    pass