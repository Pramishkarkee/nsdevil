from django import forms
from django.contrib.auth.forms import AuthenticationForm
from apps.attendance.models import AcademicClass
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter a valid Username',
                'id': 'form3Example3'
            }
        ),
        label='Username',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter your password',
                'id': 'form3Example4'
            }
        ),
        label='Password',
    )


class FilterForm(forms.Form):
    # Choices for the month/week selection
    TIME_CHOICES = [
        ('this_month', 'This Month'),
        ('week', 'Week'),
    ]

    time_period = forms.ChoiceField(
        choices=TIME_CHOICES,
        initial='this_month',
        label=None,
        widget=forms.Select(attrs={'class': 'form-select', 'aria-label': 'Default select example'}),
        required=False
    )

    # Choices for the academic classes, populated dynamically
    academic_class = forms.ModelChoiceField(
        queryset=AcademicClass.objects.all(),
        empty_label='All Class',
        label=None,
        widget=forms.Select(attrs={'class': 'form-select', 'aria-label': 'Default select example'}),
        required=False

    )