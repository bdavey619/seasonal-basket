# Seasonal — Project State

## Product Vision

Seasonal is a monthly companion for people who already know how to cook. The problem it solves is infinite grocery store choice: everything is available all the time, and that abundance makes it hard to know what is worth buying this month.

The reader transformation: from someone who knows how to cook, to someone who knows how to cook the season.

Seasonal does not change how people cook. It changes what they buy — and, over time, how they think about cooking.

**North star:** Teach fewer things that people actually keep.

After a year of reading Seasonal, a reader hasn't accumulated dozens of recipes. They've accumulated a handful of techniques and meals that have genuinely become part of how they cook. That is the ambition.

## Current Status

October is the current edition. November is built and committed with `status: "upcoming"`: its pages exist at `/november/` (noindex) while the homepage still shows October and lists November under "Next edition". On November 1, set November's status to `published` and rebuild; October moves into the archive. July, August, and September remain published and linked from the homepage archive. The architecture, voice, and product philosophy are established. The site is deployed at GitHub Pages from `/docs` on `main`, served at `https://bdavey.co/seasonal-basket/`.

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

## July–September, Reworked

The three summer editions were rebuilt on the October framework after publication: same produce baskets, jars, and drinks, plus one-store closed shopping lists, proteins with pairing lines, protein-first meals with four flavors, a weekend meal that teaches the month's cut, a method Field Note in place of the fish-counter note, and no local ritual.

- **July:** wild salmon slow-roasted beside tomatoes and burrata; skirt steak; shrimp. Meals: tomato plate, tacos, rice bowl, hot-pan dinner, tomato toast.
- **August:** thick pork chops salted early and seared, with charred nectarines; halibut; chicken drumsticks; prosciutto with figs and burrata. Meals: charred plate, sheet pan, pasta, rice bowl, fig toast.
- **September:** chile-rubbed mahi-mahi in tortillas; ground beef picadillo; chicken thighs simmered in salsa verde. Meals: tacos, stuffed roasted chiles (the old weekend meal, now a weekday format), salsa verde simmer, rice bowl, sheet pan.

The original versions are in git history before this change.

## October — What the Edition Teaches

October follows September's blueprint with three changes in how editions are built, all now in `EDITORIAL_PLAYBOOK.md`: one store (plus a fish market for fish, from week three) and one closed shopping list; meal formats that change with the season; and the month's cut and method.

October answers the question September left open — heat or storage — with storage. San Diego's October is a second summer, but the harvest moves inland: Medjool dates, new-crop sweet potatoes, pomegranates, and kabocha, which improves for weeks on the counter. Red bell peppers (the jar's base) and arugula are the fresh side. Every basket item is available at one well-stocked supermarket; guavas and whole fish were cut because they weren't.

**The shopping list** is the basket plus "Also buy" (lemons, limes, corn tortillas, feta, hibiscus tea) and "From your kitchen" (rice, black beans, sourdough, Greek yogurt, eggs, butter, olive oil, garlic, red wine vinegar, sugar, chile flakes, salt). Nothing else is mentioned anywhere in the edition.

**Nutrition layer (trial, started in week three).** Each October recipe card now carries a quiet estimate — about how many calories and how much protein a serving — with carbohydrates, fat, fiber, the serving definition, and what's excluded in a closed panel at the end. Figures come from `tools/nutrition_worksheet.py`; the audit trail is `editions/october/NUTRITION.md`. Servings were made realistic first: the tacos are two dinners, the sweet potatoes two dinners, the sausage pan dinner and one lunch, rice is 1 cup a serving, and yogurt is 2% Greek. The ajvar toast, sweet potatoes, and orzo salad carry a "Make it a meal" line. A "Mornings, and in between" section sits between the dishes and the instinct rows. Carry into November whatever proves useful in October's last week.

**October shopping, sized to a week (week four).** The basket had grown to cover all eight dishes at once (about 18 servings, ~$125–165 with the extras). It's now an "Every week" list plus one line per dish, with a suggested five: fish in parchment, rockfish tacos, roast pork, the sausage pan, and the sweet potatoes, with the orzo salad for lunches — seven dinners and most lunches, two fish dishes. Price sheet used (supermarket / fish market, October 2026, rounded): rockfish $10–18/lb; salmon $14–22/lb (farmed ~$15, sockeye ~$18; yellowtail at the fish market similar); pork tenderloin $5–8/lb; chicken sausage ~$8–11/lb (estimate); kabocha $1.30–2.50/lb; red peppers $1.50–3 each; sweet potatoes ~$1.50–2/lb; Medjool dates ~$7–10/lb (estimate); feta block $5–8; lacinato kale $2.50–3.50 a bunch. Suggested week: about $100–130, near $100 with store-counter rockfish and farmed salmon.

