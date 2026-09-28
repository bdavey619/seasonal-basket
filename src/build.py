#!/usr/bin/env python3
"""
Seasonal build script.
Reads structured content from src/content/<edition>/ and generates
static HTML into docs/. Run with: python3 src/build.py

No third-party dependencies. Requires Python 3.8+.
"""

import hashlib
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

# ── Publication status ─────────────────────────────────────────────────────────

# An edition marked "upcoming" is finished and committed, but not yet the one the
# publication leads with. Its pages are still built — so the link check covers
# them and the edition can be previewed at its own URL — but the homepage keeps
# showing the previous month as current, lists the upcoming month only under
# "Next edition", and the pages carry a noindex tag until the month arrives.
# To publish: set "status": "published" in that edition's edition.json and rebuild.

def is_published(edition):
    return edition.get("status", "published") != "upcoming"

# Set for the duration of each edition's build; read by render_shell so an
# unpublished edition's pages are not indexed while they are staged.
BUILDING_UNPUBLISHED = False

# Content hash per stylesheet, used to bust the browser cache on deploy.
# GitHub Pages serves css/*.css with max-age=600 and the filenames never
# change, so without this a CSS-only change is invisible to anyone who
# loaded the page recently.
CSS_VERSIONS = {}

def build_css(edition_slug):
    css_dir = SITE / "css"
    css_dir.mkdir(parents=True, exist_ok=True)
    for name in ["base.css", f"{edition_slug}.css"]:
        src = CSS_SRC / name
        dst = css_dir / name
        if not src.exists():
            fail(f"Missing CSS file: {src}")
        shutil.copy2(src, dst)
        CSS_VERSIONS[name] = hashlib.sha256(src.read_bytes()).hexdigest()[:8]
        print(f"  wrote css/{name} (v{CSS_VERSIONS[name]})")

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

def display_name(slug, ingredients_data=None):
    """
    Human-readable name for an ingredient slug.
    Reads the name from the edition's own ingredient content so nothing is
    hardcoded per month; falls back to a de-slugged label for anything the
    current edition doesn't carry a page for.
    """
    if ingredients_data and slug in ingredients_data:
        return ingredients_data[slug].get("name", slug)
    return slug.replace("-", " ").capitalize()

# ── Buying guidance and default moves ──────────────────────────────────────────

# The four things worth knowing at a market stall, in the order they matter.
# An ingredient or protein carries at most one, under the key "buy".
BUY_TAGS = {
    "buy-now":       "Buy now",          # short window; gone soon
    "for-the-week":  "Buy for the week", # perishable; buy what you'll cook
    "keeps-well":    "Keeps well",       # safe to buy extra
    "if-you-see-it": "If you see it",    # opportunistic; don't go looking
}

def render_buy_tag(key, source=""):
    if not key:
        return ""
    if key not in BUY_TAGS:
        fail(f"Unknown buy tag '{key}' in {source}. Use one of: {', '.join(BUY_TAGS)}")
    return f'<span class="buy-tag">{e(BUY_TAGS[key])}</span>'

def render_move_steps(steps):
    """A default move's steps as one line: Halve → seed → slice → roast."""
    return '<span class="move-arrow"> → </span>'.join(
        f'<span class="move-step">{e(s)}</span>' for s in steps)

def render_ref_list(refs, ingredients_data, depth, ing_index_path, sep=" · ", edition_href=""):
    """
    A list of things something pairs with. A basket ingredient slug becomes a
    link to its page; {"text", "anchor"} links to that section of the edition
    page; anything else (a pantry item) is plain text. This is how the edition
    draws relationships without explaining them.
    """
    base = ing_index_path.rstrip("/")
    out = []
    for r in refs:
        if isinstance(r, dict):
            out.append(f'<a href="{edition_href}#{e(r["anchor"])}">{e(r["text"])}</a>')
        elif ingredients_data and r in ingredients_data:
            href = rel(depth, f"{base}/{r}/")
            out.append(f'<a href="{href}">{e(display_name(r, ingredients_data))}</a>')
        else:
            out.append(e(r))
    return sep.join(out)

# ── Meal transformations ───────────────────────────────────────────────────────

