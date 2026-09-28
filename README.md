# Seasonal

**Working title:** Seasonal  
**Current edition:** September — San Diego  
**Next edition:** October — staged in the repository, live October 1  
**Published:** <https://bdavey.co/seasonal-basket/>

Seasonal is a monthly field guide to what is worth eating, buying, making, and noticing right now.

It is not a recipe database. It is not a nutrition tracker. It is not a grocery delivery service.

Its promise is simpler:

> Walk into the grocery store knowing exactly what you are excited to buy.

## Product shape

Each monthly edition includes:

- A short opening note
- The seasonal basket — six to eight ingredients worth organizing a week around
- Meal transformations — your usual meals, wearing the month
- Field Notes — short pieces, each a secret worth knowing
- At least one House Flavor: a make-once jar that improves meals all week
- One weekend meal
- One seasonal drink
- One thing to notice
- An ingredient page for every ingredient in the basket

Ingredient pages exist only when the ingredient is featured in that month.

Editions do not expire. Past editions stay readable at their own URLs and are linked from the homepage archive.

## Core principle

> Keep the meal. Change the season.

The user can continue eating simple staples such as rice, beans, chicken thighs, salmon, ground beef, or ground turkey. Seasonal changes the produce, herbs, sauces, and flavor direction around those dependable meals.

## Repository structure

```text
/
├── README.md
├── PROJECT_STATE.md          # Source of truth for product decisions
├── EDITORIAL_MANIFESTO.md
├── EDITORIAL_PLAYBOOK.md
├── PRODUCT_SPEC.md
├── CONTENT_SCHEMA.md
├── src/
│   ├── build.py              # Static site generator — no dependencies
│   ├── css/                  # base.css + one palette file per edition
│   ├── illustrations/
│   └── content/              # Canonical, hand-edited editorial source
│       ├── july/
│       ├── august/
│       ├── september/
│       └── october/
│           ├── edition.json
│           ├── guides.json
│           ├── house-flavor*.json
│           ├── ingredients/
│           └── meals/
├── editions/                 # Auto-generated consolidated snapshots
└── docs/                     # Auto-generated site — served by GitHub Pages
```

Only `src/content/` is edited by hand. Both `docs/` and `editions/` are build output; `docs/` is committed because GitHub Pages serves from it.

## Building

```bash
python3 src/build.py
```

No third-party dependencies; requires Python 3.8+. The build wipes and regenerates `docs/`, then verifies its own output twice: once that every expected page exists, and once that all internal links resolve. Either check failing exits non-zero.

To preview locally:

```bash
python3 -m http.server --directory docs 8000
```

## Adding an edition

1. Create `src/content/<month>/` with `edition.json`, `guides.json`, at least one `house-flavor*.json`, plus `ingredients/` and `meals/`.
2. Add `src/css/<month>.css` with that month's palette. Palette variables are the only values that change between editions — all layout and typography live in `base.css`.
3. Set `edition_number` higher than every existing edition. The highest published number becomes the current edition on the homepage; everything below it moves into the archive automatically.
4. Run the build.

### Staging an edition ahead of its month

An edition can be finished and merged before the month it belongs to. Set `"status": "upcoming"` in its `edition.json` and the build will:

- keep the previous month as the current edition on the homepage,
- leave the staged month out of the archive — it appears only in the "Next edition" block, which is driven by the current edition's `next_edition` field,
- still generate every page, so the link check covers the staged edition and it can be previewed at its own URL,
- add `<meta name="robots" content="noindex">` to the staged edition's pages so it stays out of search results while it waits.

To publish it, set `"status": "published"` (or remove the field) and rebuild. Nothing else changes.

## Deployment

GitHub Pages serves the `main` branch from `/docs` at <https://bdavey.co/seasonal-basket/>. Committing a build to `main` publishes it.
