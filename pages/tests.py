from django.test import SimpleTestCase
from django.urls import reverse, resolve
from . import views


class HomePageTests(SimpleTestCase):
    def setUp(self):
        url = reverse("home")
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, "pages/home.html")

    def test_contains_preloader(self):
        self.assertContains(self.response, '<div class="preloader" id="preloader">')
