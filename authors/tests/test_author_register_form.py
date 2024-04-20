from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse


class AuthorsRegisterFormUniTest(TestCase):
    @parameterized.expand([
        ('username', 'Your first name'),
        ('email', 'Your email'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex: Doe'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder_is_correct(self, field_name, field_placeholder):
        form = RegisterForm()
        placeholder = form.fields[field_name].widget.attrs.get('placeholder')
        self.assertEqual(placeholder, field_placeholder)

    @parameterized.expand([
        ('last_name', 'Please, submit your last name'),
        ('username', 'Between 3 and 150 characters. Must have letters, numbers and one of those: @/./+/-/_ only.'),
        ('email', 'Enter a valid email address.'),
        ('password', 'Password must have at least one uppercase letter, one lowercase letter and one number. The length should be at least 8 characters.'),
    ])
    def test_fields_help_texts_is_correct(self, field_name, field_help_text):
        form = RegisterForm()
        helptext = form.fields[field_name].help_text
        self.assertEqual(helptext, field_help_text)

    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('email', 'Email'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_fields_label_is_correct(self, field_name, field_label):
        form = RegisterForm()
        label = form.fields[field_name].label

        self.assertEqual(label, field_label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self) -> None:
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@any.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword2',
        }
        return super().setUp()

    @parameterized.expand([
        ('username', 'This field is required.'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty.'),
        ('password2', 'Please, repeat your password.'),
        ('email', 'Enter a valid email address.'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        '''Test if the fields cannot be empty.'''
        self.form_data[field] = ''

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        '''Test if the username field has at least 4 characters.'''
        self.form_data['username'] = 'us'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Username must have at least 4 characters.'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_150(self):
        '''Test if the username field has at most 150 characters.'''
        self.form_data['username'] = 'a' * 151

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Username must have at most 150 characters.'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        '''Test if the password field has at least one uppercase letter, one lowercase letter and one number.'''
        self.form_data['password'] = 'aa123'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Password must have at least one uppercase letter, one lowercase letter and one number. The length should be at least 8 characters.'

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_and_password_raises_error_if_not_equal(self):
        '''Test if the password field has at least one uppercase letter, one lowercase letter and one number.'''
        self.form_data['password'] = 'Abc12345678'
        self.form_data['password2'] = '12345678Abc'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Password and password2 must be equal'

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))
