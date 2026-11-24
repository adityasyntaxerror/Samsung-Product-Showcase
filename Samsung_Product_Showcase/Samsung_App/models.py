from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tagline = models.CharField(max_length=250)
    description = models.TextField()
    image_url = models.URLField(
        blank=True,
        help_text="Paste an image URL. Leave empty to show the reserved image placeholder.",
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.slug])

    @property
    def display_price(self):
        return f"₹{self.price:,.0f}"


class SiteImage(models.Model):
    """A named image slot on the site (logo, hero banner, promo tiles...).

    Templates look slots up by key, so nothing image-related is hard-coded in
    static files. An empty URL simply keeps the placeholder space on the page.
    """

    SLOTS = [
        ("logo", "Header logo"),
        ("hero", "Home — hero banner"),
        ("promo_rewards", "Home — rewards promo tile"),
        ("promo_tradein", "Home — trade-in promo tile"),
        ("upgrade_mobile", "Home — mobile upgrade card"),
        ("upgrade_wearable", "Home — wearable upgrade card"),
        ("bundle_phone", "Home — phone + buds bundle"),
        ("bundle_tv", "Home — TV + soundbar bundle"),
        ("about", "About page banner"),
    ]

    key = models.CharField(max_length=40, unique=True, choices=SLOTS)
    url = models.URLField(blank=True, help_text="Paste an image URL. Leave empty to keep the placeholder.")
    alt = models.CharField(max_length=150, blank=True, help_text="Short description for screen readers.")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.get_key_display()
