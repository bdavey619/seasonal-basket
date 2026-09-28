# Seasonal — Content Schema

## Monthly Edition

```json
{
  "month": "July",
  "location": "San Diego",
  "edition_number": 1,
  "opening_note": "",
  "palette": {
    "background": "",
    "paper": "",
    "primary": "",
    "secondary": "",
    "accent": "",
    "ink": ""
  },
  "guides": [],
  "featured_ingredients": [],
  "basket": {},
  "confidence": {},
  "staples": [],
  "flavor_paths": [],
  "week": [],
  "weekend_meal": {},
  "drink": {},
  "local_ritual": {},
  "one_thing_to_notice": {},
  "market_question": ""
}
```

## Optional edition sections (the expanded month)

Every section after the basket is optional; the build renders only what an edition carries, always in this order: basket, pairings, method, bring it out, meals, field notes, house flavor, drink, ritual, weekend meal, notice, progression. See `src/content/october/edition.json` for a complete example.

```json
{
  "pairings": {
    "heading": "What to cook it with.",
    "dek": "",
    "proteins": [
      {
        "slug": "chicken-thighs",
        "name": "Bone-in chicken thighs",
        "buy": "for-the-week",
        "why": "",
        "with": ["delicata-squash", "White beans"],
        "default_move": { "headline": "", "steps": [] }
      }
    ],
    "pantry_label": "The pantry that unlocks it",
    "pantry": [{ "name": "", "role": "", "with": [] }]
  },
  "methods": {
    "heading": "How October cooks.",
    "items": [
      { "slug": "braise", "name": "Braise", "origin": "New this month", "line": "",
        "steps": [{ "step": "Sear", "hint": "" }], "note": "", "works_on": [] },
      { "slug": "roast", "name": "Roast hot", "origin": "From September", "line": "",
        "compact": true, "steps": ["Cut thin", "425°F"] }
    ]
  },
  "bring_it_out": { "name": "The Dutch oven.", "line": "", "uses": [], "fallback": "", "cta": "" },
  "weekend_meal": {
    "label": "The featured cook",
    "menu_label": "Featured cook",
    "cta": "Cook it this Sunday",
    "brings_together": [
      { "role": "Basket", "items": ["delicata-squash"] },
      { "role": "Protein", "join": "+", "items": [{ "text": "Chicken thighs", "anchor": "chicken-thighs" }] },
      { "role": "Method", "join": "→", "items": [{ "text": "Braise", "anchor": "method-braise" }] }
    ],
    "time": "",
    "steps": [{ "stage": "Sear", "text": "" }],
    "after": { "heading": "The next day", "body": "" }
  },
  "progression": { "heading": "By the end of October, you'll know how to…", "items": [], "carried": "" }
}
```

In any `with` or `items` list, a basket ingredient slug links to that ingredient's page, `{text, anchor}` links to a section of the edition page, and anything else renders as plain text. Ingredient pages derive a "Cook it with" list from every protein and pantry item whose `with` names them — each relationship is written once.

`buy` is one of `buy-now`, `for-the-week`, `keeps-well`, `if-you-see-it`. The build fails on anything else.

## Guide

```json
{
  "name": "",
  "role": "",
  "location": "",
  "specialty": "",
  "bio": "",
  "quote": "",
  "verified": false
}
```

## Ingredient Page

```json
{
  "slug": "persian-cucumbers",
  "name": "Persian cucumbers",
  "month": "July",
  "why_now": "",
  "guide": "",
  "guide_quote": "",
  "how_to_choose": [],
  "buy_this_much": "",
  "pairs_with_month": [],
  "pairs_with_staples": [],
  "flavor_paths": [],
  "buy": "keeps-well",
  "default_move": { "headline": "Don't peel it.", "steps": ["Halve", "seed", "slice", "olive oil + salt", "roast at 425°F"] },
  "weekday_uses": [],
  "weekend_use": "",
  "drink_use": "",
  "storage": "",
  "one_thing_to_learn": "",
  "market_question": ""
}
```

## Confidence Score

```json
{
  "score": 9.2,
  "lunches_supported": 5,
  "dinners_supported": 5,
  "weekend_meals_supported": 2,
  "waste_risk": "low",
  "assumptions": [
    "User already has pantry basics",
    "User cooks one batch of rice",
    "User cooks one or two proteins ahead"
  ],
  "editorial_note": ""
}
```
