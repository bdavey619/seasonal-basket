#!/usr/bin/env python3
"""
Seasonal build script.
Reads structured content from src/content/<edition>/ and generates
static HTML into docs/. Run with: python3 src/build.py

No third-party dependencies. Requires Python 3.8+.
"""

import html
import json
import os
import re
import shutil
import sys
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────

ROOT       = Path(__file__).parent.parent
SRC        = ROOT / "src"
CONTENT    = SRC / "content"
TEMPLATES  = SRC / "templates"
CSS_SRC    = SRC / "css"
SITE       = ROOT / "docs"
EDITIONS   = ROOT / "editions"

# ── Helpers ────────────────────────────────────────────────────────────────────

def e(text):
    """Escape plain text for HTML insertion."""
    if text is None:
        return ""
    return html.escape(str(text), quote=True)

def safe_html(markup):
    """
    Pass-through for intentional HTML markup stored in content files.
    Call only when the value is authored markup, never for user-supplied input.
    """
    return str(markup) if markup is not None else ""

def read_json(path):
    """Load and parse a JSON file, with a clear error on failure."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        fail(f"Missing content file: {path}")
    except json.JSONDecodeError as exc:
        fail(f"JSON parse error in {path}: {exc}")

def illustration_slot(slug):
    """
    Return an empty, documented placeholder for a future botanical illustration.
    Renders nothing visible. The .illustration-slot container is display:none by default.
    To introduce an illustration later: place the artwork inside this element and
    set display:block in the edition CSS. No structural changes to templates required.
    """
    return (
        f'\n<!-- ILLUSTRATION SLOT: {slug} -->'
        f'\n<!-- When commissioned artwork is ready, place it inside the element below'
        f'\n     and set .illustration-slot {{ display: block }} in the edition CSS. -->'
        f'\n<div class="illustration-slot" aria-hidden="true"></div>'
    )

def read_template(name):
    path = TEMPLATES / name
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        fail(f"Missing template: {path}")

def write_page(path, content):
    """Write HTML to path, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  wrote {path.relative_to(ROOT)}")

def fail(msg):
    print(f"\n  ERROR: {msg}", file=sys.stderr)
    sys.exit(1)

def require_fields(data, fields, source):
    """Validate that required fields exist and are non-empty."""
    for field in fields:
        if not data.get(field):
            fail(f"Required field '{field}' missing or empty in {source}")

# ── Relative path calculator ───────────────────────────────────────────────────

def rel(depth, target):
    """
    Return a relative URL from a page at `depth` directories deep to `target`.
    depth=0 → site/index.html  → target is e.g. "css/base.css"
    depth=1 → site/july/index.html → "../css/base.css"
    """
    prefix = "../" * depth
    return prefix + target

# ── CSS builder ────────────────────────────────────────────────────────────────

def build_css(edition_slug):
    css_dir = SITE / "css"
    css_dir.mkdir(parents=True, exist_ok=True)
    for name in ["base.css", f"{edition_slug}.css"]:
        src = CSS_SRC / name
        dst = css_dir / name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  wrote css/{name}")
        else:
            fail(f"Missing CSS file: {src}")

# ── Guide helpers ──────────────────────────────────────────────────────────────

def find_guide(guides_list, guide_id):
    for g in guides_list:
        if g.get("id") == guide_id:
            return g
    return None

def render_guide_card(guide):
    if not guide:
        return ""
    return f"""
<div class="guide-card">
  <h3 class="guide-name">{e(guide['name'])}</h3>
  <span class="guide-role">{e(guide['role'])}</span>
  <p class="guide-philosophy">{e(guide['philosophy'])}</p>
</div>"""

def render_guide_quote(guide, ingredient_slug):
    if not guide:
        return ""
    quotes = guide.get("quotes", {})
    quote = quotes.get(ingredient_slug) or quotes.get("edition", "")
    if not quote:
        return ""
    return f"""
<div class="guide-quote-block">
  <!-- EDITORIAL NOTE: Guide characters are fictional editorial personalities.
       See src/content/july/guides.json for details. -->
  <blockquote>{e(quote)}</blockquote>
  <cite>— {e(guide['name'])}, {e(guide['role'])}</cite>
</div>"""

# ── Ingredient tile (basket + index pages) ─────────────────────────────────────

INGREDIENT_DISPLAY = {
    "heirloom-tomatoes":  ("Heirloom tomatoes", "Toast, bowls, pasta, weekend plate"),
    "persian-cucumbers":  ("Persian cucumbers", "Salads, rice bowls, wraps"),
    "peaches":            ("Peaches",            "Breakfast, snacks, salads, dessert"),
    "sweet-corn":         ("Sweet corn",         "Rice bowls, tacos, salads, sides"),
    "basil":              ("Basil",              "Tomatoes, chicken, pasta"),
    "mint":               ("Mint",               "Cucumbers, peaches, yogurt, drinks"),
    "cherries":           ("Cherries",           "Snacks, yogurt, drinks"),
    "blackberries":       ("Blackberries",       "Breakfast, dessert, salads"),
}

