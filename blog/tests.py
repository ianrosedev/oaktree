from django.test import TestCase, SimpleTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post
from .templatetags.format_markdown import format_markdown


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

    def test_posts_are_published(self):
        self.assertTrue(self.response.context["posts"][0].is_published)
        self.assertTrue(self.response.context["posts"][1].is_published)

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

    def test_posts_are_published(self):
        self.assertTrue(self.response.context["posts"][0].is_published)
        self.assertTrue(self.response.context["posts"][1].is_published)

    def test_contains_preloader(self):
        self.assertContains(self.response, '<div class="preloader" id="preloader">')


class SearchListTests(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="testuser1", email="test1@example.com", password="testpass123"
        )
        self.user2 = get_user_model().objects.create_user(
            username="testuser2", email="test2@example.com", password="testpass123"
        )

    def test_searchlist(self):
        url = reverse("search_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_list.html")

    def test_searchlist_content_empty_search(self):
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

        url = reverse("search_list")
        response = self.client.get(url, {"q": ""})
        self.assertContains(response, "Test Title 1")
        self.assertContains(response, "Test Title 2")
        self.assertContains(response, "Test Body 1")
        self.assertContains(response, "Test Body 2")

    def test_searchlist_content_title_search(self):
        Post.objects.create(
            author=self.user1,
            title="FINDME",
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

        search = "findme"
        url = reverse("search_list")
        response = self.client.get(url, {"q": search})
        self.assertContains(response, "FINDME")
        self.assertNotContains(response, "Test Title 2")
        self.assertContains(response, "Test Body 1")
        self.assertNotContains(response, "Test Body 2")

    def test_searchlist_content_tag_search(self):
        post1 = Post.objects.create(
            author=self.user1,
            title="Test Title 1",
            body="Test Body 1",
            meta_description="Test Meta 1",
            is_published="True",
        )
        post2 = Post.objects.create(
            author=self.user2,
            title="Test Title 2",
            body="Test Body 2",
            meta_description="Test Meta 2",
            is_published="True",
        )

        # Must add tags after post creation
        post1.tags.add("Django")
        post2.tags.add("Python")

        search = "django"
        url = reverse("search_list")
        response = self.client.get(url, {"q": search})
        self.assertContains(response, "Test Title 1")
        self.assertNotContains(response, "Test Title 2")
        self.assertContains(response, "Test Body 1")
        self.assertNotContains(response, "Test Body 2")

    def test_searchlist_content_no_results_search(self):
        post1 = Post.objects.create(
            author=self.user1,
            title="Test Title 1",
            body="Test Body 1",
            meta_description="Test Meta 1",
            is_published="True",
        )
        post2 = Post.objects.create(
            author=self.user2,
            title="Test Title 2",
            body="Test Body 2",
            meta_description="Test Meta 2",
            is_published="True",
        )

        # Must add tags after post creation
        post1.tags.add("Django")
        post2.tags.add("Python")

        search = "html"
        url = reverse("search_list")
        response = self.client.get(url, {"q": search})
        self.assertNotContains(response, "Test Title 1")
        self.assertNotContains(response, "Test Title 2")
        self.assertNotContains(response, "Test Body 1")
        self.assertNotContains(response, "Test Body 2")
        self.assertContains(response, f"No results found for: {search}")

    def test_posts_are_published(self):
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
        url = reverse("search_list")
        response = self.client.get(url, {"q": ""})
        self.assertTrue(response.context["posts"][0].is_published)
        self.assertTrue(response.context["posts"][1].is_published)


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

    def test_unpublished_posts_for_logged_out_user(self):
        unpublished_post = Post.objects.create(
            author=self.user,
            title="Test Title Unpublished",
            body="Test Body Unpublished",
            meta_description="Test Meta Unpublished",
            is_published="False",
        )
        self.url = reverse("post", kwargs={"slug": unpublished_post.slug})
        self.client.logout()
        self.response = self.client.get(self.url)
        self.assertContains(self.response, "Permission Denied")

    def test_unpublished_posts_for_logged_in_user(self):
        unpublished_post = Post.objects.create(
            author=self.user,
            title="Test Title Unpublished",
            body="Test Body Unpublished",
            meta_description="Test Meta Unpublished",
            is_published="False",
        )
        self.url = reverse("post", kwargs={"slug": unpublished_post.slug})
        self.client.login(username="testuser", password="testpass123")
        self.response = self.client.get(self.url)
        self.assertContains(self.response, "Test Title Unpublished")
        self.assertContains(self.response, "Test Body Unpublished")

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


class FormatMarkdownTests(SimpleTestCase):
    def test_markdown_is_changed_to_html(self):
        self.assertEquals(format_markdown("# Test String"), "<h1>Test String</h1>")
        self.assertEquals(
            format_markdown("*Test String*"), "<p><em>Test String</em></p>"
        )