def render_transformations(transformations, meal_hrefs=None, meals_by_name=None):
    """
    The meals section. Each transformation is the month's default version of a
    meal; the variations beneath it are the other ways to combine the basket for
    that same meal. Those were previously reachable only by opening the meal
    page, which put the edition's densest combination advice one click out of
    sight.
    """
    if meal_hrefs is None:
        meal_hrefs = {}
    meals_by_name = meals_by_name or {}
    rows = []
    for t in transformations:
        meal_name = t['meal']
        href = meal_hrefs.get(meal_name)
        if href:
            meal_cell = f'<a href="{e(href)}">{e(meal_name)}</a>'
        else:
            meal_cell = e(meal_name)

        variations = (meals_by_name.get(meal_name) or {}).get("variations", [])
        var_html = ""
        if variations:
            items = "".join(f"""
        <li class="meal-way">
          <span class="meal-way-combo">{e(v['ingredients'])}</span>
          <span class="meal-way-when">{e(v['context'])}</span>
        </li>""" for v in variations)
            more = f'<a class="meal-way-more" href="{e(href)}">All of it →</a>' if href else ""
            var_html = f"""
      <ul class="meal-ways">{items}
      </ul>
      {more}"""

        rows.append(f"""
    <div class="transformation-group">
      <div class="transformation-row">
        <span class="transformation-meal">{meal_cell}</span>
        <span class="transformation-arrow">→</span>
        <span class="transformation-change">{e(t['change'])}</span>
        <span class="transformation-result">{e(t['result'])}</span>
      </div>{var_html}
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

# ── Shopping card ──────────────────────────────────────────────────────────────

def render_bring_home(bring_home, ingredients_data, featured, depth, ing_index_path):
    """
    The basket: one row per ingredient carrying what it is, how much to buy, why,
    and what it's for — and linking to that ingredient's page. This is the only
    representation of the basket on the edition page; browsing lives on the
    ingredient index. Rows join to ingredient content by `slug`.
    """
    if not bring_home:
        return ""

    ingredients_data = ingredients_data or {}
    featured = set(featured or [])
    base = ing_index_path.rstrip("/")

    row_html = []
    for item in bring_home.get("items", []):
        slug = item.get("slug")
        if slug and featured and slug not in featured:
            fail(f"bring_home item '{item['name']}' has slug '{slug}', "
                 f"which is not in featured_ingredients")
        ing = ingredients_data.get(slug, {}) if slug else {}
        tag_html = render_buy_tag(ing.get("buy"), f"{slug}.json")
        move = ing.get("default_move")
        if move:
            # An ingredient with a default move shows it in place of the note
            # and uses: what to do with it is the thing to carry out of the store.
            detail_html = (f'<span class="bring-home-note bring-home-note--move">{e(move["headline"])}</span>\n'
                           f'          <span class="bring-home-uses bring-home-move">{render_move_steps(move["steps"])}</span>')
        else:
            uses = ing.get("tile_uses", "")
            detail_html = (f'<span class="bring-home-note">{e(item.get("note", ""))}</span>\n'
                           + (f'          <span class="bring-home-uses">{e(uses)}</span>' if uses else ""))
        name_html = (f'<span class="bring-home-name bring-home-name--tagged">'
                     f'<span class="bring-home-label">{e(item["name"])}</span>{tag_html}</span>'
                     if tag_html else f'<span class="bring-home-name">{e(item["name"])}</span>')
        inner = (f"""
          {name_html}
          <span class="bring-home-qty">{e(item['qty'])}</span>
          {detail_html}""")
        if slug:
            href = rel(depth, f"{base}/{slug}/")
            row_html.append(f'<a class="bring-home-row" href="{href}">{inner}\n        </a>')
        else:
            # An item with no slug has no ingredient page to link to.
            row_html.append(f'<div class="bring-home-row">{inner}\n        </div>')
    rows = "".join(row_html)
    cost = e(bring_home.get("cost_note", ""))
    return f"""
<div class="bring-home-list">{rows}</div>
{f'<p class="bring-home-cost">{cost}</p>' if cost else ""}"""

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
        cost_line = f'<p style="font-size:.85rem;color:var(--muted);margin-top:8px">{e(basket_cost["note"])}</p>'
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

def render_drink(drink, month):
    keep_items  = "".join(f"<li>{e(i)}</li>" for i in drink.get("keep", []))
    adds_items  = "".join(f"<li>{e(i)}</li>" for i in drink.get("season_adds", drink.get("july_adds", [])))
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
    <div class="meal-adds-sublabel" style="margin-top:16px">{e(month)} adds</div>
    <ul class="checklist">{adds_items}</ul>
    <div class="meal-adds-sublabel" style="margin-top:16px">Method</div>
    <p class="drink-method">{e(drink.get('method',''))}</p>
  </div>
  <div class="drink-variations">
    {try_section}
  </div>
</div>"""


def render_drink_link(drink, depth, edition_slug):
    """Drink reference for meal page sidebars, linked to the drink's own page."""
    if not drink or not drink.get("name"):
        return ""
    href = rel(depth, f"{edition_slug}/{drink['slug']}/")
    return f"""
    <section>
      <h3>The drink</h3>
      <ul class="meal-field-notes-list">
        <li class="meal-field-note-title">
          <a href="{href}" class="house-flavor-sidebar-link">{e(drink['name'])}</a>
        </li>
      </ul>
    </section>"""


# ── Link-out blocks (edition page) ─────────────────────────────────────────────

def render_linkout(label, name, intro, card_line, href, cta, heading_id):
    """
    Compact edition-page block for content that lives on its own page.
    Same shape the House Flavor already uses: say what it is, then send the
    reader to the page where they can actually cook from it.
    """
    return f"""
        <div class="section-label">{e(label)}</div>
        <h2 id="{e(heading_id)}">{e(name)}</h2>
        <p class="section-dek">{e(intro)}</p>
        <p class="linkout-line">{e(card_line)}</p>
        <a href="{href}" class="house-flavor-cta">→ {e(cta)}</a>"""

# ── House Flavor ───────────────────────────────────────────────────────────────

def render_house_flavor_uses(uses, depth, edition_slug):
    """Render the 'Use it this week' sequence on the dedicated page."""
    rows = []
    for u in uses:
        meal_slug = u.get("meal")
        label = e(u["label"])
        if meal_slug:
            href = rel(depth, f"{edition_slug}/meals/{meal_slug}/")
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


def render_house_flavor_card(flavor, depth, edition_context, flavor2=None):
    """Compact homepage section for the House Flavor(s)."""
    if not flavor:
        return ""

    ctx          = edition_context
    month        = ctx["month"]
    edition_slug = month.lower()

    def flavor_card(f, label):
        hf_slug = f["slug"]
        href    = rel(depth, f"{edition_slug}/{hf_slug}/")
        uses_html = "".join(f"<li>{e(u)}</li>" for u in f.get("card_uses", []))
        return f"""
        <div class="house-flavor-jar">
          <h3 class="house-flavor-jar-name">{e(f['name'])}</h3>
          <p class="house-flavor-tagline">{e(f['intro'])}</p>
          <ul class="house-flavor-card-uses">{uses_html}</ul>
          <a href="{href}" class="house-flavor-cta">→ {label}</a>
        </div>"""

    if flavor2:
        two_lives = edition_context.get("house_flavor_framing",
            f"{month} gives tomatoes two lives. One stays raw. One gets charred.")
        card1 = flavor_card(flavor,  f"Make the {flavor['name'].lower()}")
        card2 = flavor_card(flavor2, f"Make the {flavor2['name'].lower()}")
        return f"""
      <article class="house-flavor-section col-12" id="house-flavor" aria-labelledby="house-flavor-heading">
        <div class="section-label">House Flavor</div>
        <p class="house-flavor-two-lives" id="house-flavor-heading">{e(two_lives)}</p>
        <div class="house-flavor-two-jars">
          {card1}
          {card2}
        </div>
      </article>"""
    else:
        hf_slug   = flavor["slug"]
        href      = rel(depth, f"{edition_slug}/{hf_slug}/")
        uses_html = "".join(f"<li>{e(u)}</li>" for u in flavor.get("card_uses", []))
        return f"""
      <article class="house-flavor-section col-12" id="house-flavor" aria-labelledby="house-flavor-heading">
        <div class="section-label">House Flavor</div>
        <h2 id="house-flavor-heading">{e(flavor['name'])}</h2>
        <p class="house-flavor-tagline">{e(flavor['intro'])}</p>
        <ul class="house-flavor-card-uses">{uses_html}</ul>
        <a href="{href}" class="house-flavor-cta">→ Make one jar</a>
      </article>"""


def render_house_flavor_link(flavor, depth, edition_slug):
    """Title-only sidebar reference for meal and ingredient pages."""
    if not flavor:
        return ""
    hf_slug = flavor.get("slug", "house-flavor")
    href = rel(depth, f"{edition_slug}/{hf_slug}/")
    return f"""
    <section>
      <h3>House Flavor</h3>
      <ul class="meal-field-notes-list">
        <li class="meal-field-note-title">
          <a href="{href}" class="house-flavor-sidebar-link">{e(flavor['name'])}</a>
        </li>
      </ul>
    </section>"""


def build_house_flavor_page(flavor, edition, depth, canonical_url, edition_context,
                            ingredients_data):
    """Build the dedicated House Flavor page."""
    ctx      = edition_context
    month    = ctx["month"]
    ing_index_path = ctx["ingredient_index_path"]

    edition_href = rel(depth, f"{month.lower()}/")

    notes_by_slug = {n["slug"]: n for n in edition.get("field_notes", []) if "slug" in n}
    ingredients_html = "".join(f"<li>{e(i)}</li>" for i in flavor["ingredients"])
    uses_html = render_house_flavor_uses(flavor["uses"], depth, edition_slug=month.lower())

    # Linked field notes, pointing at the note on the Field Notes page
    field_notes_block = render_linked_note_titles(
        flavor.get("linked_field_notes", []), notes_by_slug,
        rel(depth, f"{month.lower()}/field-notes/"))

    # Linked ingredients
    ing_items = []
    for ing_slug in flavor.get("linked_ingredients", []):
        name = display_name(ing_slug, ingredients_data)
        href = rel(depth, f"{ing_index_path.rstrip('/')}/{ing_slug}/")
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
      <a href="{edition_href}" class="back-link">← {e(month)}</a>
    </div>

    <div class="meal-header">
      <div class="section-label">House Flavor · {e(month)}</div>
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
        title=f"{flavor['name']} — {month} — Seasonal",
        description=flavor["intro"],
        canonical_url=canonical_url,
        css_depth=depth,
        body=body,
        edition_context=edition_context,
        page_class="page--meal",
    )

# ── Drink page ─────────────────────────────────────────────────────────────────

def build_drink_page(edition, depth, canonical_url, edition_context):
    """
    The drink on its own page. It was the tallest block on the edition page, and
    it's the one thing you read while standing at the counter making it.
    """
    drink = edition["drink"]
    month = edition_context["month"]
    edition_href = rel(depth, f"{month.lower()}/")

    keep_items = "".join(f"<li>{e(i)}</li>" for i in drink.get("keep", []))
    adds_items = "".join(f"<li>{e(i)}</li>" for i in drink.get("season_adds", []))
    try_rows = "".join(
        f"""<div class="drink-try-row">
          <span class="drink-try-change">{e(v['change'])}</span>
          <span class="drink-try-context">{e(v['context'])}</span>
        </div>"""
        for v in drink.get("try_another_way", [])
    )
    try_block = f"""
        <section aria-labelledby="try-heading">
          <h2 id="try-heading">Try another way</h2>
          <div class="drink-try">{try_rows}</div>
        </section>""" if try_rows else ""

    body = f"""
    <div style="padding-top:28px">
      <a href="{edition_href}" class="back-link">← {e(month)}</a>
    </div>

    <div class="meal-header">
      <div class="section-label">The drink · {e(month)}</div>
      <h1>{e(drink['name'])}</h1>
      <p class="dek" style="font-size:clamp(1rem,2vw,1.35rem);max-width:680px">{e(drink['intro'])}</p>
    </div>

    <div class="meal-body meal-body--solo">
      <div class="meal-main">
        <section aria-labelledby="keep-heading">
          <h2 id="keep-heading">Keep</h2>
          <ul class="checklist">{keep_items}</ul>
        </section>

        <section aria-labelledby="adds-heading">
          <h2 id="adds-heading">{e(month)} adds</h2>
          <ul class="checklist">{adds_items}</ul>
        </section>

        <section aria-labelledby="method-heading">
          <h2 id="method-heading">Method</h2>
          <p class="drink-method">{e(drink.get('method',''))}</p>
        </section>

        {try_block}
      </div>
    </div>"""

    return render_shell(
        title=f"{drink['name']} — {month} — Seasonal",
        description=drink["intro"],
        canonical_url=canonical_url,
        css_depth=depth,
        body=body,
        edition_context=edition_context,
        page_class="page--meal",
    )

