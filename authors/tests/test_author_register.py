from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User

class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username','Your username'),
        ('email','Your e-mail'),
        ('first_name','Ex.: John'),
        ('last_name','Ex.: Doe'),
        ('password','Type your password'),
        ('password2','Repeat your password'),

    ])
    def test_first_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        
        self.assertEqual(
            placeholder,
            current_placeholder
        )
        
    
    @parameterized.expand([
        ('username', (
            'Username must have letters, numbers or one of those @.+-_ '
            'The lenght should b between 4 and 150 characters.'
            )),
        ('email', 'The e-mail must be valid.'),
        ('password',(
            'Password must have at least one uppercase letter,'
            'one lowercase letter and one number.'
            'The length should be at least 8 characters.'
        )),
    ])
    def test_first_fields_helptext(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        
        self.assertEqual(
            current,
            needed
        )

    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('email', 'E-mail'),
        ('password', 'Password'),
    ])
    def test_first_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        
        self.assertEqual(
            current,
            needed
        )
        
        
class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@test.com',
            'password': 'Strong123@password!',
            'password2': 'Strong123@password!',
        }
        return super().setUp(*args, **kwargs)
    
    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please, repeat your password'),
        ('email', 'E-mail is required'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))
        
    
    def test_username_fiels_min_lenght_should_be_3(self):
        self.form_data['username'] = 'jo'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'Username must have at least 3 characters'
        # self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))
    
    
    def test_username_fiels_max_lenght_should_be_150(self):
        self.form_data['username'] = 'jo' * 200
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'Username must have less than 150 characters'
        # self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))
        
    
    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123' * 100
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = (
            'Password must have at least one uppercase letter,'
            'one lowercase letter and one number.'
            'The length should be at least 8 characters.'
        )
        # self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))
        
    
    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc1235'
        
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'Password and password2 must be equal'
        
        self.assertIn(msg, response.context['form'].errors.get('password'))        
        self.assertIn(msg, response.content.decode('utf-8'))
    
    
    def test_send_get_request_to_registration_create_view_returns_404(self):        
        url = reverse('authors:register_create')
        response = self.client.get(url, data=self.form_data, follow=True)
        
        self.assertEqual(response.status_code, 404)
    
    
    def test_register_view_render_a_form(self):
        url = reverse('authors:register')
        response = self.client.get(url, data=self.form_data, follow=True)
        
        self.assertIsInstance(
            response.context['form'],  RegisterForm
        )
    
    
    def test_register_create_valid_form(self):
        url = reverse('authors:register_create')

        response = self.client.post(url, data=self.form_data, follow=True)

        # 1. Testar se o usuário foi criado
        self.assertTrue(
            User.objects.filter(username='user').exists()
        )

        # 2. Testar se a mensagem de sucesso foi exibida
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Your user is created, please log in.', [m.message for m in messages])

        # 3. Testar se a chave 'register_form_data' foi removida da sessão
        self.assertNotIn('register_form_data', self.client.session)
        
    
    def test_email_field_must_be_unique(self):
        url = reverse('authors:register_create')
        
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'User e-mail is already in use'
        
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))
        
    
    def test_author_created_can_login(self):
        url = reverse('authors:register_create')
        
        self.form_data.update({
            'username': 'testUser',
            'password': '@Bc123456',
            'password2': '@Bc123456',
        })
        
        self.client.post(url, data=self.form_data, follow=True)
        
        is_authenticated = self.client.login(
            username='testUser',
            password='@Bc123456'
        )
        
        self.assertTrue(is_authenticated, True)