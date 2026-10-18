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

## Dish and Edition Fields Added in October

Optional fields on a meal (`src/content/<month>/meals/<slug>.json`):

```json
{
  "make_it_a_meal": "One line: what to add, and why it tastes right.",
  "nutrition": {
    "serving": "What one serving is, in plain words.",
    "excludes": "What the estimate leaves out (e.g. the rice).",
    "kcal": [650, 700], "protein": [55, 60], "carbs": [75, 80], "fat": [10, 15], "fiber": [10, 10],
    "with_meal": { "kcal": [900, 1100], "protein": [40, 40] }
  }
}
```

Nutrition figures are `[low, high]`, already rounded (50 kcal, 5 g), copied from `tools/nutrition_worksheet.py`. `with_meal` is the estimate with the "Make it a meal" pairing.

Optional field on an edition:

```json
{
  "mornings": {
    "heading": "Mornings, and in between",
    "dek": "",
    "groups": [ { "label": "Weekdays", "items": [ { "name": "", "text": "" } ] } ]
  }
}
```
