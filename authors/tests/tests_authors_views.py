from django.test import SimpleTestCase
from django.urls import reverse, resolve
from authors import views


class TestAuthorsViews(SimpleTestCase):
    def test_if_authors_register_url_loads_correct_view(self):
        '''Test if the register view is loaded correctly.'''
        response = resolve(reverse('authors:register'))
        self.assertEqual(response.func, views.register_view)

    def test_if_authors_create_url_loads_correct_view(self):
        '''Test if the create view is loaded correctly.'''
        response = resolve(reverse('authors:create'))
        self.assertEqual(response.func, views.register_create)

    def test_if_authors_register_view_loads_correct_template(self):
        '''Test if the register view loads the correct template.'''
        url = reverse('authors:register')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'authors/pages/register_view.html')

    def test_if_create_view_raises_404_if_not_post(self):
        '''Test if the create view raises 404 if not POST.'''
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
