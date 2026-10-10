# Seasonal — Project State

## Product Vision

Seasonal is a monthly companion for people who already know how to cook. The problem it solves is infinite grocery store choice: everything is available all the time, and that abundance makes it hard to know what is worth buying this month.

The reader transformation: from someone who knows how to cook, to someone who knows how to cook the season.

Seasonal does not change how people cook. It changes what they buy — and, over time, how they think about cooking.

**North star:** Teach fewer things that people actually keep.

After a year of reading Seasonal, a reader hasn't accumulated dozens of recipes. They've accumulated a handful of techniques and meals that have genuinely become part of how they cook. That is the ambition.

## Current Status

October is the current edition. July, August, and September remain published and linked from the homepage archive; November is listed under "Next edition". The architecture, voice, and product philosophy are established. The site is deployed at GitHub Pages from `/docs` on `main`, served at `https://bdavey.co/seasonal-basket/`.

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

## Who the Editions Feed

One active cook with a big appetite, cooking dinner every night and eating leftovers for lunch most days. Quantities are written for that, at roughly 8 oz of raw protein per meal, and the basket card says so.

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

October follows September's blueprint with three changes in how editions are built, all now in `EDITORIAL_PLAYBOOK.md`: one store and one closed shopping list; meal formats that change with the season; and the month's cut and method.

October answers the question September left open — heat or storage — with storage. San Diego's October is a second summer, but the harvest moves inland: Medjool dates, new-crop sweet potatoes, pomegranates, and kabocha, which improves for weeks on the counter. Red bell peppers (the jar's base) and arugula are the fresh side. Every basket item is available at one well-stocked supermarket; guavas and whole fish were cut because they weren't.

**The shopping list** is the basket plus "Also buy" (lemons, limes, corn tortillas, feta, hibiscus tea) and "From your kitchen" (rice, black beans, sourdough, Greek yogurt, eggs, butter, olive oil, garlic, red wine vinegar, sugar, chile flakes, salt). Nothing else is mentioned anywhere in the edition.

**The meals** are six formats, each with three flavor directions: sheet-pan dinner, warm plate, fish tacos, toast for dinner, baked sweet potato, and skillet hash (the leftovers format). Rice bowl and pasta are retired for the month.

**The cut** is rockfish fillets: local, more reliable as the water cools, cheaper than salmon. **The method** is the sear — dry fish, hot pan, hands off — taught by the weekend meal (seared rockfish with brown butter, roasted kabocha, and an arugula, pomegranate, and date salad) and named in the Field Note that points ahead to November's braise. **No new tool.**

**The proteins** are three, one per kind of night, each with its pairing line on the basket card: rockfish, 2 lbs (the cut — weekend meal, fish tacos; *a mild fish needs something peppery and sharp*), chicken sausage, 2 lbs (sheet-pan dinner; *its fat bastes the vegetables*), and ground lamb, 1½ lbs (the warm plate; *rich meat wants sweet and sour*). Eggs carry toast for dinner; black beans carry the baked sweet potato.

The House Flavor is ajvar, made from peppers alone. The drink is cold-steeped hibiscus with pomegranate. One thing to notice is how to read a fresh fillet. No local ritual.

October is nut-free throughout, sesame included. Keep it that way where possible, and never make a nut the load-bearing ingredient of a jar or weekend meal.

## Protein Log

Which proteins each edition led with. No protein leads two months in a row; eggs and beans don't count.

| Month | Proteins |
|---|---|
| July–September | Chicken thighs, ground beef or turkey, salmon — the staples, every month. The reason this log exists. |
| October | Rockfish (the cut), chicken sausage, ground lamb |

## The Year's Cuts, Methods, and Tools (draft)

A working plan, not a commitment. Confirm each month against real San Diego weather and seasonality before writing it.

| Month | Cut | Method | Tool | Why then |
|---|---|---|---|---|
| October | Rockfish fillets | The sear | — | Still warm; rockfish more reliable as the water cools |
| November | Bone-in, skin-on chicken thighs | Braising | Dutch oven | The first reliably cool evenings |
| December | Pork shoulder | Slow roasting | Dutch oven or roasting pan | Coldest month; long oven time welcome |
| January | Whole chicken | Roasting + pan sauce | Cast iron or roasting pan | Pairs with citrus season |
| February | Spot prawns | Fast, in the shell | Cast iron | Local trap season reopens |

Each month should build on the last: the sear (October) is the first step of the braise (November), which leads to the slow roast (December).

## Next Milestone

Begin the November edition: bone-in chicken thighs, braising, and the Dutch oven, if the weather has actually turned. Pick two or three other proteins that don't repeat October's — check the protein log. Persimmons and pomegranates peak; the first citrus arrives.

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