# ── Weekend meal page ──────────────────────────────────────────────────────────

def build_weekend_page(edition, depth, canonical_url, edition_context, ingredients_data=None):
    """
    The weekend meal on its own page — the one meal worth slowing down for.
    A month can label it differently (October calls it the featured cook), and
    can write its method as staged steps. When it does, each stage is named
    after the method pattern it demonstrates, so the recipe teaches the pattern
    rather than only being followed.
    """
    meal  = edition["weekend_meal"]
    month = edition_context["month"]
    label = meal.get("label", "The weekend meal")
    edition_href = rel(depth, f"{month.lower()}/")

    ing_items = "".join(f"<li>{e(i)}</li>" for i in meal.get("ingredients", []))
    note = meal.get("ingredient_note", "")
    note_block = f'<p class="house-flavor-storage">{e(note)}</p>' if note else ""

    chain = render_brings_together(meal.get("brings_together", []), ingredients_data,
                                   depth, edition_context["ingredient_index_path"],
                                   edition_href=edition_href)
    time_line = f'<p class="cook-time">{e(meal["time"])}</p>' if meal.get("time") else ""

    if meal.get("steps"):
        stages = "".join(f"""
            <li class="cook-stage">
              <span class="pattern-step">{e(st['stage'])}</span>
              <p>{e(st['text'])}</p>
            </li>""" for st in meal["steps"])
        method_html = f'<ol class="cook-stages">{stages}\n          </ol>'
    else:
        method_html = f'<p class="drink-method">{e(meal.get("method",""))}</p>'

    after = meal.get("after")
    after_block = f"""
        <section aria-labelledby="after-heading">
          <h2 id="after-heading">{e(after['heading'])}</h2>
          <p class="drink-method">{e(after['body'])}</p>
        </section>""" if after else ""

    body = f"""
    <div style="padding-top:28px">
      <a href="{edition_href}" class="back-link">← {e(month)}</a>
    </div>

    <div class="meal-header">
      <div class="section-label">{e(label)} · {e(month)}</div>
      <h1>{e(meal['name'])}</h1>
      <p class="dek" style="font-size:clamp(1rem,2vw,1.35rem);max-width:680px">{e(meal['intro'])}</p>{chain}
    </div>

    <div class="meal-body meal-body--solo">
      <div class="meal-main">
        <section aria-labelledby="use-heading">
          <h2 id="use-heading">Use</h2>
          <ul class="checklist">{ing_items}</ul>
          {note_block}
        </section>

        <section aria-labelledby="do-heading">
          <h2 id="do-heading">Do</h2>
          {time_line}
          {method_html}
        </section>
{after_block}
      </div>
    </div>"""

    return render_shell(
        title=f"{meal['name']} — {month} — Seasonal",
        description=meal["intro"],
        canonical_url=canonical_url,
        css_depth=depth,
        body=body,
        edition_context=edition_context,
        page_class="page--meal",
    )

# ── Field Notes page ───────────────────────────────────────────────────────────

def build_field_notes_page(edition, depth, canonical_url, edition_context):
    """
    Field Notes on its own page. Kept as one coherent section rather than split
    across ingredient pages: only some notes are about a basket ingredient — the
    rest are pantry and technique advice with no ingredient home — and a rule
    that scatters a section unevenly per edition teaches the reader nothing
    about where to look. One home, and it grows without bloating the edition.
    """
    month = edition_context["month"]
    label = edition.get("field_notes_label", "Field Notes")
    edition_href = rel(depth, f"{month.lower()}/")

    notes = "".join(f"""
        <section id="{e(n['slug'])}" aria-labelledby="fn-{e(n['slug'])}">
          <h2 id="fn-{e(n['slug'])}">{e(n['name'])}</h2>
          <p>{e(n['body'])}</p>
        </section>""" for n in edition["field_notes"])

    body = f"""
    <div style="padding-top:28px">
      <a href="{edition_href}" class="back-link">← {e(month)}</a>
    </div>

    <div class="meal-header">
      <div class="section-label">{e(label)} · {e(month)}</div>
      <h1>{e(label)}</h1>
      <p class="dek" style="font-size:clamp(1rem,2vw,1.35rem);max-width:680px">Small things worth knowing this month.</p>
    </div>

    <div class="meal-body meal-body--solo">
      <div class="meal-main">
        {notes}
      </div>
    </div>"""

    return render_shell(
        title=f"{label} — {month} — Seasonal",
        description=f"{label} for the {month} edition of Seasonal.",
        canonical_url=canonical_url,
        css_depth=depth,
        body=body,
        edition_context=edition_context,
        page_class="page--meal",
    )


def render_field_note_index(notes, href):
    """Titles only on the edition page — you still see what the month teaches."""
    items = "".join(f"""
          <li class="field-note-index-item">
            <a href="{href}#{e(n['slug'])}">{e(n['name'])}</a>
          </li>""" for n in notes)
    return f"""
        <ul class="field-note-index">{items}
        </ul>
        <a href="{href}" class="house-flavor-cta">→ Read the field notes</a>"""


def render_linked_note_titles(linked_slugs, notes_by_slug, fn_href):
    """Sidebar cross-reference, now linked to the note on the Field Notes page."""
    if not linked_slugs:
        return ""
    items = []
    for slug in linked_slugs:
        note = notes_by_slug.get(slug)
        if not note:
            continue
        items.append(f'<li class="meal-field-note-title">'
                     f'<a href="{fn_href}#{e(slug)}" class="house-flavor-sidebar-link">'
                     f'{e(note["name"])}</a></li>')
    if not items:
        return ""
    return f"""
    <section>
      <h3>From Field Notes</h3>
      <ul class="meal-field-notes-list">{"".join(items)}</ul>
    </section>"""

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

def render_meal_season_adds(meal):
    anchor = meal.get("season_anchor", [])
    options = meal.get("season_options", [])
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

def render_shell(title, description, canonical_url, css_depth, body,
                 edition_context, page_class="", section_menu=""):
    """
    edition_context is required. Every page belongs to exactly one edition, and
    the masthead, palette stylesheet, and colophon are all derived from it — a
    default here would silently render one month's chrome around another's copy.
    """
    month        = edition_context["month"]
    location     = edition_context["location"]
    edition_num  = edition_context["edition_number"]
    ing_index    = edition_context["ingredient_index_path"]
    edition_slug = month.lower()

    extra_class  = f" {page_class}" if page_class else ""

    # Staged editions are readable by anyone with the URL but stay out of search
    # results until the month they belong to actually starts.
    noindex = ('\n  <meta name="robots" content="noindex" />'
               if BUILDING_UNPUBLISHED else "")

    base_css     = rel(css_depth, f"css/base.css?v={CSS_VERSIONS.get('base.css', '')}")
    month_css    = rel(css_depth, f"css/{edition_slug}.css?v={CSS_VERSIONS.get(edition_slug + '.css', '')}")
    home_href    = rel(css_depth, "")
    edition_num_str = str(edition_num).zfill(3)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}" />
  <link rel="canonical" href="{e(canonical_url)}" />{noindex}
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
    <!-- Wordmark plus, on the edition page only, a collapsed section menu.
         There is no page-level nav: its links duplicated these under
         near-identical labels while pointing at pages rather than sections. -->
    <a href="{home_href}" class="brand">Seasonal</a>
    {section_menu}
  </header>
  <main id="main">
{body}
  </main>
  <footer>
    <div>Seasonal · Know what now tastes like.</div>
    <div>{e(location)} · {e(month)} · Edition {edition_num_str}</div>
  </footer>