def render_basket_tiles(ingredients, ingredients_path, depth):
    tiles = []
    for slug in ingredients:
        name, note = INGREDIENT_DISPLAY.get(slug, (slug, ""))
        href = rel(depth, f"seasonal-basket/july-ingredients/{slug}/")
        tiles.append(f"""
    <a class="ingredient-tile" href="{href}">
      <strong>{e(name)}</strong>
      <span>{e(note)}</span>
    </a>""")
    return "\n".join(tiles)

# ── Field notes ────────────────────────────────────────────────────────────────

def render_field_notes(notes):
    items = []
    for note in notes:
        items.append(f"""
    <div class="field-note">
      <h3 class="field-note-name">{e(note['name'])}</h3>
      <p class="field-note-body">{e(note['body'])}</p>
    </div>""")
    return "\n".join(items)

# ── Meal transformations ───────────────────────────────────────────────────────

def render_transformations(transformations, meal_hrefs=None):
    if meal_hrefs is None:
        meal_hrefs = {}
    rows = []
    for t in transformations:
        meal_name = t['meal']
        href = meal_hrefs.get(meal_name)
        if href:
            meal_cell = f'<a href="{e(href)}">{e(meal_name)}</a>'
        else:
            meal_cell = e(meal_name)
        rows.append(f"""
    <div class="transformation-row">
      <span class="transformation-meal">{meal_cell}</span>
      <span class="transformation-arrow">→</span>
      <span class="transformation-change">{e(t['change'])}</span>
      <span class="transformation-result">{e(t['result'])}</span>
    </div>""")
    return "\n".join(rows)

# ── Week buckets ───────────────────────────────────────────────────────────────

def render_week(week):
    def meal_list(meals):
        items = []
        for m in meals:
            items.append(f"""
      <div class="week-meal">
        <span class="week-meal-name">{e(m['name'])}</span>
        <span class="week-meal-note">{e(m['note'])}</span>
      </div>""")
        return "\n".join(items)

    lunches = meal_list(week.get("weekday_lunches", []))
    dinners = meal_list(week.get("weekday_dinners", []))
    return f"""
  <div class="week-buckets">
    <div class="week-bucket">
      <div class="week-bucket-label">Weekday lunches</div>
      {lunches}
    </div>
    <div class="week-bucket">
      <div class="week-bucket-label">Weekday dinners</div>
      {dinners}
    </div>
  </div>"""

# ── Confidence score ───────────────────────────────────────────────────────────

def render_confidence(conf):
    score = conf.get("score", "")
    badges = [
        f'<span class="badge">{e(conf["lunches_supported"])} lunches</span>',
        f'<span class="badge">{e(conf["dinners_supported"])} dinners</span>',
        f'<span class="badge">{e(conf["weekend_meals_supported"])} weekend meals</span>',
        f'<span class="badge">Waste risk: {e(conf["waste_risk"])}</span>',
    ]
    editorial = conf.get("editorial_note", "")
    basket_cost = conf.get("basket_cost", {})
    cost_line = ""
    if basket_cost:
        cost_line = f'<p style="font-size:.85rem;color:var(--muted);margin-top:8px">Basket cost: <strong>{e(basket_cost["range"])}</strong> at {e(basket_cost["where"])}. {e(basket_cost["note"])}</p>'
    return f"""
<div class="section-label">Confidence score</div>
<div class="score-number">{e(score)}</div>
<p>With your usual rice, proteins, beans, sourdough, yogurt, and pantry basics, this basket comfortably supports:</p>
<div>{"".join(badges)}</div>
{cost_line}
<p class="score-note">{e(editorial)}</p>"""

# ── Staples list ───────────────────────────────────────────────────────────────

def render_staples(staples):
    items = "".join(f"<li>{e(s)}</li>" for s in staples)
    return f'<ul class="clean">{items}</ul>'

# ── Weekend meal ───────────────────────────────────────────────────────────────

def render_weekend(meal):
    ingredients = "".join(f"<li>{e(i)}</li>" for i in meal.get("ingredients", []))
    return f"""
<div class="two-col">
  <div>
    <strong>Use</strong>
    <ul>{ingredients}</ul>
  </div>
  <div>
    <strong>Do</strong>
    <p>{e(meal.get('method',''))}</p>
  </div>
</div>"""

# ── Drink ──────────────────────────────────────────────────────────────────────

def render_drink(drink):
    keep_items  = "".join(f"<li>{e(i)}</li>" for i in drink.get("keep", []))
    adds_items  = "".join(f"<li>{e(i)}</li>" for i in drink.get("july_adds", []))
    try_rows    = "".join(
        f"""<div class="drink-try-row">
          <span class="drink-try-change">{e(v['change'])}</span>
          <span class="drink-try-context">{e(v['context'])}</span>
        </div>"""
        for v in drink.get("try_another_way", [])
    )

    intro = f'<p class="drink-intro">{e(drink["intro"])}</p>' if drink.get("intro") else ""
    try_section = f"""
      <div class="drink-try">
        <div class="meal-adds-sublabel">Try another way</div>
        {try_rows}
      </div>""" if try_rows else ""

    return f"""
{intro}
<div class="drink-grid">
  <div class="drink-base">
    <div class="meal-adds-sublabel">Keep</div>
    <ul class="checklist">{keep_items}</ul>
    <div class="meal-adds-sublabel" style="margin-top:16px">July adds</div>
    <ul class="checklist">{adds_items}</ul>
    <div class="meal-adds-sublabel" style="margin-top:16px">Method</div>
    <p class="drink-method">{e(drink.get('method',''))}</p>
  </div>
  <div class="drink-variations">
    {try_section}
  </div>
</div>"""


