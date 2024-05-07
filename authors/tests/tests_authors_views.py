from django.test import SimpleTestCase
from django.urls import reverse, resolve
from authors import views


class TestAuthorsViews(SimpleTestCase):
    def test_if_authors_register_url_loads_correct_view(self):
        '''Test if the register view is loaded correctly.'''
        response = resolve(reverse('authors:register'))
        self.assertEqual(response.func.view_class, views.RegisterView)

    def test_if_authors_register_view_loads_correct_template(self):
        '''Test if the register view loads the correct template.'''
        url = reverse('authors:register')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'authors/pages/register_view.html')