</div>
<!-- Progressive enhancement only: the section menu is a native <details> and
     works without this. It closes the menu after you pick a section, which
     CSS alone cannot do. -->
<script>
  document.querySelectorAll('.sections-menu a').forEach(function (a) {{
    a.addEventListener('click', function () {{
      a.closest('details').open = false;
    }});
  }});
</script>
</body>
</html>"""

# ── Publication homepage ───────────────────────────────────────────────────────

def render_past_editions(past_editions, depth):
    """
    Archive block listing every edition other than the current one, newest first.
    Each entry summarises the month with its 'This month tastes like' card so the
    archive reads as a shelf of back issues rather than a list of links.
    """
    if not past_editions:
        return ""

    entries = []
    for past in past_editions:
        month = past["month"]
        href  = rel(depth, f"{month.lower()}/")
        card  = past.get("month_card", {})
        taste = " · ".join(card.get("items", []))
        sub   = card.get("sub", "")
        entries.append(f"""
      <a href="{href}" class="past-edition">
        <span class="past-edition-month">{e(month)}</span>
        <span class="past-edition-taste">{e(taste)}</span>
        <span class="past-edition-sub">{e(sub)}</span>
      </a>""")

    return f"""
    <section class="pub-past" aria-label="Past editions">
      <div class="section-label">Past editions</div>
      <div class="past-edition-list">
        {"".join(entries)}
      </div>
      <p class="pub-past-note">Every edition stays readable. The month passes; what it taught doesn't.</p>
    </section>"""


def build_publication_home(edition, depth, canonical_url, edition_context, past_editions):
    slug = edition["month"].lower()
    edition_href = rel(depth, f"{slug}/")
    palette = edition.get("palette", {})
    accent = e(palette.get("accent", "#d99662"))

    next_ed = edition.get("next_edition", {})
    next_html = ""
    if next_ed.get("month"):
        next_html = f"""
    <div class="pub-next" aria-label="Next edition">
      <div class="section-label">Next edition</div>
      <div class="pub-next-month">{e(next_ed['month'])}</div>
      <div class="pub-next-status">{e(next_ed.get('status', ''))}</div>
    </div>"""

    past_html = render_past_editions(past_editions or [], depth)

    body = f"""
    <section class="pub-intro" aria-label="About Seasonal">
      <h1 class="pub-headline">Cook with the year.</h1>
      <p class="pub-body">The grocery store offers everything, all the time. Each month, Seasonal narrows that down — the handful of ingredients worth buying while they're at their best, what they go with, and how to cook them.</p>
      <p class="pub-body">Your cooking stays exactly as it is. It starts to taste like the month.</p>
    </section>

    <section class="pub-edition-card" aria-label="Current edition">
      <div class="section-label">Current edition</div>
      <a href="{edition_href}" class="edition-entry">
        <div class="edition-entry-month" style="color:{accent}">{e(edition['month'])}</div>
        <div class="edition-entry-location">{e(edition['location'])}</div>
        <p class="edition-entry-note">{e(edition['opening_note'])}</p>
        <span class="edition-entry-cta">Read the {e(edition['month'])} edition →</span>
      </a>
      {next_html}
    </section>
{past_html}"""

    return render_shell(
        title="Seasonal — Cook with the year.",
        description="Each month, Seasonal narrows the grocery store down to the handful of ingredients worth buying while they're at their best.",
        canonical_url=canonical_url,
        css_depth=depth,
        body=body,
        edition_context=edition_context,
        page_class="page--home",
    )

# ── Pairings, method, tool, progression (edition page) ─────────────────────────
#
# Optional sections. An edition that doesn't carry the field doesn't get the
# section — September has none of them and renders exactly as it did. Together
# they let a month answer "what should I be cooking?" rather than only "what
# should I buy?": ingredients → what they pair with → how to cook them → meals.

def render_pairings(pairings, ingredients_data, depth, ing_index_path):
    """Proteins the basket points toward, and the few pantry things that unlock it."""
    proteins = pairings.get("proteins", [])
    pantry   = pairings.get("pantry", [])

    protein_html = ""
    if proteins:
        cards = []
        for p in proteins:
            move = p.get("default_move")
            move_html = f"""
            <p class="protein-move"><span class="protein-move-head">{e(move['headline'])}</span>
              <span class="protein-move-steps">{render_move_steps(move['steps'])}</span></p>""" if move else ""
            cards.append(f"""
          <div class="protein" id="{e(p['slug'])}">
            <h3 class="protein-name">{e(p['name'])}{render_buy_tag(p.get('buy'), 'pairings.proteins')}</h3>
            <p class="protein-why">{e(p['why'])}</p>
            <p class="pairs-with"><span class="pairs-with-label">With</span> {render_ref_list(p.get('with', []), ingredients_data, depth, ing_index_path)}</p>{move_html}
          </div>""")
        protein_html = f"""
        <div class="proteins">{"".join(cards)}
        </div>"""

    pantry_html = ""
    if pantry:
        rows = "".join(f"""
          <li class="pantry-item">
            <span class="pantry-name">{e(i['name'])}</span>
            <span class="pantry-role">{e(i['role'])}</span>
          </li>""" for i in pantry)
        pantry_html = f"""
        <div class="pantry">
          <div class="meal-adds-sublabel">{e(pairings.get('pantry_label', 'From the pantry'))}</div>
          <ul class="pantry-list">{rows}
          </ul>
        </div>"""

    dek = pairings.get("dek", "")
    return f"""
        <div class="section-label">{e(pairings.get('label', 'Pairings'))}</div>
        <h2 id="pairings-heading">{e(pairings['heading'])}</h2>
        {f'<p class="section-dek">{e(dek)}</p>' if dek else ""}{protein_html}{pantry_html}"""


def render_methods(methods):
    """
    Transferable patterns, not recipes. Each is a short chain of stages with a
    few words under each — the same shape a reader can reuse on a different
    ingredient next month.
    """
    blocks = []
    for m in methods.get("items", []):
        if m.get("compact"):
            # A pattern the reader already has from an earlier month: one line,
            # so the new pattern keeps the visual weight.
            origin = f'<span class="method-origin">{e(m["origin"])}</span>' if m.get("origin") else ""
            blocks.append(f"""
        <div class="method method--compact" id="method-{e(m['slug'])}">
          <h3 class="method-name">{e(m['name'])}{origin}</h3>
          <p class="method-line">{e(m['line'])}</p>
          <p class="default-move-steps">{render_move_steps(m['steps'])}</p>
        </div>""")
            continue
        stages = "".join(f"""
            <li class="pattern-stage">
              <span class="pattern-step">{e(s['step'])}</span>
              <span class="pattern-hint">{e(s['hint'])}</span>
            </li>""" for s in m.get("steps", []))
        origin = f'<span class="method-origin">{e(m["origin"])}</span>' if m.get("origin") else ""
        note = f'<p class="method-note">{e(m["note"])}</p>' if m.get("note") else ""
        uses = (f'<p class="pairs-with"><span class="pairs-with-label">Works on</span> '
                f'{" · ".join(e(u) for u in m["works_on"])}</p>') if m.get("works_on") else ""
        blocks.append(f"""
        <div class="method" id="method-{e(m['slug'])}">
          <h3 class="method-name">{e(m['name'])}{origin}</h3>
          <p class="method-line">{e(m['line'])}</p>
          <ol class="pattern">{stages}
          </ol>
          {note}
          {uses}
        </div>""")
    dek = methods.get("dek", "")
    return f"""
        <div class="section-label">{e(methods.get('label', 'Method'))}</div>
        <h2 id="method-heading">{e(methods['heading'])}</h2>
        {f'<p class="section-dek">{e(dek)}</p>' if dek else ""}
        <div class="methods">{"".join(blocks)}
        </div>"""


def render_bring_it_out(tool, weekend_href):
    """The piece of equipment coming back into season. Restrained on purpose."""
    uses = "".join(f"<li>{e(u)}</li>" for u in tool.get("uses", []))
    fallback = f'<p class="tool-fallback">{e(tool["fallback"])}</p>' if tool.get("fallback") else ""
    cta = (f'<a href="{weekend_href}" class="house-flavor-cta">→ {e(tool["cta"])}</a>'
           if tool.get("cta") and weekend_href else "")
    return f"""
        <div class="section-label">Bring it out</div>
        <h2 id="tool-heading">{e(tool['name'])}</h2>
        <p>{e(tool['line'])}</p>
        <ul class="house-flavor-card-uses">{uses}</ul>
        {fallback}
        {cta}"""


def render_brings_together(groups, ingredients_data, depth, ing_index_path, edition_href=""):
    """
    The featured cook, drawn as the month in one line: what you bought, what it
    went with, how it was cooked, and in what. Each group is joined to the one
    before by "+" (it goes in the pot) or "→" (it's what happens to the pot).
    """
    if not groups:
        return ""
    parts = []
    for i, g in enumerate(groups):
        if i:
            joiner = g.get("join", "+")
            parts.append(f'<span class="chain-join" aria-hidden="true">{e(joiner)}</span>')
        parts.append(f"""
          <span class="chain-group">
            <span class="chain-role">{e(g['role'])}</span>
            <span class="chain-items">{'<span class="chain-sep">, </span>'.join(
                f'<span class="chain-item">{render_ref_list([r], ingredients_data, depth, ing_index_path, edition_href=edition_href)}</span>'
                for r in g['items'])}</span>
          </span>""")
    return f"""
        <div class="chain" role="group" aria-label="What this meal brings together">{"".join(parts)}
        </div>"""


def render_progression(prog):
    """What the month leaves you with. Understated: a list, not a scorecard."""
    items = "".join(f"<li>{e(i)}</li>" for i in prog.get("items", []))
    carried = f'<p class="progression-carried">{e(prog["carried"])}</p>' if prog.get("carried") else ""
    return f"""
        <h2 id="progression-heading">{e(prog['heading'])}</h2>
        <ul class="checklist progression-list">{items}</ul>
        {carried}"""

# ── Edition page ───────────────────────────────────────────────────────────────

def render_section_menu(entries):
    """
    Section jump menu, collapsed into the masthead beside the wordmark.
    A native <details> disclosure: keyboard accessible and fully working with
    JavaScript off. The inline script at the end of the shell only adds the
    nicety of closing it after you pick a section.
    """
    if not entries:
        return ""
    links = "".join(
        f'<a href="#{e(anchor)}">{e(short)}</a>' for anchor, short in entries)
    return f"""<details class="sections">
      <summary aria-label="Jump to a section">Sections</summary>
      <nav class="sections-menu">{links}</nav>
    </details>"""


def build_edition_page(edition, depth, canonical_url, meal_hrefs=None, house_flavor=None,
                       house_flavor2=None, edition_context=None, ingredients_data=None,
                       meals_by_name=None):
    require_fields(edition, ["month", "opening_note", "featured_ingredients",
                              "bring_home", "meal_transformations"], "edition.json")

    slug = edition["month"].lower()
    ing_index_path = edition_context["ingredient_index_path"]

    thesis = edition.get("thesis", "")
    thesis_html = f'<p class="thesis">{e(thesis)}</p>' if thesis else ""

    month = edition["month"]
    month_card = edition.get("month_card", {})
    month_card_items = month_card.get("items", [])
    month_card_sub   = month_card.get("sub", "")
    month_card_html  = ""
    if month_card_items or month_card_sub:
        # Separators are real elements so the card can run as a stacked block on
        # desktop and a single compact line on mobile without duplicate markup.
        items_html = '<span class="month-card-sep"> · </span>'.join(
            f'<span class="month-card-item">{e(i)}</span>' for i in month_card_items)
        month_card_html = f"""
      <aside class="month-card" aria-label="This month tastes like">
        <div class="eyebrow">This month tastes like</div>
        <div class="big">{items_html}</div>
        <div class="sub">{e(month_card_sub)}</div>
      </aside>"""

    basket_href      = rel(depth, ing_index_path)
    field_notes_href = rel(depth, f"{slug}/field-notes/")
    drink            = edition.get("drink")
    weekend          = edition.get("weekend_meal")
    weekend_href     = rel(depth, f"{slug}/weekend/") if weekend else None
    weekend_label    = (weekend or {}).get("label", "The weekend meal")

    # Every section after the basket is optional. They render in one fixed
    # order — ingredients, what they pair with, how to cook them, then meals —
    # so a month only chooses what it carries, never where it goes. Each entry
    # is (anchor, menu label, html); the section menu is built from the same
    # list, so it can't point at a section the month left out.
    sections = []

    sections.append(("basket", "Basket", f"""
      <article class="section col-12" id="basket" aria-labelledby="basket-heading">
        <div class="section-label">The {e(month)} basket</div>
        <h2 id="basket-heading">{e(edition['bring_home']['heading'])}</h2>
        <div class="card card--dark">
          {render_bring_home(edition['bring_home'], ingredients_data,
                             edition.get('featured_ingredients'), depth, ing_index_path)}
        </div>
        <a href="{basket_href}" class="house-flavor-cta">→ All {len(edition['featured_ingredients'])} ingredients, in full</a>
      </article>"""))

    if edition.get("pairings"):
        sections.append(("pairings", edition["pairings"].get("label", "Pairings"), f"""
      <article class="section col-12" id="pairings" aria-labelledby="pairings-heading">
        {render_pairings(edition['pairings'], ingredients_data, depth, ing_index_path)}
      </article>"""))

    if edition.get("methods"):
        sections.append(("method", edition["methods"].get("label", "Method"), f"""
      <article class="section col-12" id="method" aria-labelledby="method-heading">
        {render_methods(edition['methods'])}
      </article>"""))

    if edition.get("bring_it_out"):
        sections.append(("bring-it-out", "Bring it out", f"""
      <aside class="section section--aside col-12" id="bring-it-out" aria-labelledby="tool-heading">
        {render_bring_it_out(edition['bring_it_out'], weekend_href)}
      </aside>"""))

    sections.append(("meals", "Meals", f"""
      <article class="section col-12" id="meals" aria-labelledby="transforms-heading">
        <div class="section-label">The meals</div>
        <h2 id="transforms-heading">Your usual meals, wearing {e(month)}.</h2>
        <p class="section-dek">{e(edition.get('meals_dek', "Keep what you already make. Add what's ripe."))}</p>
        <div class="transformations">
          {render_transformations(edition['meal_transformations'], meal_hrefs, meals_by_name)}
        </div>
      </article>"""))

    if edition.get("field_notes"):
        fn_label = edition.get("field_notes_label", "Field Notes")
        sections.append(("field-notes", fn_label, f"""
      <article class="section col-12" id="field-notes" aria-labelledby="field-notes-heading">
        <div class="section-label" id="field-notes-heading">{e(fn_label)}</div>
        {render_field_note_index(edition['field_notes'], field_notes_href)}
      </article>"""))

    if house_flavor:
        sections.append(("house-flavor", "House Flavor",
                         render_house_flavor_card(house_flavor, depth, edition_context, flavor2=house_flavor2)))

    if drink:
        drink_href = rel(depth, f"{slug}/{drink['slug']}/")
        sections.append(("drink", "Drink", f"""
      <article class="section col-12" id="drink" aria-labelledby="drink-heading">
        {render_linkout("The drink", drink['name'], drink['intro'],
                        drink['card_line'], drink_href, "Make the drink", "drink-heading")}
      </article>"""))

    ritual = edition.get("local_ritual")
    if ritual:
        sections.append(("ritual", "Ritual", f"""
      <aside class="section section--aside col-12" id="ritual" aria-label="{e(ritual['label'])}">
        <div class="section-label">{e(ritual['label'])}</div>
        <h2>{e(ritual['name'])}</h2>
        <p>{e(ritual['description'])}</p>
      </aside>"""))

    if weekend:
        chain = render_brings_together(weekend.get("brings_together", []),
                                       ingredients_data, depth, ing_index_path)
        cta = weekend.get("cta", "Make the weekend meal")
        if chain:
            weekend_inner = f"""
        <div class="section-label">{e(weekend_label)}</div>
        <h2 id="weekend-heading">{e(weekend['name'])}</h2>
        <p class="section-dek">{e(weekend['intro'])}</p>{chain}
        <a href="{weekend_href}" class="house-flavor-cta">→ {e(cta)}</a>"""
        else:
            weekend_inner = render_linkout(weekend_label, weekend['name'], weekend['intro'],
                                           weekend['card_line'], weekend_href, cta, "weekend-heading")
        sections.append(("weekend", weekend.get("menu_label", "Weekend"), f"""
      <article class="section col-12" id="weekend" aria-labelledby="weekend-heading">
        {weekend_inner}
      </article>"""))

    notice = edition.get("one_thing_to_notice")
    if notice:
        sections.append(("notice", "Notice", f"""
      <aside class="section section--aside col-12" id="notice" aria-label="One thing to notice">
        <div class="section-label">One thing to notice</div>
        <h2>{e(notice['headline'])}</h2>
        <p>{e(notice['body'])}</p>
      </aside>"""))

    if edition.get("progression"):
        sections.append(("progression", edition["progression"].get("menu_label", "By month's end"), f"""
      <aside class="section section--aside col-12 progression" id="progression" aria-labelledby="progression-heading">
        {render_progression(edition['progression'])}
      </aside>"""))

    jump_entries = [(anchor, label) for anchor, label, _ in sections]
    sections_html = "\n".join(html_ for _, _, html_ in sections)

    body = f"""
    <section class="hero" aria-label="{e(month)} edition">
      <div>
        <h1>{e(month)}</h1>
        {thesis_html}
        <p class="dek">{e(edition['opening_note'])}</p>
      </div>
      {month_card_html}
    </section>


    <div class="grid">
{sections_html}
    </div>"""

    return render_shell(
        title=f"Seasonal — {edition['month']} in {edition['location']}",
        description=edition["opening_note"],
        canonical_url=canonical_url,
        css_depth=depth,
        body=body,
        edition_context=edition_context,
        section_menu=render_section_menu(jump_entries),
    )

# ── Ingredient index page ──────────────────────────────────────────────────────

def build_ingredient_index(edition, ingredients_data, depth, canonical_url, edition_context):
    ctx   = edition_context or {}
    month = edition["month"]
    slug  = month.lower()
    count = len(edition["featured_ingredients"])

    tiles = []
    for ing_slug in edition["featured_ingredients"]:
        ing  = ingredients_data.get(ing_slug, {})
        name = ing.get("name", ing_slug)
        why  = ing.get("why_now", "")[:90] + ("…" if len(ing.get("why_now","")) > 90 else "")
        # Ingredient pages are children of this index, not siblings of the site root.
        href = f"{ing_slug}/"
        tiles.append(f"""
    <a class="ingredient-index-tile" href="{href}">
      {illustration_slot(ing_slug)}
      <strong>{e(name)}</strong>{render_buy_tag(ing.get("buy"), f"{ing_slug}.json")}
      <span class="why">{e(why)}</span>
    </a>""")

    body = f"""
    <div style="padding:40px 0 20px">
      <a href="{rel(depth, slug + '/')}" class="back-link">← {e(month)}</a>
      <div class="section-label" style="margin-top:8px">The seasonal basket</div>
      <h1 style="font-size:clamp(2.2rem,5vw,4rem);margin:8px 0 16px">{e(month)} ingredients</h1>
      <p class="dek" style="font-size:clamp(1rem,2vw,1.35rem);max-width:600px">
        {count} ingredients worth organizing your week around. Each page explains why now, how to choose it, and what to do with it.
      </p>
    </div>
    <div class="ingredient-index-grid">
      {"".join(tiles)}
    </div>"""

    return render_shell(
        title=f"{e(month)} Ingredients — Seasonal",
        description=f"Seasonal ingredients worth buying in {month} in {edition.get('location', 'San Diego')}.",
        canonical_url=canonical_url,
        css_depth=depth,
        body=body,
        edition_context=edition_context,
    )

# ── Individual ingredient page ─────────────────────────────────────────────────

def build_ingredient_page(ing, depth, canonical_url, edition_context, ingredients_data,
                          house_flavor=None, edition=None):
    require_fields(ing, ["slug", "name", "why_now", "how_to_choose", "buy_this_much",
                          "pairs_with_month", "pairs_with_staples",
                          "weekday_uses", "storage",
                          "one_thing_to_learn"], f"{ing.get('slug')}.json")

    slug = ing["slug"]
    ctx      = edition_context
    month    = ctx["month"]
    location = ctx["location"]
    ing_index_path = ctx["ingredient_index_path"]

    choose_items  = "".join(f'<li>{e(c)}</li>' for c in ing["how_to_choose"])
    weekday_items = "".join(f'<li>{e(u)}</li>' for u in ing["weekday_uses"])

    pairs_month  = ", ".join(e(display_name(p, ingredients_data)) for p in ing["pairs_with_month"])
    pairs_staple = ", ".join(e(p) for p in ing["pairs_with_staples"])

    index_href = rel(depth, ing_index_path)

    # The default move leads the page when there is one: it's the thing to
    # remember at the stall, before any of the detail below it.
    move = ing.get("default_move")
    move_block = f"""
        <section aria-labelledby="move-heading" class="default-move">
          <h2 id="move-heading">The default move</h2>
          <p class="default-move-head">{e(move['headline'])}</p>
          <p class="default-move-steps">{render_move_steps(move['steps'])}</p>
        </section>""" if move else ""

    weekend_block = f"""
        <section aria-labelledby="weekend-heading">
          <h2 id="weekend-heading">On a weekend</h2>
          <p>{e(ing['weekend_use'])}</p>
        </section>""" if ing.get("weekend_use") else ""

    # "Cook it with" is derived, not authored: every protein and pantry item in
    # the edition that names this ingredient. One source of truth for each
    # relationship, shown from both ends.
    pairings = (edition or {}).get("pairings", {})
    cook_with = [p["name"] for p in pairings.get("proteins", []) if slug in p.get("with", [])]
    cook_with += [i["name"] for i in pairings.get("pantry", []) if slug in i.get("with", [])]
    edition_href = rel(depth, f"{month.lower()}/#pairings")
    cook_with_block = f"""
        <section>
          <h3>Cook it with</h3>
          <p style="font-family:ui-sans-serif,system-ui,sans-serif;font-size:.9rem;color:var(--muted)">{", ".join(e(c) for c in cook_with)}</p>
          <a href="{edition_href}" class="house-flavor-sidebar-link" style="font-family:ui-sans-serif,system-ui,sans-serif;font-size:.85rem">→ Pairings</a>
        </section>""" if cook_with else ""

    tag = render_buy_tag(ing.get("buy"), f"{slug}.json")

    body = f"""
    <div style="padding-top:28px">
      <a href="{index_href}" class="back-link">← {e(month)} ingredients</a>
    </div>

    <div class="ingredient-header">
      {illustration_slot(slug)}
      <div class="section-label">{e(month)} · {e(location)}{tag}</div>
      <h1>{e(ing['name'])}</h1>
      <p class="dek" style="font-size:clamp(1rem,2vw,1.45rem);max-width:680px">{e(ing['why_now'])}</p>
    </div>

    <div class="ingredient-body">
      <div class="ingredient-main">{move_block}
        <section aria-labelledby="choose-heading">
          <h2 id="choose-heading">How to choose it</h2>
          <ul class="checklist">{choose_items}</ul>
          <p style="margin-top:12px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.9rem;color:var(--muted)">
            Buy this much: <strong>{e(ing['buy_this_much'])}</strong>
          </p>
          {f'<p style="margin-top:10px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.9rem">{e(ing["buying_note"])}</p>' if ing.get("buying_note") else ""}
          {f'<p style="margin-top:6px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.85rem;color:var(--muted)">{e(ing["price_note"])}</p>' if ing.get("price_note") else ""}
        </section>

        <section aria-labelledby="weekday-heading">
          <h2 id="weekday-heading">During the week</h2>
          <ul class="checklist">{weekday_items}</ul>
        </section>

{weekend_block}

        <section aria-labelledby="learn-heading">
          <h2 id="learn-heading">One thing worth learning</h2>
          <p>{e(ing['one_thing_to_learn'])}</p>
        </section>
      </div>

      <aside class="ingredient-sidebar">
        <section>
          <h3>Good with this month</h3>
          <p style="font-family:ui-sans-serif,system-ui,sans-serif;font-size:.9rem;color:var(--muted)">{pairs_month}</p>
        </section>{cook_with_block}
        <section>
          <h3>Good with your staples</h3>
          <p style="font-family:ui-sans-serif,system-ui,sans-serif;font-size:.9rem;color:var(--muted)">{pairs_staple}</p>
        </section>
        <section>
          <h3>Storage</h3>
          <p style="font-family:ui-sans-serif,system-ui,sans-serif;font-size:.9rem;color:var(--muted)">{e(ing['storage'])}</p>
        </section>
        {render_house_flavor_link(house_flavor, depth, edition_slug=month.lower()) if house_flavor and slug in (house_flavor.get('linked_ingredients') or []) else ""}
      </aside>
    </div>"""

    return render_shell(
        title=f"{ing['name']} — {month} — Seasonal",
        description=ing["why_now"],
        canonical_url=canonical_url,
        css_depth=depth,
        body=body,
        edition_context=edition_context,
        page_class="page--ingredient",
    )

# ── Individual meal page ───────────────────────────────────────────────────────

def build_meal_page(meal, edition, depth, canonical_url, edition_context, house_flavor=None):
    require_fields(meal, ["slug", "name", "intro", "keep",
                           "variations", "works_well_with", "finish"], f"{meal.get('slug')}.json")

    slug  = meal["slug"]
    ctx   = edition_context
    month = ctx["month"]
    meals_back_href = rel(depth, f"{month.lower()}/#meals")

    notes_by_slug = {n["slug"]: n for n in edition.get("field_notes", []) if "slug" in n}
    edition_drink = edition.get("drink", {})

    keep_items   = render_meal_checklist(meal["keep"])
    adds_section = render_meal_season_adds(meal)
    variations   = render_meal_variations(meal["variations"])
    fn_href      = rel(depth, f"{month.lower()}/field-notes/")
    linked_notes = render_linked_note_titles(meal.get("linked_field_notes", []), notes_by_slug, fn_href)

    linked_drink_slug = meal.get("linked_drink")
    drink_link = (render_drink_link(edition_drink, depth, month.lower())
                  if linked_drink_slug and linked_drink_slug == edition_drink.get("slug") else "")

    linked_hf_slug = meal.get("linked_house_flavor")
    flavor_link = render_house_flavor_link(house_flavor, depth, edition_slug=month.lower()) if linked_hf_slug and house_flavor and linked_hf_slug == house_flavor.get("slug") else ""

    works_well = "".join(f'<li>{e(w)}</li>' for w in meal["works_well_with"])

    body = f"""
    <div style="padding-top:28px">
      <a href="{meals_back_href}" class="back-link">← Your usual meals</a>
    </div>

    <div class="meal-header">
      <div class="section-label">{e(month)} · weekday</div>
      <h1>{e(meal.get('display_name', meal['name']))}</h1>
      <p class="dek" style="font-size:clamp(1rem,2vw,1.35rem);max-width:680px">{e(meal['intro'])}</p>
    </div>

    <div class="meal-body">
      <div class="meal-main">
        <section aria-labelledby="keep-heading">
          <h2 id="keep-heading">Keep</h2>
          {keep_items}
        </section>

        <section aria-labelledby="adds-heading">
          <h2 id="adds-heading">{e(month)} adds</h2>
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
        title=f"{meal.get('display_name', meal['name'])} — {month} — Seasonal",
        description=meal["intro"],
        canonical_url=canonical_url,
        css_depth=depth,
        body=body,
        edition_context=edition_context,
        page_class="page--meal",
    )