def render_drink_link(drink):
    """Minimal drink reference for meal page sidebars — title only."""
    if not drink or not drink.get("name"):
        return ""
    return f"""
    <section>
      <h3>The drink</h3>
      <ul class="meal-field-notes-list">
        <li class="meal-field-note-title">{e(drink['name'])}</li>
      </ul>
    </section>"""

# ── House Flavor ───────────────────────────────────────────────────────────────

def render_house_flavor_uses(uses, depth):
    """Render the 'Use it this week' sequence on the dedicated page."""
    rows = []
    for u in uses:
        meal_slug = u.get("meal")
        label = e(u["label"])
        if meal_slug:
            href = rel(depth, f"july/meals/{meal_slug}/")
            label = f'<a href="{href}" class="house-flavor-meal-link">{label}</a>'
        rows.append(f"""
    <div class="house-flavor-use">
      <div class="house-flavor-use-header">
        <span class="house-flavor-use-label">{label}</span>
        <span class="house-flavor-use-action">{e(u['action'])}</span>
      </div>
      <p class="house-flavor-use-context">{e(u['context'])}</p>
    </div>""")
    return "\n".join(rows)


def render_house_flavor_card(flavor, depth):
    """Compact homepage section for the House Flavor."""
    if not flavor:
        return ""
    href = rel(depth, "july/house-flavor/")
    uses_html = "".join(f"<li>{e(u)}</li>" for u in flavor.get("card_uses", []))
    return f"""
      <article class="house-flavor-section col-12" aria-labelledby="house-flavor-heading">
        <div class="section-label">House Flavor</div>
        <h2 id="house-flavor-heading">{e(flavor['name'])}</h2>
        <p class="house-flavor-tagline">{e(flavor['intro'])}</p>
        <ul class="house-flavor-card-uses">{uses_html}</ul>
        <a href="{href}" class="house-flavor-cta">→ Make one jar</a>
      </article>"""


def render_house_flavor_link(flavor, depth):
    """Title-only sidebar reference for meal and ingredient pages."""
    if not flavor:
        return ""
    href = rel(depth, "july/house-flavor/")
    return f"""
    <section>
      <h3>House Flavor</h3>
      <ul class="meal-field-notes-list">
        <li class="meal-field-note-title">
          <a href="{href}" class="house-flavor-sidebar-link">{e(flavor['name'])}</a>
        </li>
      </ul>
    </section>"""


def build_house_flavor_page(flavor, edition, depth, canonical_url):
    """Build the dedicated House Flavor page."""
    slug = flavor["slug"]
    july_href = rel(depth, "july/")

    notes_by_slug = {n["slug"]: n for n in edition.get("field_notes", []) if "slug" in n}
    ingredients_html = "".join(f"<li>{e(i)}</li>" for i in flavor["ingredients"])
    uses_html = render_house_flavor_uses(flavor["uses"], depth)

    # Linked field notes (titles only)
    fn_items = []
    for fn_slug in flavor.get("linked_field_notes", []):
        note = notes_by_slug.get(fn_slug)
        if note:
            fn_items.append(f'<li class="meal-field-note-title">{e(note["name"])}</li>')
    field_notes_block = f"""
    <section>
      <h3>From Field Notes</h3>
      <ul class="meal-field-notes-list">{"".join(fn_items)}</ul>
    </section>""" if fn_items else ""

    # Linked ingredients
    ing_items = []
    for ing_slug in flavor.get("linked_ingredients", []):
        name = INGREDIENT_DISPLAY.get(ing_slug, (ing_slug,))[0]
        href = rel(depth, f"seasonal-basket/july-ingredients/{ing_slug}/")
        ing_items.append(f'<li class="meal-field-note-title"><a href="{href}" class="house-flavor-sidebar-link">{e(name)}</a></li>')
    ingredients_block = f"""
    <section>
      <h3>Made with</h3>
      <ul class="meal-field-notes-list">{"".join(ing_items)}</ul>
    </section>""" if ing_items else ""

    storage_note = flavor.get("storage", {}).get("note", "")
    storage_block = f'<p class="house-flavor-storage">{e(storage_note)}</p>' if storage_note else ""

    body = f"""
    <div style="padding-top:28px">
      <a href="{july_href}" class="back-link">← July</a>
    </div>

    <div class="meal-header">
      <div class="section-label">House Flavor · July</div>
      <h1>{e(flavor['name'])}</h1>
      <p class="dek" style="font-size:clamp(1rem,2vw,1.35rem);max-width:680px">{e(flavor['intro'])}</p>
    </div>

    <div class="meal-body">
      <div class="meal-main">
        <section aria-labelledby="make-heading">
          <h2 id="make-heading">Make one jar</h2>
          <ul class="checklist">{ingredients_html}</ul>
          <p class="house-flavor-method">{e(flavor['method'])}</p>
          {storage_block}
        </section>

        <section aria-labelledby="use-heading">
          <h2 id="use-heading">Use it this week</h2>
          <div class="house-flavor-uses">
            {uses_html}
          </div>
        </section>
      </div>

      <aside class="meal-sidebar">
        {ingredients_block}
        {field_notes_block}
      </aside>
    </div>"""

    return render_shell(
        title=f"Tomato Herb Vinaigrette — July — Seasonal",
        description=flavor["intro"],
        canonical_url=canonical_url,
        css_depth=depth,
        body=body,
        edition_slug="july",
        page_class="page--meal",
    )

