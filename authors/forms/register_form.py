from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, add_attr, strong_password


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')
        add_attr(self.fields['username'], 'css', 'a-css-class')
    
    
    username = forms.CharField(
        label='Username',
        help_text=(
            'Username must have letters, numbers or one of those @.+-_ '
            'The lenght should b between 4 and 150 characters.'
            ),
        error_messages={
          'required': 'This field must not be empty',
          'min_length': 'Username must have at least 3 characters',
          'max_length': 'Username must have less than 150 characters'
        },
        min_length=3, max_length=150
    )
    
    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        required=True,
        label='First name',
    )
    
    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        required=True,
        label='Last name',
    )
    
    email = forms.EmailField(
        error_messages={'required': 'E-mail is required'},
        label='E-mail',
        help_text='The e-mail must be valid.',
    )
    
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter,'
            'one lowercase letter and one number.'
            'The length should be at least 8 characters.'
        ),
        validators=[
            strong_password
        ],
        label='Password'
    )

    
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Please, repeat your password'
        },
        help_text=(
            'Password must have at least one uppercase letter,'
            'one lowercase letter and one number.'
            'The length should be at least 8 characters.'
        ),
        validators=[
            strong_password
        ],
        label='Password2',
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]

        # exclude = ['first_name']

        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email',
            'password': 'Password',
        }

        error_messages = {
            'username': {
                'required': 'This field must not be empty',
            }
        }


    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': ValidationError(
                    'Password and password2 must be equal',
                    code='invalid'
                ),
                'password2': [
                    'Password and password2 must be equal'
                ],
            })
   

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()
        
        if exists:
            raise ValidationError('User e-mail is already in use', code='invalid')
        
        return email