# Samsung Product Showcase

**Student:** _your name · roll number · section_

## Objective
A multi-page Django website that showcases Samsung Galaxy products, demonstrating URL routing, views, template inheritance, static files, database models and form handling with Django's built-in authentication.

## Website theme / reference
An e-commerce product showcase inspired by the layout of Samsung's Black Friday landing page. It is an **unofficial student project**; all text is my own and no Samsung images or logos are bundled.

## Pages
| Page | URL | Notes |
|---|---|---|
| Home | `/` | Hero banner, promo tiles, trending products, bundles, FAQ |
| Products | `/products/` | Grid, category filter chips, search (`?category=phones`, `?q=watch`) |
| Product details | `/products/<slug>/` | Opened from any product card; "You may also like" links |
| About | `/about/` | Brand story and contact link |
| Log in | `/login/` | Username **or** email + password |
| Sign up | `/signup/` | Name, username, email, password + confirm |
| Admin | `/admin/` | Manage products and image URLs |

## Navigation flow
- Home → product card → Product details → related product / category / Products
- Header (every page): logo → Home · Products · Phones · TV & AV · About · Log in · Sign up
- Log in ⇄ Sign up (each links to the other) and both link back to Home
- Footer (every page): Home · Products · About · Contact

## Images are loaded dynamically
No image files live in `static/`. Every image comes from a URL stored in the database:
`Product.image_url` for products and `SiteImage` slots (logo, hero, promo tiles, bundles, About banner).
Space for every image is always reserved with a placeholder; paste a URL in `/admin/` and the image loads into that space (if the URL fails, the placeholder stays).

## Forms and authentication
Django's built-in `User`, `authenticate`, `login`, `logout` and password validators are used, so passwords are hashed (PBKDF2). Forms use POST with `{% csrf_token %}`; required fields, matching passwords, valid email, unique username/email and password strength are validated **on the server**, with success/error messages. Log out is a POST form.

## Technologies
Python 3, Django 6, SQLite, HTML5, CSS3 (responsive), a little vanilla JavaScript (mobile menu).

## Project structure
```
Samsung_Product_Showcase/
├── manage.py
├── Samsung_Product_Showcase/     # settings.py, urls.py
└── Samsung_App/
    ├── models.py  views.py  urls.py  admin.py  tests.py  context_processors.py
    ├── management/commands/seed_products.py
    ├── migrations/
    ├── templates/Samsung_App/    # base, navbar, home, products, product_detail, about, login, signup, partials/media.html
    └── static/Samsung_App/       # css/styles.css, js/script.js
```

## How to run
```bash
pip install django
python manage.py migrate
python manage.py seed_products        # demo categories, products, empty image slots
python manage.py createsuperuser      # optional, for /admin/
python manage.py runserver
```
Open http://127.0.0.1:8000/ . Run the tests with `python manage.py test` (includes a crawler that follows every link from Home).

## Screenshots
_Add screenshots of Home, Products, Product details, About, Log in and Sign up here._

## Known limitations / future improvements
- No cart or checkout; "Buy now" opens the product page.
- Product images must be added by URL in the admin (no uploads).
- Contact is a `mailto:` link, not a form.
- Add password reset, user profile and wishlist.