**October nutrition review.** The first review (week three) found thin greens, no reliable oily fish, one legume, and corn tortillas as the only whole grain. Four changes followed, each chosen because it made a dish better: lacinato kale crisps on the sausage pan in the last minutes and is massaged into the orzo salad, where it holds in the fridge as arugula couldn't; the parchment fish became salmon or local yellowtail, the rich fish the method suits; chickpeas joined the orzo salad; and sourdough became "whole-grain if it's a good one," a preference rather than a rule. Now: proteins varied (two rockfish dishes, salmon or yellowtail, chicken sausage, pork, eggs, black beans, chickpeas); omega-3s from the parchment fish; two legumes; a dark green in two dishes and a morning; whole grain in the tortillas and, often, the bread; color wider with the kale. Still worth noticing: the orzo salad remains a lighter lunch (about 20 g protein) and relies on its "Make it a meal" eggs.

**The meals** are eight dishes, then "Or cook by instinct." Dishes: fish baked in parchment with ajvar and lemon (replaced crispy lamb in week three; the sealed packet keeps the fish smell in); roast pork tenderloin with sweet potatoes and date-feta relish; chicken sausages, peppers, and kabocha with ajvar; rockfish tacos with pomegranate and lime yogurt; ajvar toast with fried eggs (meatless); baked sweet potatoes with black beans, ajvar, and lime yogurt (meatless); and the weekend dish, seared rockfish with brown butter and the October salad. Each ends with "How it works" and "Make it your own." The eighth, added in week three, is the first make-ahead: an orzo salad with roasted kabocha, feta, and pomegranate (arugula and pomegranate added per bowl), the template for every edition's fridge salad. The instinct rows carry each protein's pairing line, a few one-sentence moves linked to the dishes, and its best flavors; the four flavors are defined once below. The weekend meal and the old format pages (sheet-pan dinner, warm plate, skillet hash, toast for dinner, baked sweet potato) were folded in or retired.

**The proteins** are four, each with its pairing line on the basket card: rockfish, 2 lbs in two trips (the cut; *a mild fish needs something peppery and sharp*), chicken sausage, 1 lb (*its fat bastes the vegetables*), pork tenderloin, about 1¼ lbs (*lean meat gets its richness from the finish*), and 1 lb of salmon or local yellowtail from the fish market (*rich fish carries smoke, sweetness, and something sharp*), which replaced ground lamb in week three and became a rich fish in the variety review. Eggs and black beans carry the no-meat nights.

The House Flavor is ajvar, made from peppers alone. The drink is cold-steeped hibiscus with pomegranate. One thing to notice is how to read a fresh fillet. No local ritual.

October is nut-free throughout, sesame included. Keep it that way where possible, and never make a nut the load-bearing ingredient of a jar or weekend meal.

## November — What the Edition Teaches

November is the month San Diego's evenings turn: days still reach the mid to high sixties, nights drop to the low fifties. The edition answers with the braise — the plan's cut, method, and tool (bone-in, skin-on chicken thighs; braising; the Dutch oven) — but only where the weather earns it: the weekend dish and the Sunday soup are the long cooks, and the weeknights stay quick.

**The basket** is the first citrus and the cool-weather vegetables: satsuma mandarins, Fuyu persimmons, fennel, Swiss chard, cauliflower, and leeks. Satsumas, persimmons, and the jar's fennel are the "Every week" list; the rest are bought by dish.

**The jar** is pickled fennel with satsuma peel and chile, in September's brine (one cup vinegar, one cup water, a tablespoon of salt, a teaspoon of sugar) — accumulation working as intended. A satsuma mojo was the first idea and was dropped in sourcing: tested recipes keep mojo about a day, and raw garlic in oil shouldn't be stretched, while pickled fennel keeps for weeks. The month's logic is that rich, slow food wants something cold and sharp beside it.

**The meals** are eight dishes, then "Or cook by instinct" (revised after the first draft read as thin on weeknights and too meatless): braised chicken thighs with leeks, fennel, and satsuma (the weekend dish — sear, then uncovered at 325°F to about 195°F); beef, white bean, and chard soup (the Sunday make-ahead — six bowls, freezes); and six weeknight dinners — roast salmon over warm lentils with cauliflower and pickled fennel (eggs in its swaps for a meat-free night); orecchiette with Italian sausage, chard, and melted leeks (white beans in its swaps); farro bowls with the braise's leftovers, chard, and pickled fennel (the leftovers dish, and the month's whole grain); seared flat iron steak with melted leeks; roast chicken thighs and cauliflower; and seared halibut with persimmon and fennel salad. Four flavors: pickled fennel and brine; Parmesan, lemon, and pepper; persimmon, fennel, and lemon; leeks melted in butter.

**The proteins** are chicken thighs (the cut; *skin and bone are flavor you cook into a pot*), beef — chuck for the soup and flat iron for a weeknight (*hard-working cuts need time and liquid; easy ones need a hot pan*), salmon (*rich fish wants something earthy and sharp underneath*), Italian sausage (*its fat and seasoning do the work of a sauce*), and halibut (*lean, sweet fish wants something crisp and sweet-sharp beside it*). Salmon and pork both appeared in October as supporting proteins; neither leads November, which the rotation rule allows, but December should avoid them as leads.

