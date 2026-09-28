# Seasonal — Project State

## Product Vision

Seasonal is a monthly companion for people who already know how to cook. The problem it solves is infinite grocery store choice: everything is available all the time, and that abundance makes it hard to know what is worth buying this month.

The reader transformation: from someone who knows how to cook, to someone who knows how to cook the season.

Seasonal does not change how people cook. It changes what they buy — and, over time, how they think about cooking.

**North star:** Teach fewer things that people actually keep.

After a year of reading Seasonal, a reader hasn't accumulated dozens of recipes. They've accumulated a handful of techniques and meals that have genuinely become part of how they cook. That is the ambition.

## Current Status

September is the current edition. October is written, built, and staged behind `"status": "upcoming"` — the homepage keeps leading with September and lists October under "Next edition" until October 1, when flipping that one field and rebuilding publishes it. July and August remain published and linked from the homepage archive. The architecture, voice, and product philosophy are established. The site is deployed at GitHub Pages from `/docs` on `main`, served at `https://bdavey.co/seasonal-basket/`.

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

## September Featured Ingredients

Summer's last word:

- Roasting chiles (poblano, Anaheim, Hatch)
- Tomatillos
- Cilantro
- Limes

Fall's first:

- Delicata squash
- Julian apples
- Table grapes

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
- How much personalization should be added after the static edition proves useful
- Whether the archive stays a flat list or gains its own index page once several editions exist

**Resolved:** archive navigation ships in the first public version — the homepage lists past editions below the current and next ones. Editions do not expire; each stays readable at its own URL.

## July — What the Edition Teaches

July's technique is blistering/charring tomatoes on a dry comal or cast-iron pan. It earns its place: it unlocks the charred tomato salsa, which leads to tacos, beans, fish, and eggs. The complementary lesson — trust ripe tomatoes, don't cook them — is equally important. July teaches both transformation and restraint.

## September — What the Edition Teaches

September is San Diego's overlap month: chile season is at its peak and about to end, while the first squash and the first Julian apples arrive during a week that is still eighty degrees. The edition is built on that overlap rather than pretending the season has turned.

The one new technique is the quick pickle brine underneath the escabeche — one cup vinegar, one cup water, a tablespoon of salt, a teaspoon of sugar — which works on any crisp vegetable and is the thing a reader should still be making a year from now. Charring is deliberately *not* re-taught: July's dry pan and August's covered bowl are assumed, and the chiles simply build on them. That is the accumulation principle working as intended.

The restraint half of the edition is the fruit. Apples and grapes are bought to be eaten raw and cold. Nothing is baked into a dessert. September does not need one.

The House Flavor is a single jar (escabeche), not two. Salsa verde is taught as judgment rather than as a second jar — a Field Note with no fixed ratio — because the season offered it and the North Star did not call for another recipe.

## October — What the Edition Teaches

October is the first edition built on the expanded model. The question it answers is no longer only "what should I buy?" but "what should I be cooking?" — so the page runs ingredients → pairings → method → meals.

October teaches heat. San Diego doesn't look like fall (some of the year's hottest days land this month), but the evenings shorten and the oven comes back on. The one new technique is **the braise**, taught as six named stages — Sear, Aromatics, Deglaze, Liquid, Slow cook, Brighten — and demonstrated by the featured cook (Dutch-oven chicken with delicata and white beans), whose steps carry the same six names. September's hot roast is assumed and shown as a one-line callback. The Dutch oven is the Bring It Out tool.

Proteins are chosen for how they fit the basket, not because meat is "in season": bone-in chicken thighs (the braise), thick pork chops (apples, sage, cider vinegar — and the sear on its own), and California spiny lobster, which genuinely opens off San Diego the first weekend of October.

The quiet lesson under the whole month is *put something sharp against something rich*: lemon in the braise, cider vinegar in the pork pan, pomegranate on the squash.

What October deliberately leaves out: no drink, no local ritual, no one-thing-to-notice, no Field Notes, no house jar. Every one of those sections is still available; October's job was done without them, and the pairings, method, and featured cook carry the weight they used to.

## Next Milestone

Begin the November edition on the same model. Poblanos will be gone; persimmons and pomegranates peak; the first citrus arrives. Decide whether November adds a method (a pot of beans from dry? a slow-roast?) or builds on the braise — and whether any tool is genuinely coming back into season. Don't add one for symmetry.

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
