# Seasonal — Editorial Playbook

## Building an Edition, Step by Step

Do these in order. Each step depends on the one before; the reasons behind each live in the sections below.

1. **Read the weather and the season — honestly.** Research what is actually ripe in Southern California this month, and what the weather really is (San Diego's October is a second summer, not New England's fall). Decide what the month teaches: heat or restraint, fresh or storage.
2. **Choose the basket from one store, plus a fish market for fish.** Six to eight seasonal ingredients, mostly vegetables, every one reliably available at a well-stocked supermarket. Include whatever the month's jar is made from. Fish may come from a fish market; everything else that's only at a specialty market stays out. Choose with variety in mind from the start (see "Nutritional Variety as Inspiration"): is there a dark green coming into season, an oily fish at the counter, a legume or grain that belongs with this produce?
3. **Choose the proteins — as many as the meals call for, with no fixed limit.** For each candidate, answer four questions:
   - *Category:* does it fill a gap? Aim for different kinds — fish, poultry, red meat, pork — not one animal on repeat.
   - *Rotation:* did it lead last month? Check the protein log; if so, pick another.
   - *Pairing:* what does it want from this basket, and what general principle does that teach (sharp against mild, fat that bastes, sweet and sour against rich, lean meat gets its richness from the finish)? Each protein should teach a different one.
   - *Cut and weather:* which cut suits the month's weather? Quick, lean cuts when it's warm; long-cooked cuts when it's cool. Seafood seasonality is literal — name it. Meat seasonality usually isn't — say so, and choose the cut for the weather.
   One of the proteins is the month's cut: the new one the weekend meal teaches.
