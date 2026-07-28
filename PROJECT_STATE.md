# Seasonal — Project State

## Product Vision

Seasonal is a monthly companion for people who already know how to cook. The problem it solves is infinite grocery store choice: everything is available all the time, and that abundance makes it hard to know what is worth buying this month.

The reader transformation: from someone who knows how to cook, to someone who knows how to cook the season.

Seasonal does not change how people cook. It changes what they buy — and, over time, how they think about cooking.

**North star:** Teach fewer things that people actually keep.

After a year of reading Seasonal, a reader hasn't accumulated dozens of recipes. They've accumulated a handful of techniques and meals that have genuinely become part of how they cook. That is the ambition.

## Current Status

July edition is live. The architecture, voice, and product philosophy are established. The edition is deployed at GitHub Pages from `/docs` on `main`.

## What We Know

**The organizing unit is the month.** Each edition is built around four editorial pillars — seasonal ingredients, foundational techniques, house jars, and repeatable meals. These are scaffolding, not visible sections. Readers should experience a coherent month.

**Seasonal ingredients.** A tightly curated basket — typically six to eight ingredients — that reduces decision fatigue. The publication is opinionated about what is worth buying right now, not exhaustive.

**Foundational techniques.** One or two per edition, chosen because they permanently expand the reader's cooking vocabulary and naturally unlock multiple meals throughout the month. A technique that only serves one dish doesn't belong. Seasonal is not a cooking school. Some months teach how to cook. Others teach when not to cook. Both are equally valuable — restraint is not a lesser edition.

**House jars and foundations.** Make-once preparations that leverage seasonal abundance and improve meals all week. Every edition has at least one. A second belongs only when it serves a genuinely different flavor direction, not for symmetry. July has two: a raw vinaigrette (Mediterranean) and a charred salsa (Baja). Both use the same tomato. Different technique, different life.

**Repeatable meals.** Every technique and every house jar should naturally lead to meals readers will actually make again. The goal is not variety. It is confidence through repetition.

**Don't manufacture symmetry.** The season determines the curriculum. Some months have two techniques; some have one; some ingredients are best transformed, others best left almost untouched. Nothing should be added simply to match last month or to complete a pattern.

**Repetition is the architecture.** A basket where tomatoes appear in five meals and basil in four feels coherent. Repetition is the whole point.

**Weekdays:** help readers improve the meals they are already going to make.
**Weekends:** one recipe worth slowing down for — inseparable from the month.

**Familiar staple meals remain intact.** Seasonal produce and flavors change around them.

**Ingredient pages** exist only for ingredients highlighted in the current month.

**The Drink** captures the season in one glass. Make it on repeat.

**The confidence score has been retired.** The shopping card ("This is what I'd bring home") replaces it.

**The Week section has been retired.** Meal transformations do this job better.

**Venue:** Seasonal should feel equally at home for someone shopping at a farmers market, Whole Foods, Trader Joe's, Sprouts, or Walmart. Conventional produce in season is worth eating.

**Organic guidance** is internal only. Never discourage someone from buying produce because the ideal version is unavailable or unaffordable.

**Tone:** appreciative, practical, and grounded — like a generous, experienced shopper talking to a friend beside them in the produce section.

**Design:** timeless, not trendy. No advertising. No infinite scroll. No trend language. The color palette changes by month, derived from the basket.

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
- House Flavor pages — Tomato Herb Vinaigrette and Charred Tomato Salsa, each with full recipe and use guide

## Open Questions

- Whether guide voices are real contributors at launch or added later
- Illustration sourcing and style
- Whether archive navigation should exist in the first public version
- How much personalization should be added after the static edition proves useful
- August featured ingredients and palette

## July — What the Edition Teaches

July's technique is blistering/charring tomatoes on a dry comal or cast-iron pan. It earns its place: it unlocks the charred tomato salsa, which leads to tacos, beans, fish, and eggs. The complementary lesson — trust ripe tomatoes, don't cook them — is equally important. July teaches both transformation and restraint.

## Next Milestone

Begin the August edition. Identify the technique(s) the August basket naturally wants to teach before settling on the ingredient list.

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
