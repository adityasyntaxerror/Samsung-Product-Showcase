from decimal import Decimal

from django.core.management.base import BaseCommand

from Samsung_App.models import Category, Product, SiteImage

CATEGORIES = [
    ("phones", "Phones", "Galaxy smartphones and foldables."),
    ("wearables", "Wearables", "Smartwatches and health companions."),
    ("tv-av", "TV & AV", "Televisions, soundbars and home entertainment."),
    ("pc-tablets", "PC & Tablets", "Laptops and tablets for work and play."),
    ("appliances", "Appliances", "Smart Bespoke appliances for the home."),
]

# (slug, category slug, title, price, tagline, description, featured)
PRODUCTS = [
    ("galaxy-s25-ultra", "phones", "Galaxy S25 Ultra", "129999",
     "Galaxy AI. Built for the extraordinary.",
     "A premium titanium-framed flagship with an advanced camera, the brilliant Dynamic AMOLED display, and powerful Galaxy AI experiences.", True),
    ("galaxy-z-fold7", "phones", "Galaxy Z Fold7", "174999",
     "Thin. Powerful. Transformative.",
     "Unfold a cinematic screen and a laptop-like workspace in a remarkably slim foldable design made for multitasking.", True),
    ("galaxy-watch8", "wearables", "Galaxy Watch8", "29999",
     "Know your health. Own your day.",
     "Stay connected and informed with an elegant smartwatch, advanced wellness insights, fitness tracking, and all-day battery life.", True),
    ("neo-qled-8k", "tv-av", "Neo QLED 8K", "249999",
     "Every detail, elevated.",
     "Quantum Mini LEDs deliver intense contrast and detail in an immersive 8K display with intelligent upscaling.", False),
    ("galaxy-book4", "pc-tablets", "Galaxy Book4", "89990",
     "Power meets portability.",
     "A refined Windows laptop built for smooth productivity, vivid visuals, and seamless connection to the Galaxy ecosystem.", False),
    ("bespoke-washing-machine", "appliances", "Bespoke AI Washer", "54990",
     "Smarter laundry, beautifully done.",
     "Personalise your laundry experience with intelligent fabric care, efficient cleaning, and a refined Bespoke finish.", False),
]


class Command(BaseCommand):
    help = "Create the demo categories, products and empty image slots (safe to run repeatedly)."

    def handle(self, *args, **options):
        categories = {}
        for slug, name, description in CATEGORIES:
            categories[slug], _ = Category.objects.get_or_create(
                slug=slug, defaults={"name": name, "description": description}
            )

        for slug, category_slug, title, price, tagline, description, featured in PRODUCTS:
            Product.objects.get_or_create(slug=slug, defaults={
                "category": categories[category_slug],
                "title": title,
                "price": Decimal(price),
                "tagline": tagline,
                "description": description,
                "is_featured": featured,
            })

        for key, _label in SiteImage.SLOTS:
            SiteImage.objects.get_or_create(key=key)

        self.stdout.write(self.style.SUCCESS(
            f"Ready: {Category.objects.count()} categories, {Product.objects.count()} products, "
            f"{SiteImage.objects.count()} image slots. Add image URLs in /admin/."
        ))
