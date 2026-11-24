import re
from urllib.parse import urldefrag, urlparse

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Product, SiteImage

STRONG_PASSWORD = "Galaxy-Tab-2026!"


class SiteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_products", verbosity=0)


class PageTests(SiteTestCase):
    def test_home_is_served_at_root(self):
        self.assertEqual(reverse("home"), "/")
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_content_pages_render_with_shared_header_and_footer(self):
        product = Product.objects.first()
        urls = [reverse("home"), reverse("products"), product.get_absolute_url(),
                reverse("about"), reverse("login"), reverse("signup")]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'class="site-header')
                self.assertContains(response, 'class="site-footer')
                self.assertContains(response, reverse("home"))

    def test_unknown_product_is_404(self):
        self.assertEqual(self.client.get("/products/does-not-exist/").status_code, 404)

    def test_products_filter_by_category_and_search(self):
        response = self.client.get(reverse("products"), {"category": "phones"})
        self.assertEqual({p.slug for p in response.context["items"]}, {"galaxy-s25-ultra", "galaxy-z-fold7"})
        response = self.client.get(reverse("products"), {"q": "watch"})
        self.assertEqual([p.slug for p in response.context["items"]], ["galaxy-watch8"])
        self.assertContains(self.client.get(reverse("products"), {"q": "zzz"}), "No products found")


class DynamicImageTests(SiteTestCase):
    def test_placeholder_space_is_reserved_when_no_image(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "image-placeholder")
        self.assertNotContains(response, "<img")

    def test_images_load_from_database_urls(self):
        Product.objects.filter(slug="galaxy-z-fold7").update(image_url="https://example.com/fold.jpg")
        SiteImage.objects.filter(key="hero").update(url="https://example.com/hero.jpg", alt="Hero")
        home = self.client.get(reverse("home"))
        self.assertContains(home, 'src="https://example.com/hero.jpg"')
        self.assertContains(self.client.get(reverse("product_detail", args=["galaxy-z-fold7"])),
                            'src="https://example.com/fold.jpg"')

    def test_no_static_image_files_are_referenced(self):
        for url in [reverse("home"), reverse("products"), reverse("about")]:
            html = self.client.get(url).content.decode()
            self.assertIsNone(re.search(r'src="[^"]*/static/[^"]*\.(png|jpe?g|gif|svg|webp)', html), url)


class AuthTests(SiteTestCase):
    signup_data = {"name": "Aayush", "username": "aayush", "email": "a@example.com",
                   "password": STRONG_PASSWORD, "confirm_password": STRONG_PASSWORD}

    def test_signup_creates_hashed_user_and_logs_in(self):
        response = self.client.post(reverse("signup"), self.signup_data, follow=True)
        self.assertRedirects(response, reverse("home"))
        user = User.objects.get(username="aayush")
        self.assertNotEqual(user.password, STRONG_PASSWORD)
        self.assertTrue(user.password.startswith(("pbkdf2_", "argon2", "bcrypt", "scrypt")))
        self.assertContains(response, "Hi, Aayush")

    def test_signup_rejects_empty_mismatch_duplicates_and_weak_passwords(self):
        cases = {
            "empty": ({**self.signup_data, "name": ""}, "complete every field"),
            "mismatch": ({**self.signup_data, "confirm_password": "different"}, "do not match"),
            "bad email": ({**self.signup_data, "email": "nope"}, "valid email"),
            "weak": ({**self.signup_data, "password": "12345678", "confirm_password": "12345678"}, "numeric"),
        }
        for label, (data, expected) in cases.items():
            with self.subTest(label):
                response = self.client.post(reverse("signup"), data)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, expected, html=False)
                self.assertFalse(User.objects.filter(username="aayush").exists())
        self.client.post(reverse("signup"), self.signup_data)
        self.client.post(reverse("logout"))
        dupe = self.client.post(reverse("signup"), {**self.signup_data, "email": "other@example.com"})
        self.assertContains(dupe, "already taken")

    def test_login_with_username_or_email_and_failure_message(self):
        User.objects.create_user("aayush", "a@example.com", STRONG_PASSWORD, first_name="Aayush")
        bad = self.client.post(reverse("login"), {"username": "aayush", "password": "wrong"})
        self.assertContains(bad, "Invalid username/email or password")
        empty = self.client.post(reverse("login"), {"username": "", "password": ""})
        self.assertContains(empty, "enter both")
        for identifier in ("aayush", "A@example.com"):
            with self.subTest(identifier):
                self.client.logout()
                response = self.client.post(reverse("login"), {"username": identifier, "password": STRONG_PASSWORD}, follow=True)
                self.assertRedirects(response, reverse("home"))
                self.assertContains(response, "Welcome back")

    def test_logout_requires_post(self):
        User.objects.create_user("aayush", password=STRONG_PASSWORD)
        self.client.login(username="aayush", password=STRONG_PASSWORD)
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.assertRedirects(self.client.post(reverse("logout")), reverse("home"))

    def test_forms_include_csrf_token_and_use_post(self):
        for name in ("login", "signup"):
            html = self.client.get(reverse(name)).content.decode()
            self.assertIn('method="post"', html)
            self.assertIn("csrfmiddlewaretoken", html)

    def test_login_and_signup_link_to_each_other_and_home(self):
        login = self.client.get(reverse("login"))
        signup = self.client.get(reverse("signup"))
        self.assertContains(login, f'href="{reverse("signup")}"')
        self.assertContains(login, f'href="{reverse("home")}"')
        self.assertContains(signup, f'href="{reverse("login")}"')
        self.assertContains(signup, f'href="{reverse("home")}"')


class NavigationTests(SiteTestCase):
    def test_every_internal_link_reachable_from_home_works(self):
        """Click through the whole site like a user: follow every <a href> from Home."""
        seen, queue = set(), ["/"]
        while queue:
            url = queue.pop()
            if url in seen:
                continue
            seen.add(url)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"broken link: {url}")
            html = response.content.decode()
            self.assertNotIn('href="#"', html, f"dead '#' link on {url}")
            for href in re.findall(r'<a [^>]*href="([^"]*)"', html):
                href, _ = urldefrag(href)
                parsed = urlparse(href)
                if not href or parsed.scheme in ("mailto", "http", "https"):
                    continue
                queue.append(href)
        self.assertTrue({"/", "/products/", "/about/", "/login/", "/signup/",
                         "/products/galaxy-z-fold7/"} <= seen)
