from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser
from .models import Post


class PostListTests(TestCase):
    def setUp(self):
        user1 = CustomUser.objects.create_user(
            username="Test User 1", email="test1@example.com", password="testpass123"
        )
        user2 = CustomUser.objects.create_user(
            username="Test User 2", email="test2@example.com", password="testpass123"
        )
        Post.objects.create(
            author=user1,
            title="Test Title 1",
            body="Test Body 1",
            meta_description="Test Meta 1",
            is_published="True",
        )
        Post.objects.create(
            author=user2,
            title="Test Title 2",
            body="Test Body 2",
            meta_description="Test Meta 2",
            is_published="True",
        )
        url = reverse("post_list")
        self.response = self.client.get(url)

    def test_postlist_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_postlist_template(self):
        self.assertTemplateUsed(self.response, "blog/post_list.html")

    def test_postlist_content(self):
        self.assertContains(self.response, "Test Title 1")
        self.assertContains(self.response, "Test Title 2")
        self.assertContains(self.response, "Test Body 1")
        self.assertContains(self.response, "Test Body 2")


class PostDetailTests(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(
            username="Test User", email="test@example.com", password="testpass123"
        )
        post = Post.objects.create(
            author=user,
            title="Test Title 1",
            body="Test Body 1",
            meta_description="Test Meta 1",
            is_published="True",
        )
        url = reverse("post", kwargs={"pk": post.id})
        self.response = self.client.get(url)

    def test_postdetail_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_postdetail_template(self):
        self.assertTemplateUsed(self.response, "blog/post.html")


class PostCreateTests(TestCase):
    def setUp(self):
        url = reverse("post_create")
        self.response = self.client.get(url)

    def test_postcreate_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_postcreate_template(self):
        self.assertTemplateUsed(self.response, "blog/post_form.html")


class PostUpdateTests(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(
            username="Test User", email="test@example.com", password="testpass123"
        )
        post = Post.objects.create(
            author=user,
            title="Test Title 1",
            body="Test Body 1",
            meta_description="Test Meta 1",
            is_published="True",
        )
        url = reverse("post_update", kwargs={"pk": post.id})
        self.response = self.client.get(url)

    def test_postupdate_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_postupdate_template(self):
        self.assertTemplateUsed(self.response, "blog/post_form.html")


class PostDeleteTests(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(
            username="Test User", email="test@example.com", password="testpass123"
        )
        post = Post.objects.create(
            author=user,
            title="Test Title 1",
            body="Test Body 1",
            meta_description="Test Meta 1",
            is_published="True",
        )
        url = reverse("post_delete", kwargs={"pk": post.id})
        self.response = self.client.get(url)

    def test_postdelete_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_postdelete_template(self):
        self.assertTemplateUsed(self.response, "blog/post_delete.html")
