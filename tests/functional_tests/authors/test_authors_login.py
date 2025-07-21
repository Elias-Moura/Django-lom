import time
from django.urls import reverse
import pytest
from .base import AuthorsBaseTest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_sucessfully(self):
        string_password = 'P@ssw0rd10'
        user = User.objects.create_user(
            username='my_user', password=string_password)

        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuário vê o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Usuário digita seu usuário e senha
        self.get_by_placeholder(
            form, 'Type your username').send_keys(user.username)
        self.get_by_placeholder(
            form, 'Type your password').send_keys(string_password)

        # Usuário envia o formulário
        form.submit()

        # Usuário vê a mensagem de login com sucesso e seu nome
        self.assertIn(
            f'You are logged in with {user.username}',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url +
                         reverse('authors:login_create'))

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_is_invalid(self):
        # Usuário abre a página de login
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )
        
        # Usuário vê o formulário de login
        
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        
        # E tenta enviar espaço nos inputs
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        
        username.send_keys(' ')
        password.send_keys(' ')
        
        # Usuário envia o formulário
        
        form.submit()
        
        time.sleep(1)
        
        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )  
        
    def test_form_login_invalid_credentials(self):
        # Usuário abre a página de login
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )
        
        # Usuário vê o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        
        # E tenta enviar espaço nos inputs
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        
        username.send_keys('username')
        password.send_keys('password')
        
        # Usuário envia o formulário
        
        form.submit()
        
        self.assertIn(
            'Invalid credentials.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
