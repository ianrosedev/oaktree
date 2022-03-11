from django.core import mail
from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def setUp(self):
        url = reverse("home")
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, "pages/home.html")

    def test_contains_preloader(self):
        self.assertContains(self.response, '<div class="preloader" id="preloader">')


class ContactFormTests(TestCase):
    def setUp(self):
        self.url = reverse("contact")
        self.response = self.client.get(self.url)

    def test_contactpage(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "pages/contact.html")

    def test_contactpage_contains_form_inputs(self):
        self.assertContains(self.response, '<input type="text" name="name"')
        self.assertContains(self.response, '<input type="email" name="email"')
        self.assertContains(self.response, '<input type="text" name="subject"')
        self.assertContains(self.response, '<textarea name="message"')

    def test_contactpage_contains_preloader(self):
        self.assertContains(self.response, '<div class="preloader" id="preloader">')

    def test_send_email(self):
        mail.send_mail(
            subject="Test Subject",
            message="Test Message",
            from_email="test@example.com",
            recipient_list=["to@example.com"],
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Test Subject")
        self.assertEqual(mail.outbox[0].body, "Test Message")
        self.assertEqual(mail.outbox[0].from_email, "test@example.com")
        self.assertEqual(mail.outbox[0].to, ["to@example.com"])
