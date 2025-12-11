from django import forms
from .models import CustomUser


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'manager']  # full profile editable

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        # Employees can select managers
        if user.role == 'employee':
            self.fields['manager'].queryset = CustomUser.objects.filter(role='manager')
        else:
            # Managers can't set their own manager
            self.fields['manager'].disabled = True

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = CustomUser.objects.exclude(pk=self.instance.pk)
        if qs.filter(email=email).exists():
            raise forms.ValidationError("Email already in use.")
        return email