# ── Guide cards row ────────────────────────────────────────────────────────────

def render_guides_section(guides_list):
    cards = "".join(render_guide_card(g) for g in guides_list)
    return f"""
<section class="guides" aria-label="This month's guides">
  <div class="section-label">This month's guides</div>
  <!-- EDITORIAL NOTE: Guide characters below are fictional editorial
       personalities created to test tone and voice. They are not real people.
       See src/content/july/guides.json. -->
  <div class="guides-grid">
    {cards}
  </div>
</section>"""

# ── Meal page renderers ────────────────────────────────────────────────────────

def render_meal_checklist(items):
    lis = "".join(f'<li>{e(item)}</li>' for item in items)
    return f'<ul class="checklist">{lis}</ul>'

def render_meal_variations(variations):
    rows = []
    for v in variations:
        rows.append(f"""
    <div class="meal-variation">
      <span class="meal-variation-ingredients">{e(v['ingredients'])}</span>
      <span class="meal-variation-context">{e(v['context'])}</span>
    </div>""")
    return "\n".join(rows)

def render_meal_linked_notes(linked_slugs, notes_by_slug):
    if not linked_slugs:
        return ""
    items = []
    for slug in linked_slugs:
        note = notes_by_slug.get(slug)
        if not note:
            continue
        items.append(f'<li class="meal-field-note-title">{e(note["name"])}</li>')
    if not items:
        return ""
    return f"""
    <section>
      <h3>From Field Notes</h3>
      <ul class="meal-field-notes-list">{"".join(items)}</ul>
    </section>"""


def render_meal_july_adds(meal):
    anchor = meal.get("july_anchor", [])
    options = meal.get("july_options", [])
    legacy = meal.get("july_adds", [])

    if anchor or options:
        anchor_items = "".join(f'<li>{e(item)}</li>' for item in anchor)
        options_items = "".join(f'<li>{e(item)}</li>' for item in options)
        anchor_block = f"""
      <div class="meal-adds-group">
        <div class="meal-adds-sublabel">Start with</div>
        <ul class="checklist">{anchor_items}</ul>
      </div>""" if anchor else ""
        options_block = f"""
      <div class="meal-adds-group">
        <div class="meal-adds-sublabel">Choose from</div>
        <ul class="checklist">{options_items}</ul>
      </div>""" if options else ""
        return anchor_block + options_block
    else:
        return render_meal_checklist(legacy)

# ── HTML shell ─────────────────────────────────────────────────────────────────

def render_shell(title, description, canonical_url, css_depth, body, edition_slug="july", page_class=None):
    if page_class is None:
        # Auto-detect narrow layout for single ingredient pages
        if 'ingredient' in title.lower() and 'ingredients' not in title.lower():
            page_class = "page--ingredient"
        else:
            page_class = ""
    extra_class = f" {page_class}" if page_class else ""

    base_css  = rel(css_depth, "css/base.css")
    month_css = rel(css_depth, f"css/{edition_slug}.css")
    home_href = rel(css_depth, "")
    july_href = rel(css_depth, "july/")
    basket_href = rel(css_depth, "seasonal-basket/july-ingredients/")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}" />
  <link rel="canonical" href="{e(canonical_url)}" />
  <!-- Social preview -->
  <meta property="og:title" content="{e(title)}" />
  <meta property="og:description" content="{e(description)}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{e(canonical_url)}" />
  <!-- Favicon placeholder: replace with actual favicon -->
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🌿</text></svg>" />
  <link rel="stylesheet" href="{base_css}" />
  <link rel="stylesheet" href="{month_css}" />
</head>
<body>
<a href="#main" class="skip-link" style="position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden;">Skip to content</a>
<div class="page{extra_class}">
  <header class="masthead">
    <a href="{home_href}" class="brand">Seasonal</a>
    <nav class="nav" aria-label="Primary navigation">
      <a href="{july_href}">July</a>
      <a href="{basket_href}">The Basket</a>
      <a href="{july_href}#week">The Week</a>
      <a href="{july_href}#weekend">The Weekend</a>
    </nav>
  </header>
  <main id="main">
{body}
  </main>
  <footer>
    <div>Seasonal · Know what now tastes like.</div>
    <div>San Diego · July · Edition 001</div>
  </footer>