# ── Consolidated CONTENT.json snapshot ────────────────────────────────────────

def build_content_snapshot(edition, guides, ingredients_data):
    """
    Generate editions/{slug}/CONTENT.json as a consolidated snapshot of all
    editorial content for the edition. Auto-generated — edit src/content/{slug}/ instead.
    """
    slug = edition["month"].lower()
    snapshot = {
        "_generated": f"Auto-generated by src/build.py. Do not edit manually. Edit src/content/{slug}/ instead.",
        **{k: v for k, v in edition.items() if not k.startswith("_")},
        "guides": [{k: v for k, v in g.items() if not k.startswith("_")}
                   for g in guides.get("guides", [])],
        "ingredients": {s: {k: v for k, v in ing.items() if not k.startswith("_")}
                        for s, ing in ingredients_data.items()},
    }
    out = EDITIONS / slug / "CONTENT.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    print(f"  wrote editions/{slug}/CONTENT.json (consolidated snapshot)")

# ── Verification ───────────────────────────────────────────────────────────────

def verify(edition_slug, ingredient_slugs, meal_slugs, house_flavor_slugs, ing_index_dir):
    errors = []
    # The publication homepage is not an edition artifact — main() writes it once
    # after every edition is built, and verify_links() covers it.
    expected_pages = [
        SITE / f"{edition_slug}" / "index.html",
        SITE / ing_index_dir / "index.html",
        SITE / "css" / "base.css",
        SITE / "css" / f"{edition_slug}.css",
    ]
    for slug in ingredient_slugs:
        expected_pages.append(SITE / ing_index_dir / slug / "index.html")
    for slug in meal_slugs:
        expected_pages.append(SITE / f"{edition_slug}" / "meals" / slug / "index.html")
    for hf_slug in house_flavor_slugs:
        expected_pages.append(SITE / f"{edition_slug}" / hf_slug / "index.html")

    for p in expected_pages:
        if not p.exists():
            errors.append(f"Missing output: {p.relative_to(ROOT)}")

    # Check ingredient links appear in the basket index
    index_src = (SITE / ing_index_dir / "index.html").read_text()
    for slug in ingredient_slugs:
        if f"{slug}/" not in index_src:
            errors.append(f"Ingredient link missing from basket index: {slug}")

    # Check meal links appear on the edition page
    edition_src = (SITE / edition_slug / "index.html").read_text()
    for slug in meal_slugs:
        if f"meals/{slug}/" not in edition_src:
            errors.append(f"Meal link missing from edition page: {slug}")

    if errors:
        print("\n  VERIFICATION FAILED:")
        for err in errors:
            print(f"    ✗ {err}")
        sys.exit(1)
    else:
        print(f"\n  Verification passed. {len(expected_pages)} expected files confirmed.")


