from django.test import TestCase, SimpleTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Project
from blog.templatetags.format_markdown import format_markdown


class ProjectDetailTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.project = Project.objects.create(
            author=self.user,
            title="Test Title 1",
            lead="Test Lead 1",
            body="Test Body 1",
            web_link="test-link.example.com",
            github_link="test-github-link.example.com",
            main_image="[Test Main Image](https://example.com)",
            meta_description="Test Meta 1",
            is_published="True",
        )
        self.url = reverse("project", kwargs={"slug": self.project.slug})
        self.response = self.client.get(self.url)

    def test_projectdetail(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "projects/project.html")

    def test_projectdetail_contains_links(self):
        self.assertContains(self.response, "test-link.example.com")
        self.assertContains(self.response, "test-github-link.example.com")

    def test_unpublished_projects_for_logged_out_user(self):
        unpublished_project = Project.objects.create(
            author=self.user,
            title="Test Title Unpublished",
            body="Test Body Unpublished",
            meta_description="Test Meta Unpublished",
            is_published="False",
        )
        self.url = reverse("project", kwargs={"slug": unpublished_project.slug})
        self.client.logout()
        self.response = self.client.get(self.url)
        self.assertContains(self.response, "Permission Denied")

    def test_unpublished_projects_for_logged_in_user(self):
        unpublished_project = Project.objects.create(
            author=self.user,
            title="Test Title Unpublished",
            body="Test Body Unpublished",
            meta_description="Test Meta Unpublished",
            is_published="False",
        )
        self.url = reverse("project", kwargs={"slug": unpublished_project.slug})
        self.client.login(username="testuser", password="testpass123")
        self.response = self.client.get(self.url)
        self.assertContains(self.response, "Test Title Unpublished")
        self.assertContains(self.response, "Test Body Unpublished")

    def test_contains_preloader(self):
        self.assertContains(self.response, '<div class="preloader" id="preloader">')


class ProjectCreateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.url = reverse("project_create")

    def test_projectcreate_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/admin/login/?next=/projects/new/")

    def test_projectcreate_for_logged_in_user(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/project_form.html")


class ProjectUpdateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")
        self.project = Project.objects.create(
            author=self.user,
            title="Test Title 1",
            body="Test Body 1",
            web_link="test-link.example.com",
            github_link="test-github-link.example.com",
            main_image="[Test Main Image](https://example.com)",
            meta_description="Test Meta 1",
            is_published="True",
        )
        self.url = reverse("project_update", kwargs={"slug": self.project.slug})

    def test_projectupdate_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"/admin/login/?next=/projects/edit/{self.project.slug}/"
        )

    def test_projectupdate_for_logged_in_user(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/project_form.html")


class ProjectDeleteTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")
        self.project = Project.objects.create(
            author=self.user,
            title="Test Title 1",
            body="Test Body 1",
            main_image="[Test Main Image](https://example.com)",
            meta_description="Test Meta 1",
            is_published="True",
        )
        self.url = reverse("project_delete", kwargs={"slug": self.project.slug})

    def test_projectdelete_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"/admin/login/?next=/projects/delete/{self.project.slug}/"
        )

    def test_projectdelete_for_logged_in_user(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/project_delete.html")
