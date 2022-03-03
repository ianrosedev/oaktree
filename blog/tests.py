from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post


class PostListTests(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="testuser1", email="test1@example.com", password="testpass123"
        )
        self.user2 = get_user_model().objects.create_user(
            username="testuser2", email="test2@example.com", password="testpass123"
        )
        Post.objects.create(
            author=self.user1,
            title="Test Title 1",
            body="Test Body 1",
            meta_description="Test Meta 1",
            is_published="True",
        )
        Post.objects.create(
            author=self.user2,
            title="Test Title 2",
            body="Test Body 2",
            meta_description="Test Meta 2",
            is_published="True",
        )
        self.url = reverse("post_list")
        self.response = self.client.get(self.url)

    def test_postlist(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "blog/post_list.html")

    def test_postlist_content(self):
        self.assertContains(self.response, "Test Title 1")
        self.assertContains(self.response, "Test Title 2")
        self.assertContains(self.response, "Test Body 1")
        self.assertContains(self.response, "Test Body 2")

    def test_contains_preloader(self):
        self.assertContains(self.response, '<div class="preloader" id="preloader">')


class TagListTests(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="testuser1", email="test1@example.com", password="testpass123"
        )
        self.user2 = get_user_model().objects.create_user(
            username="testuser2", email="test2@example.com", password="testpass123"
        )
        self.post1 = Post.objects.create(
            author=self.user1,
            title="Test Title 1",
            body="Test Body 1",
            meta_description="Test Meta 1",
            is_published="True",
        )
        self.post2 = Post.objects.create(
            author=self.user2,
            title="Test Title 2",
            body="Test Body 2",
            meta_description="Test Meta 2",
            is_published="True",
        )

        # Must add tags after post creation
        self.post1.tags.add("Django")
        self.post2.tags.add("Django")

        self.url = reverse("tag_list", kwargs={"tag": "django"})
        self.response = self.client.get(self.url)

    def test_taglist(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "blog/post_list.html")

    def test_taglist_content(self):
        self.assertContains(self.response, "Test Title 1")
        self.assertContains(self.response, "Test Title 2")
        self.assertContains(self.response, "Test Body 1")
        self.assertContains(self.response, "Test Body 2")

    def test_taglist_content_heading(self):
        self.assertContains(self.response, "Django")

    def test_taglist_content_tags(self):
        self.assertContains(self.response, "DJANGO")

    def test_contains_preloader(self):
        self.assertContains(self.response, '<div class="preloader" id="preloader">')


class PostDetailTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.post = Post.objects.create(
            author=self.user,
            title="Test Title 1",
            body="Test Body 1",
            meta_description="Test Meta 1",
            is_published="True",
        )
        self.url = reverse("post", kwargs={"slug": self.post.slug})
        self.response = self.client.get(self.url)

    def test_postdetail(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "blog/post.html")

    def test_contains_preloader(self):
        self.assertContains(self.response, '<div class="preloader" id="preloader">')


class PostCreateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.url = reverse("post_create")

    def test_postcreate_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/admin/login/?next=/blog/new/")

    def test_postcreate_for_logged_in_user(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_form.html")


class PostUpdateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")
        self.post = Post.objects.create(
            author=self.user,
            title="Test Title 1",
            body="Test Body 1",
            meta_description="Test Meta 1",
            is_published="True",
        )
        self.url = reverse("post_update", kwargs={"slug": self.post.slug})

    def test_postupdate_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"/admin/login/?next=/blog/edit/{self.post.slug}/"
        )

    def test_postupdate_for_logged_in_user(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_form.html")


class PostDeleteTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")
        self.post = Post.objects.create(
            author=self.user,
            title="Test Title 1",
            body="Test Body 1",
            meta_description="Test Meta 1",
            is_published="True",
        )
        self.url = reverse("post_delete", kwargs={"slug": self.post.slug})

    def test_postdelete_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"/admin/login/?next=/blog/delete/{self.post.slug}/"
        )

    def test_postdelete_for_logged_in_user(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_delete.html")