4. **Choose the method and, only if one is genuinely coming back into use, a tool.** The method is taught by the weekend meal and named in one Field Note that points to next month.
5. **Choose the dishes.** Six or seven specific dishes that suit the weather and the basket, including the weekend dish and at least one meatless one. Then write the instinct rows from them: each protein's pairing line and two or three moves, linking the moves the dishes demonstrate. Every dish must be linked from the edition page; the build checks. One of the dishes is **the make-ahead**: something cooked once that keeps in the fridge for snacks and lunches all week (see "The Make-Ahead" below). Then write **Mornings, and in between** from the same basket (see "Mornings, and In Between").
6. **Choose three or four flavors.** Each is two or three things from the shopping list, defined once (what it is, how to do it). Give each protein its two best flavors, following from its pairing line.
7. **Write the shopping list for a real week, and close it.** Size it to five dishes, not to every dish: an "Every week" list of what most dishes share (the jar's produce, citrus, the cheese), then one line per dish saying what that dish adds. Suggest a good five. The dishes stay options; whatever five someone picks, the list still adds up. Basket, proteins (with amounts, meals, and pairing line), "Also buy," and "From your kitchen." Pick one cheese, one citrus, one tortilla. Then read every page — meals, jar, drink, weekend meal, ingredient pages — and remove or list anything not on those lines.
8. **Set the quantities.** One active cook with a big appetite, dinner every night, leftovers for lunch most days: roughly 8 oz of raw protein per meal. State it in the basket card's "feeds" line. Give every recipe a serving size a real person eats: "dinner for one" means one person eats it all; name rice by the cup, yogurt by type (2% Greek), and oil by the tablespoon wherever it's more than a film in the pan.
9. **Write the rest of the edition.** Field Notes, the jar, the drink, one thing to notice. Leave out any section that isn't about cooking this month.
10. **Estimate nutrition, then look back.** Enter each dish in `tools/nutrition_worksheet.py`, run it, and copy the rounded figures into each meal's `nutrition` block (see "Nutrition, Quietly"). Then reread the month against the variety questions below and record what you found in `PROJECT_STATE.md` — by now it should confirm choices already made, not send you back to patch them.
11. **Check and record.** Build (it verifies pages, links, and that every meal is reachable). Check the page at phone and desktop width. Add the month to the protein log and update the year plan in `PROJECT_STATE.md`.

## Product Vision

Seasonal is not a recipe publication. It is a monthly companion for people who already know how to cook.

The problem it solves: modern grocery stores offer infinite choice. Everything is available all the time, and that abundance makes it hard to know what is actually worth buying this month. Seasonal answers that question.

The transformation: from someone who knows how to cook, to someone who knows how to cook the season.

Seasonal does not change how people cook. It changes what they buy — and by extension, how their existing meals taste.

## Editorial Objective

Each edition should make the reader confident about what to buy this month, and capable of using those ingredients across the meals they already make.

Over time, across editions, the reader should quietly accumulate a repertoire — techniques that have become instinct, preparations they return to, meals they no longer need to look up. That accumulation is the long-term product. Each individual edition is one installment in it.

## The Editorial Test

Before publishing any section, ask:

1. Does this help someone know what is worth buying now?
2. Does this reduce decision fatigue?
3. Does this respect the ingredient rather than showing off?
4. Does this work in a real weekday kitchen?
5. Does this sound appreciative rather than pretentious?
6. Will this still feel true ten or thirty years from now?
7. Does this section help someone upgrade the meals they already make — or does it ask them to learn something new without payoff across multiple meals?

## Edition Structure

Each edition is organized around the four pillars. These are editorial scaffolding — they are not visible sections on the page. Readers experience a coherent month; they do not navigate between frameworks.

**What every edition includes:**

- A curated basket of six to eight ingredients, with a shopping card ("This is what I'd bring home")
- One or two foundational techniques that earn their place by unlocking multiple repeatable meals
- One or two house jars or make-once preparations that carry flavor across the week
- A handful of repeatable weekday meals — recognizable, improved by the season
- One weekend meal that is inseparable from the month
- Field Notes: two to four short notes, each a single memorable idea worth knowing
- One seasonal drink
- One thing to notice
- Individual ingredient pages for everything in the basket
- A market question

**What each edition does not include:**

- A confidence score (retired; the shopping card does this job better)
- A prescribed week schedule (retired; meal transformations do this job better)
- A section called "the user's staples" (this lives in the reader's kitchen, not on the page)
- Techniques added for symmetry when the season doesn't naturally call for them

**Page structure (homepage sections, in order):**

1. Hero — month name, thesis, opening note
2. Basket tiles + Shopping card (dark panel)
3. Meal transformations — "Your usual meals, wearing [month]."
4. Field Notes
5. House Flavor — one jar, or two if the season naturally calls for it
6. Drink + Local ritual
7. Weekend meal + One thing to notice

## One Store Plus a Fish Market, One List

Two rules for every edition, from October on:

- **Everything comes from one store, plus a fish market for the fish.** A normal, well-stocked supermarket is the reference (Whole Foods, in practice). Fish is the one exception: a local fish market sells what was caught this week, fresher and more varied than a supermarket counter, so the fish can come from there — and should still work from the store's counter if that's all you have. Name fish by type ("firm white fish — yellowtail, white seabass, or halibut") rather than one species, so the cook can buy what came in. Any other ingredient that's only reliable at a specialty market stays out of the basket — save it for a month that is deliberately about that store. When a fish or cut may be out, name the substitute that works in every meal.
- **The shopping list is closed.** Every ingredient the edition mentions — in meals, the jar, the drink, the weekend meal, the ingredient pages — is either in the basket, on the "Also buy" line, or on the "From your kitchen" line, all shown in the basket card. No optional extras that aren't on a list (no "a splash of mezcal," no "if you have cotija"). Pick one cheese, one citrus, one tortilla, and use them everywhere. Before publishing, read every page against those three lines.

## Dishes First, Instinct Underneath

The meals section has two halves that teach each other.

**The month's dishes (inspiration).** Six or seven specific, named dishes — mostly weeknight, at least one meatless, and the weekend dish, which is where the month's cut and method are taught (there is no separate weekend section). Each commits to one protein, one method, one flavor, and the month's produce, and has a name that lets you picture the plate: "Crispy lamb over yogurt with kabocha, pomegranate, and dates," not "Warm plate." Choose them by hand for culinary sense and real precedent; never generate them from every combination the data allows. Each dish page is a cooking card that ends with **How it works** (the formula and the why, in two or three sentences) and **Make it your own** (two or three intentional swaps).

**Cook by instinct (intuition).** One row per protein (plus eggs and beans): its pairing line, two or three one-sentence moves — method, flavor, produce — and the flavors it's best with. Where a move is what a dish is built on, it links to that dish. Leftover moves live here too ("cube it, crisp it, crack an egg on top"); they don't need pages.

A great dish inspires you to cook; its "How it works" teaches you to cook it without the page. The instinct rows point back to a dish that shows each idea in practice.

**On the page.** In editions built around dishes, the meals section comes first and the basket follows; links under the opening note jump to each, since most visits are "what should I cook?" and the shopping list is a once-a-week stop. Each dish row carries a picture: a plate drawn from 2–5 colors of its main ingredients (`plate` in the edition's `dishes`), replaced by a real photo (`photo`, a path under the edition's `images/`) once the dish has been cooked and shot. Instinct rows open from a single line — the protein and its pairing reason — and each move starts with a one- or two-word `lead` ("Tacos.", "Leftovers.") so the list scans.

**Sourced, then cooked.** Every dish is checked against at least one tested recipe for the same dish or core technique (America's Test Kitchen, NYT Cooking, Food52, a cookbook author's own recipe) and, for meat and fish, the USDA safe-temperature chart. Compare oven temperature, times, doneness cues and step order; where ours differ, change ours or have a reason. Write the dish in our own words — never copy a source's method — and list what it was checked against in the dish's `sources` (title, link, and one line on what we took from it), shown at the foot of the cooking card. A dish is only fully trusted once someone has cooked it as written; fix what that cooking finds.

**The make-ahead.** Every edition has one dish made to keep: cooked once, eaten cold or quickly finished for snacks and lunches through the week. It sits alongside the jar (which keeps a flavor) and the drink — this one keeps a meal. The default is the fridge salad, and it's a formula, not a recipe: **orzo + the month's vegetable + one cheese + a sharp dressing (often the jar) + something fresh added at serving.** Keep orzo constant so the habit repeats; only the produce changes — raw in warm months, roasted in cool ones. Its rules: dress the pasta while it's hot; cook it two minutes past al dente, since the cold firms it; keep greens, herbs, juicy fruit, and burrata out of the container and add them to each bowl; season it harder than a hot dish and taste it again cold; refrigerate within two hours and eat it within three or four days. In the colder months the make-ahead becomes a soup: a big pot made once, eaten through the week and frozen in portions for later. Otherwise, when a month suits something else better, it can be a marinated bean salad or a frittata eaten cold — but it should be one thing, made once, that feeds the week.

**Retiring a page.** Once an edition is live, its URLs may be bookmarked. When a page is removed or renamed, add the old path to the edition's `redirects` (old path → replacement, relative to the edition) so the build leaves a forwarding page behind.

## Mornings, and In Between

A short section after the dishes and before "Or cook by instinct": three weekday ideas, two or three for the weekend, and three for the hours between meals. One line each, like the instinct moves — ideas to cook from, not recipes to follow.

- **From the same basket.** Every idea uses the closed shopping list. Mornings are where the month's produce, the jar, and the leftovers get a second life: a cold wedge of last night's squash, the jar on eggs, the month's fruit on yogurt.
- **Weekdays are fast; weekends can be a project.** Weekday ideas take five minutes or come straight from the fridge. Weekend ideas can borrow from a real tradition (eggs on garlic yogurt, a hash, a slow scramble).
- **Seasonal and culinary, never a fitness menu.** No "protein hacks," no shakes, no packaged bars or granola. If an idea reads like a gym snack, rewrite it as food someone would want to eat.
- **Nut-free, sesame-free.** Like every edition, nothing with tree nuts, peanuts, or sesame — and that rules out most granola, nut butters, pesto, seeded breads, and store-bought "power" snacks.

## What a Week Costs

The basket card's cost line covers everything on the card for the suggested week — the everyday list, "Also buy," and the five dishes — not just produce and proteins. Price it from real shelf prices at the reference store and the fish market, not guesses, and record the price sheet in `PROJECT_STATE.md`. Aim for about $90–120 for a week of dinners and most lunches; fish is the biggest lever, so plan two fish dishes a week rather than three, and say in the cost line which choices move the total.

## Make It a Meal

Some dishes are deliberately light: a toast, a salad, a meatless plate. Where pairing something with it genuinely makes it a better dinner, add one line — "Make it a meal" — after Leftovers: what to add and why it tastes right ("the yolks dress the orzo"). It's optional by design. Don't add it to dishes that are already a full meal, and never change a light recipe just to raise its protein; some dishes should stay snacks, sides, or small dinners.

## Nutrition, Quietly

Nutrition supports the cooking; it never leads it.

- **Where it appears.** One small line on each recipe card — about how many calories and how much protein a serving — and a closed "Nutrition estimate" panel at the very end of the card with carbohydrates, fat, fiber, exactly what a serving is, and what's not included. Never on the edition page, the dish list, or the basket card. No daily totals, no targets, no sorting or filtering by nutrients.
- **How it's estimated.** Every number comes from `tools/nutrition_worksheet.py`, which adds up the recipe's own ingredient amounts using standard values (USDA FoodData Central; Japan's food tables for kabocha, which USDA only lists as generic squash; package labels for branded items like sausage). Each ingredient carries a low and high value so real uncertainty — fish species, sausage brand, how much frying fat stays in the pan — becomes a range. The worksheet writes `editions/<month>/NUTRITION.md`, the audit trail for every figure.
- **No false precision.** Round calories to the nearest 50 and grams to the nearest 5. Show a range whenever the low and high differ. Always say "about" and "estimate."
- **Servings first.** A number is only as good as the serving it describes. Fix vague servings before estimating.
- **Keep it current.** Any change to a recipe's amounts means re-running the worksheet before publishing.

## Nutritional Variety as Inspiration

Variety is a source of ideas, not a box to tick after the fact. Bring these questions to steps 2–5, while the basket and dishes are still taking shape, and let the answers suggest better food: the green that crisps on the sausage pan, the oily fish that parchment was made for, the chickpeas that give a make-ahead salad something to bite into. The test for every addition is the same as for anything else in the edition — it has to make a dish more interesting or more delicious. If it only satisfies a guideline, leave it out.

Prefer substitutions and enhancements inside existing dishes over new recipes or a longer shopping list. Prefer a preference over a rule where quality matters more (a great traditional sourdough beats a mediocre whole-grain one). The record lives in `PROJECT_STATE.md`, never on the site. These are prompts, not quotas — the season decides, and a month can be light on something if the reason is good.

- **Proteins.** At least three kinds across the month (fish, poultry, pork or red meat, eggs or legumes)? Different from last month's lead?
- **Omega-3s.** An oily fish (salmon, mackerel, sardines, yellowtail, black cod) this month or last? Lean white fish doesn't count. When a dish can take more than one fish, estimate each one separately.
- **Legumes.** At least one dish built on beans or lentils, not just a side?
- **Greens.** A leafy or cruciferous green when one is in season?
- **Grains and carbohydrates.** A good spread of carbohydrates (rice, potatoes, bread, tortillas, pasta), and at least one whole grain or whole-grain option?
- **Color and fiber.** Produce from more than one color family? A few high-fiber meals?
- **Enough to eat.** Do the proteins and amounts support dinner and most lunches for an active cook (the "feeds" line)? Do the light dishes have a "Make it a meal"?

Seasonal is written for an active cook — someone who trains, plays outside, and eats to match. That reader informs these questions; it doesn't organize the edition. The season, the basket, and the cooking still come first.

## Meal Formats Change With the Season

The repeatable meals are formats, not fixed dishes: a shape with slots (one vegetable, one protein, one pan, a hot oven, the jar after). Each month chooses three to five formats that suit its weather and basket, and each format gets made more than once within the month. A familiar format can carry over when it still fits; none is permanent. Rice bowl, pasta, and tacos were July's through September's — October replaced them with a sheet-pan dinner, a warm plate, fish tacos, toast for dinner, and a baked sweet potato.

**Every format has three directions**, and they change the flavor, not just the protein: smoky (the jar), cool and sharp (yogurt and fruit), bright and hot (citrus and chile oil), sweet and salty, and so on — all from the same shopping list. Swapping sausage for chicken is not a direction. Six formats with three directions each is about eighteen distinct dinners from one list. Include at least one leftovers format (October's skillet hash) so the week's cooking turns into a different dinner instead of the same one reheated.

**The meals section follows how people decide: protein, then method, then flavor.** It opens with "What do you feel like tonight?" — one row per protein (plus a no-meat row), each listing two or three ways to cook it (links to the meal pages) and the flavors it's best with. Below it, the month's three or four flavors are defined once — a name, what it is, how to do it — instead of being repeated inside every meal. Meal pages stay as the how-to, and their variations are written as protein · flavor pairings. Every meal page must be reachable from at least one protein; the build checks.

**Meal pages are cooking cards**, written for someone standing at the stove with a phone, in the order they work: pick a protein (each with its amount and its own timing), pick a flavor (with the full how-to, so nobody goes back to the edition page), one "You'll need" list with quantities, numbered steps that lead with their time or temperature, and one line on leftovers. When a protein changes the timing, say so inside the step ("Pork: add the tenderloin now"), not in a paragraph above it. Readers can tap a step to mark it done and keep the screen awake while they cook. Nothing goes below the leftovers line: if a flavor uses the month's jar, the jar's recipe is linked inside that flavor, and any Field Note tip that matters belongs in the step where it applies. Protein amounts across a month's meals should add up to the shopping list.

Flavors accumulate like techniques: a reader who has followed Seasonal for a year should have a dozen ways to finish a plate that they reach for without thinking. (Editions without a `tonight` block fall back to the older meal list, and can set `meal_ways_compact` to hide the explanations there.)

Formats accumulate like techniques. After a year, the reader should have a dozen meal shapes they cook without looking anything up.

"Keep the meal. Change the season." still holds for the staples. Read it as: keep it simple, and let the season change the shape of the meal as well as what's in it.

## Proteins: As Many as the Meals Call For, Rotating

There is no fixed number of proteins. An edition names as many as its meals naturally call for — usually three or four, sometimes more — and every meal format is written around a specific one, never "protein of choice." Never drop a protein that belongs with the month's ingredients just to hit a count; a small one like prosciutto with figs earns its place the same way a main one does.

- **One is the month's cut**, the new one the weekend meal teaches. It also returns in one weekday meal.
- **The rest suit that month's formats**, chosen across categories (fish, poultry, red meat, pork) so the week isn't one animal on repeat.
- **No protein leads two months in a row.** Check the protein log in `PROJECT_STATE.md` before choosing, and add the month to it when the edition is done.
- **Eggs and beans don't count.** They're kitchen staples that carry the lighter nights.
- **Every protein carries one line on why it pairs with the basket.** This is the lesson, not decoration — the reader should finish it thinking "huh, that's why." Name the principle, not just the match: *fat that bastes*, *sweet and sour against rich*, *something sharp against something mild*. Those principles transfer to next month's proteins; the specific pairings don't.
- All proteins go in the basket card's "Proteins" block: amount, which meals and lunches it covers, and the pairing line. The month's cut links to its ingredient page.

**Portions.** Quantities are written for one active cook with a big appetite, cooking dinner every night and eating leftovers for lunch most days. The basket card states this in its "feeds" line. Plan roughly 8 oz of raw protein per meal, and cook the sheet-pan and skillet proteins in batches big enough to leave lunches.

## The Month's Cut, Method, and Tool

Produce isn't the only thing that's seasonal. How people cook changes through the year too: summer is raw, grilled, and fast; cooler months bring back bone-in cuts, long cooking, and the heavy pot. Every edition answers three questions — what's ripe, what it's cooked with, and how it's cooked — but only the first gets the page's full weight. The other two ride on sections that already exist:

- **The cut goes in the basket.** One protein a month, chosen to expand the reader's repertoire past the staples — a whole fish, a bone-in cut, a shellfish in season. It gets a row in "This is what I'd bring home" and an ingredient page like any produce: why now, how to choose it, how much, what to ask the counter.
- **The weekend meal teaches the method.** It is where the month's cut meets the month's method, because the weekend is when readers have time to try something new.
- **A Field Note carries the lesson forward.** One short note that names the principle underneath the method, so it transfers to next month's cut.
- **The weekday meals repeat it.** The cut shows up again in at least one weekday meal, so it becomes something the reader cooks, not something they read about once.
- **A tool appears only when one is genuinely coming back into use.** Most months won't introduce one. Never add one for symmetry.

The staples list stays the weekday base. The season changes the produce, and sometimes the cut and the pot.

Seafood seasonality is literal and worth naming. Meat seasonality usually isn't — choose a cut because it fits the weather and the basket, and say so honestly.

## The Weekday / Weekend Philosophy

These are two different modes, and both belong in each edition.

**Weekdays:** Keep the meal. Change the season. The edition should help readers improve the meals they are already going to make. A weekday suggestion should be recognizable from their existing rotation. If it requires explanation, it has gone too far.

**Weekends:** Slow down and let one ingredient be the reason you cook. People often have more time on weekends, may cook with others, and are more willing to try something they have never made before. The Weekend Meal exists to celebrate one seasonal recipe worth slowing down for.

The Weekend Meal earns its place only when the dish is inseparable from the month — when it would not make sense to cook it in any other season.

## Contributor Voice

The publication should surface the people behind seasonal knowledge.

Preferred voices:

- Farmers
- Growers
- Farmers market managers
- Bakers
- Fishmongers
- Cheesemakers
- Produce managers
- Experienced home cooks
- Small neighborhood restaurant owners

Avoid celebrity framing.

Use human, grounded introductions:

> Maria has been growing tomatoes in Escondido since 1989.

Not:

> Award-winning agricultural expert Maria Lopez.

Contributor language should be practical, specific, and unforced.

Good:

> If this were mine, I would slice it, salt it, and eat it over the sink.

Bad:

> This ingredient offers a sophisticated balance of acidity and aromatic complexity.

## Ingredient Page Standard

Ingredient pages exist only for ingredients highlighted in the current month.

Every page should answer:

- Why now?
- How do I choose it?
- How much should I buy?
- What does it pair with this month?
- What does it pair with among my staples?
- What are three simple flavor directions?
- How can I use it on a weekday?
- What is one weekend use?
- How should I store it?
- What is one thing worth learning?
- What should I ask the farmer?

## Language Rules

Prefer:

- Favorite ways
- Start here
- This week
- If this were mine
- Good with
- Try it with
- Use the rest for

Avoid:

- Expressions
- Elevated
- Artisanal
- Curated culinary experience
- Flavor journey
- Chef-driven
- Gourmet

## Repetition

Repetition is a feature.

A featured ingredient should appear across several meals in the same week.

Do not create artificial variety simply to avoid repetition.

## The Ingredient-First Principle

Seasonal reverses the normal cooking process.

Most cooking starts with a recipe and then sources the ingredients. Seasonal starts with what is exceptional today and builds dinner from there.

The reader's transformation is not just learning new meals. It is learning a new sequence:

1. Discover what's at its best right now.
2. Build dinner around it.

This is how a farmer shops. It is how a fisherman eats. It is how good home cooking actually works in a place with good produce and a good fish counter.

Every section of the edition should reinforce this sequence — not by stating it, but by demonstrating it.

## North Star

Teach fewer things that people actually keep.

Most food media optimizes for breadth. Five hundred tomato recipes. A new idea every day. Seasonal optimizes for retention. If someone remembers, six months later, how to blister tomatoes, how to make a vinaigrette, how to roast peppers, how to brown butter — the publication has genuinely changed how they cook. That is a more enduring ambition than helping someone decide what to make for dinner tonight.

## The Four Pillars

Each edition is built on four editorial pillars. These are scaffolding, not visible architecture. Readers should experience a coherent month — not four distinct sections.

**1. Seasonal ingredients.** A tightly curated basket that reduces decision fatigue. Opinionated about what is actually worth buying right now. Not exhaustive.

**2. Foundational techniques.** One or two techniques per edition, maximum — chosen because they permanently expand the reader's cooking vocabulary and naturally unlock multiple meals throughout the month. If a technique doesn't earn its place this way, it doesn't belong. Seasonal is not a cooking school.

**3. Make-once preparations.** A sauce, a brine, a braise base, a broth — whatever form the season naturally calls for. Made once, used across the week. Every edition should have at least one. A second belongs only when it serves a genuinely different flavor direction — not for symmetry.

**4. Repeatable meals.** Every technique and every house jar should naturally lead to meals readers will actually make again. The goal is not variety. It is confidence through repetition.

The overarching promise: seasonal ingredients, approachable techniques, repeatable meals with big flavor.

## Don't Manufacture Symmetry

Every month should teach what the season naturally wants to teach.

Some months will have two foundational techniques. Some will have one. Some ingredients are best transformed; others are best left almost untouched. Some months teach how to cook. Others teach when not to cook. Both are equally valuable.

A technique should not be added simply because last month had one. A second jar should not be added simply to match the first. If the season offers it naturally, include it. If it requires forcing, leave it for the month where it belongs.

This is a gardener's mindset: pay attention to what the season is offering, then build the edition around that. The season determines the curriculum.

## Techniques

Techniques earn their place exactly the same way ingredients do.

A technique belongs in an edition when it meets all three of these conditions:

1. It permanently expands the reader's cooking vocabulary.
2. It naturally unlocks multiple meals during that month.
3. It could not be taught as effectively in any other season.

Blistering tomatoes in July meets all three. It is worth teaching. A technique that only unlocks one dish, or that could be demonstrated with any ingredient at any time of year, does not belong.

Not every house jar needs a technique underneath it. Sometimes a great seasonal ingredient needs only a simple preparation. The vinaigrette in July teaches something real — trust ripe tomatoes, don't cook them — but that is a lesson in judgment, not heat. Judgment is a technique too. Some of the most important things Seasonal can teach are when not to cook.

## How Editions Accumulate

Seasonal is not twelve independent editions. It is one ongoing education, delivered monthly.

A reader who has followed along for a year has not accumulated twelve sets of seasonal ingredients. They have accumulated a repertoire: a handful of techniques that have become instinct, a set of house preparations they return to without looking anything up, and a collection of repeatable meals that feel like their own cooking now.

**Each edition should add to that repertoire, not replace it.**

This has practical implications:

A technique introduced in July (blistering tomatoes) is available to all future editions. August does not need to re-teach it. If August's basket calls for charred peppers, the charring technique from July is already in the reader's hands. The edition can assume it and build forward.

Make-once preparations accumulate across the year. The vinaigrette from July may appear by reference in a September salad. The salsa from July may reappear when dried chiles are in season. These callbacks are not cross-promotion — they are the point. They show the reader that what they learned last month is still useful.

Repeatable meals are not monthly specials. If the rice bowl from July is a good rice bowl, it belongs in August too — with different seasonal additions. The meal is the constant. The season changes around it.

**What each edition should leave the reader with:**

At the end of each edition, the reader should have at least one thing they will still be using a year later. It could be a technique, a shopping habit, a jar recipe, or a single repeatable meal. If an edition does not clearly answer "what will they keep from this?" it has not done its job.

**Cross-edition continuity:**

- The drink should feel like it belongs to the same publication across months, even if it is completely different. The Hillcrest Spritz is July's. August's drink should feel like a natural companion — not a repetition, not an interruption.
- Techniques from prior editions can be assumed without re-explanation. A brief callback ("the same charring technique from last month") is sufficient.
- Staple meals carry forward. The basket changes; the meals stay familiar.

## Recipe Philosophy

Most content should be meal guidance, not formal recipes.

Use recipes only when precision materially improves the outcome.

Preferred format:

- What you need
- What to do
- What to use next

## Design Principles

- Timeless over trendy
- Editorial over app-like
- Botanical identification over food glamour
- Seasonal colors derived from the basket
- Generous breathing room
- Clear hierarchy
- No infinite scroll
- No advertising
- No trend language
- No unnecessary photography

## What We've Learned Building July

These are insights earned while building the first edition. They are not rules — they are things that turned out to be true and should be carried forward.

**Confidence matters more than recipes.** The goal is not to give people new things to cook. It is to help them feel confident choosing and using ingredients they may not have bought before. A reader who feels comfortable picking a ripe tomato has gained something more durable than a new recipe.

**Grocery stores are the venue, not farmers markets.** The edition should feel equally at home for someone shopping at Trader Joe's, Whole Foods, Sprouts, Walmart, or a farmers market. The ingredient is what matters. Where it's purchased is secondary.

**The shopping card beats the confidence score.** An editorial shopping list ("This is what I'd bring home") answers a more useful question than a numerical confidence metric. Quantities and brief notes feel like advice from someone who knows these ingredients. Numbers feel like a feature.

**The Week section worked against the philosophy.** Prescribing specific weekday meals — "Tuesday: chicken rice bowl, Wednesday: salmon wrap" — implied that Seasonal was planning the reader's week. The meal transformations section does the same job better by showing how July slots into meals the reader already makes.

**Repetition is the architecture.** A basket that features eight ingredients, each used only once, feels overwhelming. A basket where tomatoes appear in five meals and basil in four feels coherent. The repetition is the whole point — it's how the season actually works.

**The House Flavor is the connective tissue.** One sauce or preparation that works across rice bowls, pasta, chicken, and white beans turns the basket into a system rather than a list of ingredients. Every edition should have one.

**Field Notes should feel like secrets, not essays.** Each note should land on a single memorable idea. If someone remembers one sentence from the Field Notes while they're cooking next week, the section has succeeded. Length is the enemy.

**The Weekend Meal earns its place when it's inseparable from the month.** Tomatoes, burrata, basil, and sourdough in July works because the dish only makes sense in peak tomato season. A weekend meal that could be made any month of the year should not be the Weekend Meal.

## Place and Seasonal Identity

Each edition should feel subtly rooted in its place — not through landmarks or restaurant recommendations, but through everyday habits and the produce that defines the month.

The goal is not a travel guide. It is the quiet recognition that someone who lives here buys differently than someone who does not.

**Fish:** In coastal San Diego, buying fresh fish is a natural part of the week. The edition should teach readers to approach a fish counter with curiosity — asking what's freshest rather than committing to a species — because that is how good fish dinners happen here. This belongs in Field Notes, not in a new section.

**Mexican flavor vocabulary:** San Diego home cooking is quietly influenced by proximity to Mexico. This influence belongs in Seasonal as a slow accumulation — fresh herbs, limes, chiles, simple salsas, instinctive flavor combinations — not as a recipe genre. The House Flavor section is the natural vehicle for this over the course of the year. July's flavor is correctly tomato-forward. Future editions (August, September) should look for natural opportunities to deepen this vocabulary when the seasonal ingredients invite it.

**Restraint:** If an ingredient or habit doesn't belong naturally to the month, leave it for the month where it does.

## Sourcing and Organic Guidance

Organic is optional, not a condition of participation. Seasonal prioritizes produce that is ripe, in season, accessible, and likely to be eaten. Any organic guidance must be evidence-based and useful enough to justify the additional decision.

The underlying principle: conventional produce in season is worth eating. Seasonal should never discourage someone from buying fruits and vegetables because the theoretically ideal version is unavailable or unaffordable.

## Publication Checklist

- Is the basket small enough to remember?
- Is it large enough to support a week?
- Are weekday meals truly realistic?
- Is one meal special enough to justify the shopping trip?
- Is every featured ingredient used more than once?
- Is the waste risk acceptably low?
- Is the contributor voice grounded and credible?
- Does the page help someone shop with confidence?
- Does each technique unlock multiple meals this month — or does it only serve one?
- Is there anything in this edition that was added for symmetry rather than because the season offered it?
- Six months from now, what is one thing the reader will still remember from this edition?
- Tomorrow, what ordinary thing will the reader notice differently?