HREF_RE = re.compile(r'href="([^"]*)"')

def verify_links():
    """
    Walk every built page and confirm each internal link resolves to a real file.
    Cross-edition links are the easiest thing to get wrong when a new edition
    lands, so this runs over the whole site once all editions are written.
    """
    broken  = []
    checked = 0
    for page in sorted(SITE.rglob("index.html")):
        for href in HREF_RE.findall(page.read_text(encoding="utf-8")):
            if href.startswith(("http://", "https://", "mailto:", "data:", "#")):
                continue
            target = href.split("#", 1)[0].split("?", 1)[0]
            if not target:
                continue  # same-page link
            checked += 1
            resolved = (page.parent / target).resolve()
            if resolved.is_dir():
                resolved = resolved / "index.html"
            if not resolved.exists():
                broken.append(f"{page.relative_to(SITE)} → {href}")

    if broken:
        print("\n  BROKEN LINKS:")
        for err in broken:
            print(f"    ✗ {err}")
        sys.exit(1)
    print(f"  Link check passed. {checked} internal links resolve.")

# ── Main ───────────────────────────────────────────────────────────────────────

def edition_context_for(edition, edition_slug):
    """
    The per-edition values every page builder needs so no template hardcodes a month.
    Ingredient index URL pattern: seasonal-basket/{slug}-ingredients/
    """
    return {
        "month":                 edition["month"],
        "location":              edition.get("location", ""),
        "edition_number":        edition.get("edition_number", 1),
        "ingredient_index_path": f"basket/{edition_slug}-ingredients/",
        "house_flavor_framing":  edition.get("house_flavor_framing", ""),
    }