**Shopping.** One simple list again, sized to the suggested week: the braise and the farro bowls it leads to, the soup, salmon over lentils, and orecchiette with sausage — seven dinners and most lunches. Produce: a 2-lb bag of satsumas, 4 Fuyu persimmons, 3 fennel, 6 leeks, 3 bunches chard, 1 cauliflower. Proteins: 6 bone-in chicken thighs, 2½ lbs chuck, 1 lb salmon, ¾ lb Italian sausage. Also buy: lemons, Parmesan, farro, French green lentils, orecchiette, white beans, chicken stock, cinnamon sticks, dark brown sugar. The other three dishes list their needs on their own pages, and the card says so. Price sheet used (October 2026, rounded): bone-in chicken thighs ~$3–5/lb; beef chuck roast $6–10/lb; flat iron $11–15/lb; salmon $14–18/lb (farmed to sockeye); Italian sausage $4–8/lb; halibut $15–35/lb, lingcod $17–25/lb, rockfish $10–18/lb; Parmesan ~$20–24/lb; farro ~$5 for 24 oz; leeks, chard, fennel, cauliflower ~$2.50–5 each or a bunch (estimates); satsumas and persimmons (estimates). The week: about $95–150, typically ~$120, plus ~$15 the first week for Parmesan, cinnamon, and brown sugar — at the top of the $90–120 aim, because it's a bigger week than the first draft.

**The drink** is café de olla (coffee simmered with cinnamon, dark brown sugar, and satsuma peel), named for Sherman Heights. No local ritual.

**November nutrition review.** Proteins: poultry, two cuts of beef, salmon, pork sausage, halibut, plus eggs, lentils, and white beans. Omega-3s: salmon over lentils. Legumes: lentils under the salmon and white beans in the soup. Greens: chard in three dishes and a frittata; cauliflower as the cruciferous vegetable. Grains: farro in the leftovers bowls and under the steak — the first draft's thin spot, fixed with a dish rather than a rule — plus rice, pasta, and sourdough. Color: orange (persimmon, satsuma, salmon), green (chard, leeks, fennel), white (cauliflower). Enough to eat: every dinner carries about 45–80 g protein a serving; the heaviest plates (orecchiette, farro bowls) were trimmed to ¾ lb sausage and ¾ cup farro after the first estimate. Nutrition audit trail: `editions/november/NUTRITION.md`.

## Protein Log

Which proteins each edition led with. No protein leads two months in a row; eggs and beans don't count. July through September were first published on the staples (chicken thighs, ground beef or turkey, salmon) every month, then reworked onto this framework.

| Month | Proteins |
|---|---|
| July | Wild salmon (the cut), skirt steak, shrimp |
| August | Thick pork chops (the cut), halibut, chicken drumsticks, prosciutto |
| September | Mahi-mahi (the cut), ground beef, boneless chicken thighs |
| October | Rockfish (the cut), chicken sausage, pork tenderloin, salmon or yellowtail from the fish market (replaced ground lamb) |
| November | Bone-in chicken thighs (the cut), beef chuck and flat iron, salmon, Italian sausage, halibut (or lingcod or rockfish) |

## The Year's Cuts, Methods, and Tools (draft)

A working plan, not a commitment. Confirm each month against real San Diego weather and seasonality before writing it.

| Month | Cut | Method | Tool | Why then |
|---|---|---|---|---|
| July | Wild salmon | Slow-roasting at low heat | — | Wild Pacific salmon is in season; a low oven suits a month of barely cooking |
| August | Thick bone-in pork chops | Salt early, sear, rest | Cast-iron skillet | Stone fruit is peak; a ten-minute cook suits the heat |
| September | Mahi-mahi | A chile paste, charred in a hot pan | — | Warm-water fish runs late summer; chile season |
| October | Rockfish fillets | The sear | — | Still warm; rockfish more reliable as the water cools |
| November | Bone-in, skin-on chicken thighs | Braising | Dutch oven | The first reliably cool evenings |
| December | Pork shoulder | Slow roasting | Dutch oven or roasting pan | Coldest month; long oven time welcome |
| January | Whole chicken | Roasting + pan sauce | Cast iron or roasting pan | Pairs with citrus season |
| February | Spot prawns | Fast, in the shell | Cast iron | Local trap season reopens |

Each month should build on the last: gentle heat (July), salt-and-rest (August), and the paste-and-char (September) lead to the sear (October) is the first step of the braise (November), which leads to the slow roast (December).

## Next Milestone

Publish November on November 1 (flip its status and rebuild), then begin December: pork shoulder, slow roasting, the Dutch oven or a roasting pan, if the plan still fits the weather. Don't repeat November's lead proteins; keep an oily fish in the month (November's is salmon). Use nutritional variety as inspiration from the start — Keep five weeknight dinners and one simple shopping list.

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
