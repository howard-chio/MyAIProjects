#!/usr/bin/env python3
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# Sitemap structure: top-level label -> (folder, [(label, filename, blurb), ...])
SITEMAP = {
    "Products": ("products", [
        ("Toothpaste Bits", "toothpaste-bits.html", "Plastic-free toothpaste tablets that fizz into a full clean."),
        ("Mouthwash Bits", "mouthwash-bits.html", "Concentrated mouthwash tablets — just drop, dissolve, swish."),
        ("Deodorant", "deodorant.html", "Aluminum-free deodorant that goes on smooth and lasts all day."),
        ("Body Wash", "body-wash.html", "Gentle, low-waste body wash for everyday use."),
        ("Lip Balm", "lip-balm.html", "Nourishing lip balm in fully recyclable packaging."),
        ("Starter Kits", "starter-kits.html", "Everything you need to make the switch to zero-waste bathroom care."),
    ]),
    "Subscriptions": ("subscriptions", [
        ("Monthly Subscription Plans", "monthly-plans.html", "Pick a plan and never run out of your bathroom essentials."),
        ("Manage My Subscription", "manage-subscription.html", "Pause, skip, swap, or update your delivery — anytime."),
    ]),
    "About Us": ("about", [
        ("Our Story", "our-story.html", "Why we started bITe and what we're working toward."),
        ("Our Team", "our-team.html", "Meet the people behind the bits."),
        ("Sustainability", "sustainability.html", "How we're cutting plastic waste out of daily routines."),
        ("Eco Ingredients", "eco-ingredients.html", "What goes into our products, and why."),
    ]),
    "Resources": ("resources", [
        ("Blog", "blog.html", "Tips, news, and stories from the bITe community."),
        ("FAQ", "faq.html", "Answers to the questions we hear most."),
        ("Reviews", "reviews.html", "See what customers are saying about bITe."),
    ]),
    "Community": ("community", [
        ("Refer a Friend", "refer-a-friend.html", "Share bITe and earn rewards together."),
        ("Quiz", "quiz.html", "Find the right products for your routine."),
    ]),
    "Account": ("account", [
        ("Log In / Create Account", "login.html", "Access your bITe account or create a new one."),
        ("Manage Subscription", "account-manage-subscription.html", "Update billing, shipping, and delivery preferences."),
    ]),
}

SITE_TITLE = "bITe"
SITE_TAGLINE = "Toothpaste Bits & Bathroom Essentials"


def nav_html(rel_prefix):
    """Build the main nav markup. rel_prefix is '' for root, '../' for subpages."""
    items = []
    for top_label, (folder, children) in SITEMAP.items():
        children_html = "\n".join(
            f'          <a href="{rel_prefix}{folder}/{fname}">{label}</a>'
            for label, fname, _ in children
        )
        items.append(f'''      <div class="nav-item">
        <span class="nav-top-label">{top_label}</span>
        <div class="dropdown">
{children_html}
        </div>
      </div>''')
    return "\n".join(items)


def page_shell(title, rel_prefix, body, breadcrumbs=""):
    nav = nav_html(rel_prefix)
    css = f"{rel_prefix}styles.css"
    js = f"{rel_prefix}nav.js"
    home = f"{rel_prefix}index.html"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | {SITE_TITLE}</title>
<link rel="stylesheet" href="{css}">
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a class="logo" href="{home}">{SITE_TITLE}</a>
    <nav class="main-nav">
{nav}
    </nav>
    <button class="mobile-toggle" aria-label="Toggle navigation">&#9776;</button>
  </div>
</header>
<main>
  {breadcrumbs}
  {body}
</main>
<footer class="site-footer">
  <p>&copy; 2026 {SITE_TITLE}. <a href="{home}">Back to home</a></p>
</footer>
<script src="{js}"></script>
</body>
</html>
"""


def write_page(path, content):
    full_path = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)


def build_homepage():
    sections = []
    for top_label, (folder, children) in SITEMAP.items():
        cards = "\n".join(
            f'      <a class="card-link" href="{folder}/{fname}">{label}</a>'
            for label, fname, _ in children
        )
        sections.append(f'''  <div class="section-block">
    <h2>{top_label}</h2>
    <div class="card-grid">
{cards}
    </div>
  </div>''')
    body = f"""<h1>{SITE_TITLE}</h1>
  <p class="subtitle">{SITE_TAGLINE}. Browse the full site map below.</p>
  {''.join(sections)}"""
    content = page_shell("Home", "", body)
    write_page("index.html", content)


def build_category_and_child_pages():
    for top_label, (folder, children) in SITEMAP.items():
        # Category landing page, e.g. products/index.html
        cards = "\n".join(
            f'    <a class="card-link" href="{fname}">{label}</a>'
            for label, fname, _ in children
        )
        breadcrumbs = f'<div class="breadcrumbs"><a href="../index.html">Home</a> / {top_label}</div>'
        body = f"""<h1>{top_label}</h1>
  <p class="subtitle">Explore everything under {top_label}.</p>
  <div class="card-grid">
{cards}
  </div>"""
        content = page_shell(top_label, "../", body, breadcrumbs)
        write_page(f"{folder}/index.html", content)

        # Each child page
        for label, fname, blurb in children:
            breadcrumbs = (
                f'<div class="breadcrumbs">'
                f'<a href="../index.html">Home</a> / '
                f'<a href="index.html">{top_label}</a> / {label}'
                f'</div>'
            )
            body = f"""<h1>{label}</h1>
  <p class="subtitle">{blurb}</p>
  <div class="placeholder-note">This is a placeholder page for "{label}". Replace this content with real copy, images, and details for this section.</div>"""
            content = page_shell(label, "../", body, breadcrumbs)
            write_page(f"{folder}/{fname}", content)


if __name__ == "__main__":
    build_homepage()
    build_category_and_child_pages()
    print("Site generated.")