def build_edition(edition_dir_name):
    global BUILDING_UNPUBLISHED
    edition_slug = edition_dir_name  # e.g. "july", "august"
    content_dir  = CONTENT / edition_slug
    ing_dir      = content_dir / "ingredients"
    meals_dir    = content_dir / "meals"

    print(f"\nBuilding edition: {edition_slug}")

    # Load edition JSON
    edition     = read_json(content_dir / "edition.json")
    # guides.json is optional: the guide characters are a voice some months use.
    guides_path = content_dir / "guides.json"
    guides      = read_json(guides_path) if guides_path.exists() else {}
    guides_list = guides.get("guides", [])
    base_url    = edition.get("base_url", "").rstrip("/")
    month       = edition["month"]

    BUILDING_UNPUBLISHED = not is_published(edition)
    if BUILDING_UNPUBLISHED:
        print("  (staged — built and previewable, but not yet the current edition)")

    # Build edition context — passed to all page builders so they never hardcode month/location
    edition_context = edition_context_for(edition, edition_slug)
    ing_index_path  = edition_context["ingredient_index_path"]

    # Ingredient slugs come from edition.json's featured_ingredients list
    ingredient_slugs = edition.get("featured_ingredients", [])

    # Load all ingredient JSON files
    ingredients_data = {}
    for slug in ingredient_slugs:
        ing_path = ing_dir / f"{slug}.json"
        if not ing_path.exists():
            fail(f"Ingredient file missing: {ing_path}")
        ingredients_data[slug] = read_json(ing_path)

    # Meal slugs are discovered by scanning the meals/ directory
    meal_slugs = sorted(
        p.stem for p in meals_dir.glob("*.json")
    ) if meals_dir.exists() else []

    # Load meals
    meals_data = {}
    for slug in meal_slugs:
        meals_data[slug] = read_json(meals_dir / f"{slug}.json")

    # Load house flavors (house-flavor.json, house-flavor-2.json, etc.)
    house_flavors = []
    for hf_filename in sorted(content_dir.glob("house-flavor*.json")):
        hf = read_json(hf_filename)
        derived = [u["meal"] for u in hf.get("uses", []) if u.get("meal")]
        for ms in derived:
            if ms not in meals_data:
                fail(f"{hf_filename.name} references meal '{ms}' which does not exist")
        hf["linked_meals"] = derived
        house_flavors.append(hf)
    house_flavor  = house_flavors[0] if len(house_flavors) >= 1 else None
    house_flavor2 = house_flavors[1] if len(house_flavors) >= 2 else None

    # CSS
    build_css(edition_slug)

    def meal_hrefs_at(depth):
        return {
            meal["name"]: rel(depth, f"{edition_slug}/meals/{slug}/")
            for slug, meal in meals_data.items()
        }

    # Keyed by display name, the same key meal_transformations uses.
    meals_by_name = {meal["name"]: meal for meal in meals_data.values()}

    edition_canonical = f"{base_url}/{edition_slug}/"

    # Edition page
    edition_html = build_edition_page(
        edition, depth=1, canonical_url=edition_canonical,
        meal_hrefs=meal_hrefs_at(1), meals_by_name=meals_by_name,
        house_flavor=house_flavor, house_flavor2=house_flavor2,
        edition_context=edition_context,
        ingredients_data=ingredients_data,
    )
    write_page(SITE / edition_slug / "index.html", edition_html)

    # Ingredient index
    ing_index_dir     = Path(*ing_index_path.split("/"))
    ing_index_canonical = f"{base_url}/{ing_index_path}"
    ing_index_html = build_ingredient_index(
        edition, ingredients_data, depth=2,
        canonical_url=ing_index_canonical,
        edition_context=edition_context,
    )
    write_page(SITE / ing_index_dir / "index.html", ing_index_html)

    # Individual ingredient pages
    for slug in ingredient_slugs:
        ing = ingredients_data[slug]
        ing_canonical = f"{base_url}/{ing_index_path}{slug}/"
        ing_html = build_ingredient_page(
            ing, depth=3, canonical_url=ing_canonical,
            house_flavor=house_flavor, edition_context=edition_context,
            ingredients_data=ingredients_data, edition=edition,
        )
        write_page(SITE / ing_index_dir / slug / "index.html", ing_html)

    # Individual meal pages
    for slug, meal in meals_data.items():
        meal_canonical = f"{base_url}/{edition_slug}/meals/{slug}/"
        meal_html = build_meal_page(
            meal, edition, depth=3, canonical_url=meal_canonical,
            house_flavor=house_flavor, edition_context=edition_context,
        )
        write_page(SITE / edition_slug / "meals" / slug / "index.html", meal_html)

    # House flavor pages — each derives its URL from its own slug field
    hf_slugs_built = []
    for hf in house_flavors:
        hf_slug     = hf["slug"]
        hf_canonical = f"{base_url}/{edition_slug}/{hf_slug}/"
        hf_html = build_house_flavor_page(
            hf, edition, depth=2, canonical_url=hf_canonical,
            edition_context=edition_context,
            ingredients_data=ingredients_data,
        )
        write_page(SITE / edition_slug / hf_slug / "index.html", hf_html)
        hf_slugs_built.append(hf_slug)

    # Drink, Field Notes, and weekend pages exist only when the month carries
    # them. Their pages are the full versions of the edition-page blocks.
    own_pages = []

    # Drink page — same hub-and-spoke pattern as meals and house flavors
    if edition.get("drink"):
        drink_slug = edition["drink"]["slug"]
        drink_html = build_drink_page(
            edition, depth=2, canonical_url=f"{base_url}/{edition_slug}/{drink_slug}/",
            edition_context=edition_context,
        )
        write_page(SITE / edition_slug / drink_slug / "index.html", drink_html)
        own_pages.append(drink_slug)

    # Field Notes page — fixed slug, one home for the whole section
    if edition.get("field_notes"):
        fn_html = build_field_notes_page(
            edition, depth=2, canonical_url=f"{base_url}/{edition_slug}/field-notes/",
            edition_context=edition_context,
        )
        write_page(SITE / edition_slug / "field-notes" / "index.html", fn_html)
        own_pages.append("field-notes")

    # Weekend meal page — fixed slug so the link is stable across editions
    if edition.get("weekend_meal"):
        weekend_html = build_weekend_page(
            edition, depth=2, canonical_url=f"{base_url}/{edition_slug}/weekend/",
            edition_context=edition_context, ingredients_data=ingredients_data,
        )
        write_page(SITE / edition_slug / "weekend" / "index.html", weekend_html)
        own_pages.append("weekend")

    # Consolidated snapshot
    build_content_snapshot(edition, guides, ingredients_data)

    # Verify
    verify(
        edition_slug,
        ingredient_slugs=ingredient_slugs,
        meal_slugs=meal_slugs,
        house_flavor_slugs=hf_slugs_built + own_pages,
        ing_index_dir=str(ing_index_dir),
    )


