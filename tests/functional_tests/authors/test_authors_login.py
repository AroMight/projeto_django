from .base import AuthorsBaseTest
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_sucessfully(self):
        user = User.objects.create_user(
            username='my_user', password='password')

        # usuario abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # usuario vê o formulario de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # usuario digita seu usuario e senha
        username_field.send_keys(user.username)
        password_field.send_keys('password')
        form.submit()

        # usuario vê a mensagem de sucesso
        self.assertIn(f'Your are logged in with {user.username}.',
                      self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url +
                         reverse('authors:login_create'))
        self.assertIn('Not Found', self.browser.find_element(
            By.TAG_NAME, 'body').text)

    def test_form_login_is_invalid(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        username_field.send_keys(' ')
        password_field.send_keys(' ')
        form.submit()

        self.assertIn('Invalid username or password',
                      self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_login_crendentials_is_invalid(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        username_field.send_keys('wrong_username')
        password_field.send_keys('wrong_password')
        form.submit()

        self.assertIn('Invalid credentials',
                      self.browser.find_element(By.TAG_NAME, 'body').text)
