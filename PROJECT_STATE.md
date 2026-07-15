# Seasonal — Project State

## Product Vision

Seasonal is a monthly companion for people who already know how to cook. The problem it solves is infinite grocery store choice: everything is available all the time, and that abundance makes it hard to know what is worth buying this month.

The reader transformation: from someone who knows how to cook, to someone who knows how to cook the season.

Seasonal does not change how people cook. It changes what they buy — and by extension, how their existing meals taste.

## Current Status

July edition is live. The architecture, voice, and product philosophy are established. The edition is deployed at GitHub Pages from `/docs` on `main`.

## What We Know

- The organizing unit is the month.
- The featured ingredients define the edition — typically six to eight.
- The edition teaches the season into existing meals, not new recipes.
- Repetition is a feature. Every featured ingredient should appear more than once across the week.
- Weekdays: help readers improve the meals they are already going to make.
- Weekends: one recipe worth slowing down for — inseparable from the month.
- Familiar staple meals remain intact. Seasonal produce and flavors change around them.
- Ingredient pages exist only for ingredients highlighted in the current month.
- The House Flavor is one sauce, dressing, or preparation that works across several of the week's meals.
- The Drink captures the season in one glass. Make it on repeat.
- The confidence score has been retired. The shopping card ("This is what I'd bring home") replaces it.
- The Week section has been retired. Meal transformations do this job better.
- Seasonal should feel equally at home for someone shopping at a farmers market, Whole Foods, Trader Joe's, Sprouts, or Walmart. Conventional produce in season is worth eating.
- Organic guidance is internal only. Never discourage someone from buying produce because the ideal version is unavailable or unaffordable.
- The tone should be appreciative, practical, and grounded — like a generous, experienced shopper talking to a friend beside them in the produce section.
- Design is timeless, not trendy. No advertising. No infinite scroll. No trend language.
- The color palette changes by month, derived from the basket.
- Botanical illustrations may provide identification and character when commissioned.

## User Staples

- Sticky white rice
- Ground beef or turkey
- Chicken thighs
- Salmon
- Beans
- Sourdough
- Greek yogurt

## July Featured Ingredients

- Ripe tomatoes (any variety)
- Persian cucumbers
- Peaches
- Sweet corn
- Basil
- Mint
- Cherries
- Blackberries

## Information Architecture (July)

Homepage sections, in order:

1. Hero — month, thesis, opening note, month-card aside
2. Basket (col-8) + Shopping card (col-4, dark)
3. Meal transformations — "Your usual meals, wearing July."
4. Field Notes — three short notes, each a secret worth knowing
5. House Flavor — one jar, several jobs
6. Drink (col-7) + Local ritual (col-5)
7. Weekend meal (col-7) + One thing to notice (col-5)

Supporting pages:

- Ingredient index — all eight ingredients
- Individual ingredient pages — why now, how to choose, buy this much, pairs with, weekday uses, weekend use, storage, one thing to learn, market question
- Meal pages — rice bowl, tacos, pasta
- House Flavor page — full recipe and use guide

## Open Questions

- Whether guide voices are real contributors at launch or added later
- Illustration sourcing and style
- Whether archive navigation should exist in the first public version
- How much personalization should be added after the static edition proves useful
- August featured ingredients and palette

## Next Milestone

Begin the August edition.

## Development Handoff Goal

Claude Code should be able to read this repository and understand:

- Why the product exists
- What the product is not
- The required page structure
- The intended editorial voice
- The weekday / weekend philosophy
- The MVP boundaries
- The content model
- The visual direction