</div>
</body>
</html>"""

# ── Edition page ───────────────────────────────────────────────────────────────

def build_edition_page(edition, depth, canonical_url, meal_hrefs=None, house_flavor=None):
    require_fields(edition, ["month", "opening_note", "week", "featured_ingredients",
                              "meal_transformations", "field_notes"], "edition.json")

    slug = edition["month"].lower()
    basket_href = rel(depth, "seasonal-basket/july-ingredients/")

    basket_tiles = render_basket_tiles(edition["featured_ingredients"],
                                       "seasonal-basket/july-ingredients", depth)

    body = f"""
    <section class="hero" aria-label="July edition">
      <div>
        <h1>{e(edition['month'])}</h1>
        <p class="dek">{e(edition['opening_note'])}</p>
      </div>
      <aside class="month-card" aria-label="This month tastes like">
        <div class="eyebrow">This month tastes like</div>
        <div class="big">Tomato<br>Cucumber<br>Peach</div>
        <div class="sub">Fresh, bright, and barely cooked.</div>
      </aside>
    </section>

    <div class="grid">
      <article class="card col-8" id="basket" aria-labelledby="basket-heading">
        <div class="section-label">The July basket</div>
        <h2 id="basket-heading">One trip. A full week of meals.</h2>
        <p>These are the ingredients worth organizing your week around. Repetition is intentional: the best produce should appear more than once.</p>
        <div class="basket-grid">
          {basket_tiles}
        </div>
        <p style="margin-top:18px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.88rem;color:var(--muted)">
          <a href="{basket_href}">View all July ingredients →</a>
        </p>
      </article>

      <aside class="card card--dark col-4" aria-label="Confidence score">
        {render_confidence(edition['confidence'])}
      </aside>

      <article class="card col-12" id="meals" aria-labelledby="transforms-heading">
        <div class="section-label">Keep the meal. Change the season.</div>
        <h2 id="transforms-heading">Your usual meals, wearing July.</h2>
        <p>The basket doesn't replace what you already make. It just makes those meals taste like right now.</p>
        <div class="transformations">
          {render_transformations(edition['meal_transformations'], meal_hrefs)}
        </div>
      </article>

      <article class="field-notes-section col-12" aria-labelledby="field-notes-heading">
        <div class="section-label">{e(edition.get('field_notes_label', 'Field Notes'))}</div>
        <div class="field-notes">
          {render_field_notes(edition['field_notes'])}
        </div>
      </article>

      {render_house_flavor_card(house_flavor, depth)}

      <article class="card col-12" id="week" aria-labelledby="week-heading">
        <div class="section-label">The week</div>
        <h2 id="week-heading">What a week actually looks like.</h2>
        <p>Mix and match. Repeat what works. One protein batch, one rice cook, and this basket will carry you.</p>
        {render_week(edition['week'])}
      </article>

      <article class="card col-7" id="weekend" aria-labelledby="weekend-heading">
        <div class="section-label">The weekend meal</div>
        <h2 id="weekend-heading">{e(edition['weekend_meal']['name'])}</h2>
        <p>{e(edition['weekend_meal']['intro'])}</p>
        {render_weekend(edition['weekend_meal'])}
      </article>

      <aside class="card card--cream col-5" aria-label="One thing to notice">
        <div class="section-label">One thing to notice</div>
        <h2>{e(edition['one_thing_to_notice']['headline'])}</h2>
        <p>{e(edition['one_thing_to_notice']['body'])}</p>
      </aside>

      <article class="card col-7" aria-labelledby="drink-heading">
        <div class="section-label">The drink</div>
        <h2 id="drink-heading">{e(edition['drink']['name'])}</h2>
        {render_drink(edition['drink'])}
      </article>


      <aside class="card card--warm col-5" aria-label="{e(edition['local_ritual']['label'])}">
        <div class="section-label">{e(edition['local_ritual']['label'])}</div>
        <h2>{e(edition['local_ritual']['name'])}</h2>
        <p>{e(edition['local_ritual']['description'])}</p>
      </aside>
    </div>

    <blockquote class="pull-quote">Keep the meal. Change the season.</blockquote>"""

    return render_shell(
        title=f"Seasonal — {edition['month']} in {edition['location']}",
        description=edition["opening_note"],
        canonical_url=canonical_url,
        css_depth=depth,
        body=body,
        edition_slug=slug,
    )

# ── Ingredient index page ──────────────────────────────────────────────────────

def build_ingredient_index(edition, ingredients_data, depth, canonical_url):
    tiles = []
    for slug in edition["featured_ingredients"]:
        ing = ingredients_data.get(slug, {})
        name = ing.get("name", slug)
        why  = ing.get("why_now", "")[:90] + ("…" if len(ing.get("why_now","")) > 90 else "")
        href = rel(depth, f"{slug}/")
        tiles.append(f"""
    <a class="ingredient-index-tile" href="{href}">
      {illustration_slot(slug)}
      <strong>{e(name)}</strong>
      <span class="why">{e(why)}</span>
    </a>""")

    body = f"""
    <div style="padding:40px 0 20px">
      <a href="{rel(depth, 'july/')}" class="back-link">← July</a>
      <div class="section-label" style="margin-top:8px">The seasonal basket</div>
      <h1 style="font-size:clamp(2.2rem,5vw,4rem);margin:8px 0 16px">July ingredients</h1>
      <p class="dek" style="font-size:clamp(1rem,2vw,1.35rem);max-width:600px">
        Eight ingredients worth organizing your week around. Each page explains why now, how to choose it, and what to do with it.
      </p>
    </div>
    <div class="ingredient-index-grid">
      {"".join(tiles)}
    </div>"""

    return render_shell(
        title="July Ingredients — Seasonal",
        description="Eight seasonal ingredients worth buying in July in San Diego.",
        canonical_url=canonical_url,
        css_depth=depth,
        body=body,
        edition_slug="july",
    )

# ── Individual ingredient page ─────────────────────────────────────────────────

def build_ingredient_page(ing, depth, canonical_url, house_flavor=None):
    require_fields(ing, ["slug", "name", "why_now", "how_to_choose", "buy_this_much",
                          "pairs_with_month", "pairs_with_staples",
                          "weekday_uses", "weekend_use", "storage",
                          "one_thing_to_learn"], f"{ing.get('slug')}.json")

    slug = ing["slug"]

    choose_items  = "".join(f'<li>{e(c)}</li>' for c in ing["how_to_choose"])
    weekday_items = "".join(f'<li>{e(u)}</li>' for u in ing["weekday_uses"])

    pairs_month  = ", ".join(e(INGREDIENT_DISPLAY.get(p, (p,))[0]) for p in ing["pairs_with_month"])
    pairs_staple = ", ".join(e(p) for p in ing["pairs_with_staples"])

    index_href = rel(depth, "seasonal-basket/july-ingredients/")

    body = f"""
    <div style="padding-top:28px">
      <a href="{index_href}" class="back-link">← July ingredients</a>
    </div>

    <div class="ingredient-header">
      {illustration_slot(slug)}
      <div class="section-label">July · San Diego</div>
      <h1>{e(ing['name'])}</h1>
      <p class="dek" style="font-size:clamp(1rem,2vw,1.45rem);max-width:680px">{e(ing['why_now'])}</p>
    </div>

    <div class="ingredient-body">
      <div class="ingredient-main">
        <section aria-labelledby="choose-heading">
          <h2 id="choose-heading">How to choose it</h2>
          <ul class="checklist">{choose_items}</ul>
          <p style="margin-top:12px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.9rem;color:var(--muted)">
            Buy this much: <strong>{e(ing['buy_this_much'])}</strong>
          </p>
          {f'<p style="margin-top:8px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.85rem;color:var(--muted)">{e(ing["price_note"])}</p>' if ing.get("price_note") else ""}
        </section>

        <section aria-labelledby="weekday-heading">
          <h2 id="weekday-heading">On a weekday</h2>
          <ul class="checklist">{weekday_items}</ul>
        </section>

        <section aria-labelledby="weekend-heading">
          <h2 id="weekend-heading">On a weekend</h2>
          <p>{e(ing['weekend_use'])}</p>
        </section>

        <section aria-labelledby="learn-heading">
          <h2 id="learn-heading">One thing worth learning</h2>
          <p>{e(ing['one_thing_to_learn'])}</p>
        </section>
      </div>

      <aside class="ingredient-sidebar">
        <section>
          <h3>Good with this month</h3>
          <p style="font-family:ui-sans-serif,system-ui,sans-serif;font-size:.9rem;color:var(--muted)">{pairs_month}</p>
        </section>
        <section>
          <h3>Good with your staples</h3>
          <p style="font-family:ui-sans-serif,system-ui,sans-serif;font-size:.9rem;color:var(--muted)">{pairs_staple}</p>
        </section>
        <section>
          <h3>Storage</h3>
          <p style="font-family:ui-sans-serif,system-ui,sans-serif;font-size:.9rem;color:var(--muted)">{e(ing['storage'])}</p>
        </section>
        {render_house_flavor_link(house_flavor, depth) if house_flavor and slug in (house_flavor.get('linked_ingredients') or []) else ""}
      </aside>
    </div>"""

    return render_shell(
        title=f"{ing['name']} — July — Seasonal",
        description=ing["why_now"],
        canonical_url=canonical_url,
        css_depth=depth,
        body=body,
        edition_slug="july",
    )

# ── Individual meal page ───────────────────────────────────────────────────────

def build_meal_page(meal, edition, depth, canonical_url, house_flavor=None):
    require_fields(meal, ["slug", "name", "intro", "keep",
                           "variations", "works_well_with", "finish"], f"{meal.get('slug')}.json")

    slug = meal["slug"]
    meals_back_href = rel(depth, "july/#meals")

    notes_by_slug = {n["slug"]: n for n in edition.get("field_notes", []) if "slug" in n}
    edition_drink = edition.get("drink", {})

    keep_items   = render_meal_checklist(meal["keep"])
    adds_section = render_meal_july_adds(meal)
    variations   = render_meal_variations(meal["variations"])
    linked_notes = render_meal_linked_notes(meal.get("linked_field_notes", []), notes_by_slug)

    linked_drink_slug = meal.get("linked_drink")
    drink_link = render_drink_link(edition_drink) if linked_drink_slug and linked_drink_slug == edition_drink.get("slug") else ""

    linked_hf_slug = meal.get("linked_house_flavor")
    flavor_link = render_house_flavor_link(house_flavor, depth) if linked_hf_slug and house_flavor and linked_hf_slug == house_flavor.get("slug") else ""

    works_well = "".join(f'<li>{e(w)}</li>' for w in meal["works_well_with"])

    body = f"""
    <div style="padding-top:28px">
      <a href="{meals_back_href}" class="back-link">← Your usual meals</a>
    </div>

    <div class="meal-header">
      <div class="section-label">July · weekday</div>
      <h1>{e(meal.get('display_name', meal['name']))}</h1>
      <p class="dek" style="font-size:clamp(1rem,2vw,1.35rem);max-width:680px">{e(meal['intro'])}</p>
    </div>

    <div class="meal-body">
      <div class="meal-main">
        <section aria-labelledby="keep-heading">
          <h2 id="keep-heading">Keep</h2>
          {keep_items}
        </section>

        <section aria-labelledby="july-adds-heading">
          <h2 id="july-adds-heading">July adds</h2>
          {adds_section}
        </section>

        <section aria-labelledby="variations-heading">
          <h2 id="variations-heading">Variations</h2>
          <div class="meal-variations">
            {variations}
          </div>
        </section>

        <section aria-labelledby="finish-heading">
          <h2 id="finish-heading">Finish</h2>
          <p style="font-family:ui-sans-serif,system-ui,sans-serif;font-size:.97rem;color:#3d4842;line-height:1.6">{e(meal['finish'])}</p>
        </section>
      </div>

      <aside class="meal-sidebar">
        <section>
          <h3>Works well with</h3>
          <ul class="checklist">{works_well}</ul>
        </section>
        {linked_notes}
        {flavor_link}
        {drink_link}
      </aside>
    </div>"""

    return render_shell(
        title=f"{meal.get('display_name', meal['name'])} — July — Seasonal",
        description=meal["intro"],
        canonical_url=canonical_url,
        css_depth=depth,
        body=body,
        edition_slug="july",
        page_class="page--meal",
    )

# ── Consolidated CONTENT.json snapshot ────────────────────────────────────────

def build_content_snapshot(edition, guides, ingredients_data):
    """
    Generate editions/july/CONTENT.json as a consolidated snapshot of all
    editorial content. This file is auto-generated — edit src/content/july/
    instead. Marked clearly at the top.
    """
    snapshot = {
        "_generated": "Auto-generated by src/build.py. Do not edit manually. Edit src/content/july/ instead.",
        **{k: v for k, v in edition.items() if not k.startswith("_")},
        "guides": [{k: v for k, v in g.items() if not k.startswith("_")}
                   for g in guides.get("guides", [])],
        "ingredients": {slug: {k: v for k, v in ing.items() if not k.startswith("_")}
                        for slug, ing in ingredients_data.items()},
    }
    out = EDITIONS / "july" / "CONTENT.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    print(f"  wrote editions/july/CONTENT.json (consolidated snapshot)")

# ── Verification ───────────────────────────────────────────────────────────────

EXPECTED_INGREDIENT_SLUGS = [
    "heirloom-tomatoes", "persian-cucumbers", "peaches", "sweet-corn",
    "basil", "mint", "cherries", "blackberries",
]

EXPECTED_MEAL_SLUGS = ["rice-bowl", "tacos", "pasta"]

def verify(edition_slug):
    errors = []
    expected_pages = [
        SITE / "index.html",
        SITE / f"{edition_slug}" / "index.html",
        SITE / "seasonal-basket" / "july-ingredients" / "index.html",
        SITE / "css" / "base.css",
        SITE / "css" / f"{edition_slug}.css",
    ]
    for slug in EXPECTED_INGREDIENT_SLUGS:
        expected_pages.append(
            SITE / "seasonal-basket" / "july-ingredients" / slug / "index.html"
        )
    for slug in EXPECTED_MEAL_SLUGS:
        expected_pages.append(
            SITE / f"{edition_slug}" / "meals" / slug / "index.html"
        )
    expected_pages.append(SITE / f"{edition_slug}" / "house-flavor" / "index.html")

    for p in expected_pages:
        if not p.exists():
            errors.append(f"Missing output: {p.relative_to(ROOT)}")

    # Check ingredient links appear in the basket index
    index_src = (SITE / "seasonal-basket" / "july-ingredients" / "index.html").read_text()
    for slug in EXPECTED_INGREDIENT_SLUGS:
        if f"{slug}/" not in index_src:
            errors.append(f"Ingredient link missing from basket index: {slug}")

    # Check meal links appear on the homepage
    home_src = (SITE / "index.html").read_text()
    for slug in EXPECTED_MEAL_SLUGS:
        if f"meals/{slug}/" not in home_src:
            errors.append(f"Meal link missing from homepage: {slug}")

    if errors:
        print("\n  VERIFICATION FAILED:")
        for err in errors:
            print(f"    ✗ {err}")
        sys.exit(1)
    else:
        print(f"\n  Verification passed. {len(expected_pages)} expected files confirmed.")

# ── Main ───────────────────────────────────────────────────────────────────────

def build_edition(edition_dir_name):
    edition_slug = edition_dir_name  # e.g. "july"
    content_dir  = CONTENT / edition_slug
    ing_dir      = content_dir / "ingredients"
    meals_dir    = content_dir / "meals"

    print(f"\nBuilding edition: {edition_slug}")

    # Load content
    edition = read_json(content_dir / "edition.json")
    guides  = read_json(content_dir / "guides.json")
    guides_list = guides.get("guides", [])

    base_url = edition.get("base_url", "").rstrip("/")

    ingredients_data = {}
    for slug in EXPECTED_INGREDIENT_SLUGS:
        ing = read_json(ing_dir / f"{slug}.json")
        ingredients_data[slug] = ing

    # Load meals (ordered)
    meals_data = {}
    for slug in EXPECTED_MEAL_SLUGS:
        meal_path = meals_dir / f"{slug}.json"
        if meal_path.exists():
            meals_data[slug] = read_json(meal_path)

    # Load house flavor
    hf_path = content_dir / "house-flavor.json"
    house_flavor = None
    if hf_path.exists():
        house_flavor = read_json(hf_path)
        # Derive linked_meals from non-null uses[].meal, validate against meals_data
        derived = [u["meal"] for u in house_flavor.get("uses", []) if u.get("meal")]
        for ms in derived:
            if ms not in meals_data:
                fail(f"house-flavor.json references meal '{ms}' which does not exist in meals_data")
        house_flavor["linked_meals"] = derived

    # CSS
    build_css(edition_slug)

    # Build meal href map for homepage linking (at depth 0 and depth 1)
    # We compute at depth=0; depth=1 version computed inline below
    def meal_hrefs_at(depth):
        return {
            meal['name']: rel(depth, f"july/meals/{slug}/")
            for slug, meal in meals_data.items()
        }

    # Edition pages (root + canonical /july/)
    july_canonical = f"{base_url}/july/"

    root_html = build_edition_page(edition, depth=0,
                                   canonical_url=july_canonical,
                                   meal_hrefs=meal_hrefs_at(0),
                                   house_flavor=house_flavor)
    write_page(SITE / "index.html", root_html)

    july_html = build_edition_page(edition, depth=1,
                                   canonical_url=july_canonical,
                                   meal_hrefs=meal_hrefs_at(1),
                                   house_flavor=house_flavor)
    write_page(SITE / "july" / "index.html", july_html)

    # Ingredient index
    ing_index_canonical = f"{base_url}/seasonal-basket/july-ingredients/"
    ing_index_html = build_ingredient_index(
        edition, ingredients_data,
        depth=2, canonical_url=ing_index_canonical
    )
    write_page(SITE / "seasonal-basket" / "july-ingredients" / "index.html", ing_index_html)

    # Individual ingredient pages
    for slug in EXPECTED_INGREDIENT_SLUGS:
        ing   = ingredients_data[slug]
        ing_canonical = f"{base_url}/seasonal-basket/july-ingredients/{slug}/"
        ing_html = build_ingredient_page(ing, depth=3,
                                         canonical_url=ing_canonical,
                                         house_flavor=house_flavor)
        write_page(
            SITE / "seasonal-basket" / "july-ingredients" / slug / "index.html",
            ing_html
        )

    # Individual meal pages (depth=3: docs/july/meals/<slug>/index.html)
    for slug, meal in meals_data.items():
        meal_canonical = f"{base_url}/july/meals/{slug}/"
        meal_html = build_meal_page(
            meal, edition,
            depth=3, canonical_url=meal_canonical,
            house_flavor=house_flavor
        )
        write_page(SITE / "july" / "meals" / slug / "index.html", meal_html)

    # House flavor page (depth=2: docs/july/house-flavor/index.html)
    if house_flavor:
        hf_canonical = f"{base_url}/july/house-flavor/"
        hf_html = build_house_flavor_page(house_flavor, edition,
                                          depth=2, canonical_url=hf_canonical)
        write_page(SITE / "july" / "house-flavor" / "index.html", hf_html)

    # Consolidated snapshot
    build_content_snapshot(edition, guides, ingredients_data)

    # Verify
    verify(edition_slug)


def main():
    print("Seasonal build")
    print("=" * 40)

    # Files in docs/ that must survive the clean step.
    PROTECTED = ["july-prototype.html"]

    rescued = {}
    if SITE.exists():
        for name in PROTECTED:
            p = SITE / name
            if p.exists():
                rescued[name] = p.read_bytes()
        shutil.rmtree(SITE)
    SITE.mkdir()

    for name, data in rescued.items():
        (SITE / name).write_bytes(data)

    # Build all editions found in src/content/
    edition_dirs = sorted(d.name for d in CONTENT.iterdir() if d.is_dir())
    if not edition_dirs:
        fail("No edition directories found in src/content/")

    for edition_dir in edition_dirs:
        build_edition(edition_dir)

    print("\nBuild complete.")
    print("Preview: python3 -m http.server --directory docs 8000")
    print("Then open: http://localhost:8000/")


if __name__ == "__main__":
    main()
