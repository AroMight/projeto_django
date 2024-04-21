from unittest import TestCase
from django.urls import reverse


class AuthorsURLSTest(TestCase):
    def test_register_url_is_correct(self):
        '''Test if the URL for the register view is correct.'''
        url = reverse('authors:register')
        self.assertEqual(url, '/authors/register/')

    def test_create_url_is_correct(self):
        '''Test if the URL for the create view is correct.'''
        url = reverse('authors:register_create')
        self.assertEqual(url, '/authors/register/create/')