def main():
    global BUILDING_UNPUBLISHED
    print("Seasonal build")
    print("=" * 40)

    # docs/ is entirely build output — nothing in it is authored by hand.
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()

    # Build all editions found in src/content/
    edition_dirs = sorted(d.name for d in CONTENT.iterdir() if d.is_dir())
    if not edition_dirs:
        fail("No edition directories found in src/content/")

    # Load every edition up front, newest first, so the homepage can show the
    # current edition and link the archive of everything published before it.
    all_editions = sorted(
        ((d, read_json(CONTENT / d / "edition.json")) for d in edition_dirs),
        key=lambda pair: pair[1].get("edition_number", 0),
        reverse=True,
    )
    published = [(d, ed) for d, ed in all_editions if is_published(ed)]
    if not published:
        fail("No published editions found — every edition is marked upcoming")
    current_dir, current_edition = published[0]
    past_editions = [ed for d, ed in published[1:]]

    for edition_dir in edition_dirs:
        build_edition(edition_dir)

    # Publication homepage (site root) — written once, after every edition exists.
    # It always belongs to the current published edition, whatever was built last.
    BUILDING_UNPUBLISHED = False
    print("\nBuilding publication homepage")
    base_url = current_edition.get("base_url", "").rstrip("/")
    root_html = build_publication_home(
        current_edition, depth=0, canonical_url=f"{base_url}/",
        edition_context=edition_context_for(current_edition, current_dir),
        past_editions=past_editions,
    )
    write_page(SITE / "index.html", root_html)

    verify_links()

    print("\nBuild complete.")
    print("Preview: python3 -m http.server --directory docs 8000")
    print("Then open: http://localhost:8000/")


if __name__ == "__main__":
    main()
