"""
Seasonal — nutrition worksheet.

Editorial tool, not part of the build. For each dish it adds up per-serving
estimates from the ingredient amounts written in the recipe, using low/high
values per ingredient so uncertainty (fish species, sausage brand, how much
frying oil is eaten) shows up as a range instead of false precision.

Run:  python3 tools/nutrition_worksheet.py october
It writes editions/<month>/NUTRITION.md (the audit trail) and prints the
rounded figures to copy into each meal's "nutrition" block. When a recipe's
amounts change, update its entry here and re-run before publishing.

Values are per 100 g unless a unit is named. Sources: USDA FoodData Central
(SR Legacy) via its published entries, package labels for branded items, and
Japan's Standard Tables of Food Composition for kabocha, which USDA lists only
as generic winter squash.
"""
import sys
from pathlib import Path

# name: (unit_grams or None for per-100g basis, {nutrient: (low, high)}, source)
# Nutrients: kcal, protein, carbs, fat, fiber — per 100 g (or per unit when unit is set).
DB = {
    "rockfish":        (None, dict(kcal=(90, 90), protein=(18.4, 18.4), carbs=(0, 0), fat=(1.3, 1.6), fiber=(0, 0)), "USDA: rockfish, Pacific, raw"),
    "firm white fish": (None, dict(kcal=(91, 146), protein=(18.4, 23.1), carbs=(0, 0), fat=(1.3, 5.2), fiber=(0, 0)), "USDA: halibut / seabass (low) to yellowtail (high), raw"),
    "chicken sausage": (85, dict(kcal=(160, 190), protein=(13, 15), carbs=(3, 5), fat=(11, 13), fiber=(0, 0)), "Package labels, per 85 g link (brands vary)"),
    "pork tenderloin": (None, dict(kcal=(109, 120), protein=(20.9, 21), carbs=(0, 0), fat=(2.2, 3.5), fiber=(0, 0)), "USDA: pork tenderloin, raw, lean only to lean and fat"),
    "egg":             (50, dict(kcal=(72, 72), protein=(6.3, 6.3), carbs=(0.4, 0.4), fat=(4.8, 4.8), fiber=(0, 0)), "USDA: egg, whole, large"),
    "black beans":     (None, dict(kcal=(110, 132), protein=(7, 8.9), carbs=(20, 23.7), fat=(0.5, 0.5), fiber=(7, 8.7)), "USDA: black beans, cooked / canned, drained"),
    "greek yogurt 2%": (None, dict(kcal=(70, 73), protein=(10, 10.1), carbs=(3.5, 3.5), fat=(2, 2.1), fiber=(0, 0)), "Label: 2% plain Greek yogurt (170 g = 120 kcal, 17 g protein)"),
    "feta":            (None, dict(kcal=(264, 264), protein=(14.2, 14.2), carbs=(4.1, 4.1), fat=(21.3, 21.3), fiber=(0, 0)), "USDA: feta"),
    "olive oil":       (None, dict(kcal=(884, 884), protein=(0, 0), carbs=(0, 0), fat=(100, 100), fiber=(0, 0)), "USDA: olive oil (1 tbsp = 13.5 g)"),
    "butter":          (None, dict(kcal=(717, 717), protein=(0.9, 0.9), carbs=(0.1, 0.1), fat=(81, 81), fiber=(0, 0)), "USDA: butter (1 tbsp = 14.2 g)"),
    "sourdough":       (None, dict(kcal=(272, 272), protein=(10.8, 10.8), carbs=(51.9, 51.9), fat=(2.4, 2.4), fiber=(2.2, 2.2)), "USDA: French or sourdough bread"),
    "corn tortilla":   (26, dict(kcal=(52, 57), protein=(1.4, 1.5), carbs=(10.7, 11.6), fat=(0.7, 0.7), fiber=(1.5, 1.6)), "USDA: corn tortilla, ~6-inch"),
    "rice, cooked":    (None, dict(kcal=(130, 130), protein=(2.7, 2.7), carbs=(28.2, 28.2), fat=(0.3, 0.3), fiber=(0.4, 0.4)), "USDA: white rice, cooked (1 cup = 158 g)"),
    "orzo, dry":       (None, dict(kcal=(357, 371), protein=(12.5, 13.6), carbs=(71, 75), fat=(1.2, 1.5), fiber=(2.5, 3.5)), "USDA branded / generic enriched pasta, dry"),
    "kabocha":         (None, dict(kcal=(70, 90), protein=(1.2, 1.9), carbs=(17, 20.6), fat=(0.2, 0.3), fiber=(3.5, 3.5)), "Japan's Standard Tables of Food Composition, kabocha (seiyo kabocha), raw. USDA's generic winter squash (~35-45 kcal) understates this denser squash"),
    "sweet potato":    (None, dict(kcal=(86, 86), protein=(1.6, 1.6), carbs=(20.1, 20.1), fat=(0.1, 0.1), fiber=(3, 3)), "USDA: sweet potato, raw"),
    "red bell pepper": (None, dict(kcal=(31, 31), protein=(1, 1), carbs=(6, 6), fat=(0.3, 0.3), fiber=(2.1, 2.1)), "USDA: red bell pepper, raw"),
    "medjool date":    (24, dict(kcal=(66, 67), protein=(0.4, 0.4), carbs=(18, 18), fat=(0, 0), fiber=(1.6, 1.6)), "USDA: Medjool date, per date"),
    "pomegranate seeds": (None, dict(kcal=(83, 83), protein=(1.7, 1.7), carbs=(18.7, 18.7), fat=(1.2, 1.2), fiber=(4, 4)), "USDA: pomegranate, raw"),
    "arugula":         (None, dict(kcal=(25, 25), protein=(2.6, 2.6), carbs=(3.7, 3.7), fat=(0.7, 0.7), fiber=(1.6, 1.6)), "USDA: arugula, raw"),
    "ajvar":           (None, dict(kcal=(160, 220), protein=(1, 1.3), carbs=(8, 10), fat=(13, 19), fiber=(2.5, 3)), "Calculated from the October jar recipe (peppers cooked down with oil); yield varies"),
    "lemon or lime":   (None, dict(kcal=(25, 30), protein=(0.4, 0.6), carbs=(8, 10), fat=(0.2, 0.3), fiber=(0, 0.3)), "USDA: juice"),
}

TBSP_OIL = 13.5
TBSP_BUTTER = 14.2

# Each dish: servings in the recipe, the serving definition shown to readers,
# what's not included, and ingredient amounts in grams for the WHOLE recipe.
# Amounts are (low_g, high_g) where the recipe allows a range.
OCTOBER = {
    "rockfish-tacos": dict(
        servings=2, serving="Half the recipe: three tacos (six tortillas), half the fish, ¼ cup yogurt.",
        excludes="Nothing — the recipe is the whole meal.",
        items=[("rockfish", 454), ("corn tortilla", 12 * 26), ("greek yogurt 2%", 113), ("pomegranate seeds", 85),
               ("arugula", 40), ("olive oil", (0.5 * TBSP_OIL, 1 * TBSP_OIL)), ("lemon or lime", 30)]),
    "seared-rockfish-brown-butter": dict(
        servings=2, serving="Half the recipe: one fillet, half the squash and salad.",
        excludes="Ajvar at the table; no bread or rice.",
        items=[("rockfish", 454), ("kabocha", (500, 650)), ("olive oil", (1.5 * TBSP_OIL, 2 * TBSP_OIL)), ("butter", (2 * TBSP_BUTTER, 3 * TBSP_BUTTER)),
               ("olive oil", (0.5 * TBSP_OIL, 1 * TBSP_OIL)), ("arugula", 80), ("pomegranate seeds", 85),
               ("medjool date", 4 * 24), ("feta", 28), ("olive oil", 2 * TBSP_OIL), ("lemon or lime", 30)]),
    "fish-in-parchment": dict(
        servings=2, serving="One packet with 1 cup cooked rice and half the salad.",
        excludes="Nothing beyond the 1 cup of rice.",
        items=[("firm white fish", 454), ("ajvar", 2 * 22), ("olive oil", 2 * TBSP_OIL), ("arugula", 40),
               ("pomegranate seeds", 85), ("medjool date", 3 * 24), ("olive oil", 1 * TBSP_OIL),
               ("rice, cooked", 2 * 158), ("lemon or lime", 25)]),
    "pork-tenderloin-date-relish": dict(
        servings=3, serving="A third of the recipe: about 6 oz pork, sweet potatoes and peppers, relish, arugula.",
        excludes="Rice. The lunches go over 1 cup cooked rice: add about 200 kcal and 45 g carbohydrate.",
        items=[("pork tenderloin", 567), ("sweet potato", (300, 360)), ("red bell pepper", 120), ("olive oil", (1.5 * TBSP_OIL, 2 * TBSP_OIL)),
               ("medjool date", 6 * 24), ("feta", 57), ("olive oil", 3 * TBSP_OIL), ("lemon or lime", 45), ("arugula", 40)]),
    "sausages-peppers-ajvar": dict(
        servings=2, serving="Half the recipe: two to three sausages, half the squash and peppers, ajvar, and one thick slice of sourdough or 1 cup cooked rice.",
        excludes="Nothing beyond the bread or rice.",
        items=[("chicken sausage", 454), ("kabocha", (500, 650)), ("red bell pepper", 240), ("olive oil", 2 * TBSP_OIL),
               ("ajvar", (3 * 22, 4 * 22)), ("sourdough", (2 * 60, 2 * 75))]),
    "ajvar-egg-toast": dict(
        servings=1, serving="The whole recipe: two eggs on two thick slices of sourdough.",
        excludes="Nothing.",
        items=[("sourdough", (120, 150)), ("olive oil", (1.5 * TBSP_OIL, 2 * TBSP_OIL)), ("egg", 2 * 50),
               ("ajvar", (2 * 22, 3 * 22)), ("arugula", 20), ("olive oil", 0.5 * TBSP_OIL)]),
    "sweet-potatoes-black-beans": dict(
        servings=2, serving="Half the recipe: two baked sweet potatoes, half the beans, ¼ cup yogurt, feta, ajvar.",
        excludes="Nothing.",
        items=[("sweet potato", (600, 720)), ("olive oil", 4 * 4.5), ("black beans", 250), ("ajvar", (3 * 22, 4 * 22)),
               ("greek yogurt 2%", 113), ("feta", 28), ("lemon or lime", 30)]),
    "orzo-salad": dict(
        servings=3, serving="A lunch: a third of the salad, with a handful of arugula and pomegranate. As one of five snack bowls, about 60% of these numbers.",
        excludes="Nothing.",
        items=[("orzo, dry", 227), ("kabocha", (500, 650)), ("olive oil", (1 * TBSP_OIL, 1.5 * TBSP_OIL)), ("feta", 85),
               ("olive oil", 0.33 * 236 * 0.91), ("lemon or lime", 20), ("arugula", 60), ("pomegranate seeds", 85)]),
}

# Optional "Make it a meal" pairings, as extra items for ONE serving.
PAIRINGS = {
    "ajvar-egg-toast": [("egg", 50), ("greek yogurt 2%", 57)],
    "sweet-potatoes-black-beans": [("egg", 100), ("olive oil", 0.5 * TBSP_OIL)],
    "orzo-salad": [("egg", 100), ("feta", 14)],
}

NUTRIENTS = ["kcal", "protein", "carbs", "fat", "fiber"]


def amount(a):
    return a if isinstance(a, tuple) else (a, a)


def add(items):
    tot = {n: [0.0, 0.0] for n in NUTRIENTS}
    rows = []
    for name, amt in items:
        unit, vals, _ = DB[name]
        lo_g, hi_g = amount(amt)
        r = {}
        for n in NUTRIENTS:
            lo_v, hi_v = vals[n]
            if unit:  # per-unit values: convert grams to units
                lo, hi = lo_g / unit * lo_v, hi_g / unit * hi_v
            else:
                lo, hi = lo_g / 100 * lo_v, hi_g / 100 * hi_v
            tot[n][0] += lo
            tot[n][1] += hi
            r[n] = (lo, hi)
        rows.append((name, lo_g, hi_g, r))
    return tot, rows


def rnd(x, step):
    return int(step * round(x / step))


def display(lo, hi, step):
    a, b = rnd(lo, step), rnd(hi, step)
    return (a, b)


def main(month):
    if month != "october":
        sys.exit("Only October is entered so far.")
    out = ["# October — nutrition worksheet", "",
           "Per-serving estimates from the ingredient amounts in each recipe. Low/high values carry the real uncertainty "
           "(fish species, sausage brand, kabocha's density, how much frying fat stays in the pan). Rounded to the nearest "
           "50 kcal and 5 g before publishing. These are estimates, not lab measurements.", ""]
    summary = {}
    for slug, d in OCTOBER.items():
        tot, rows = add(d["items"])
        s = d["servings"]
        per = {n: (tot[n][0] / s, tot[n][1] / s) for n in NUTRIENTS}
        shown = {"kcal": display(*per["kcal"], 50)}
        for n in ["protein", "carbs", "fat", "fiber"]:
            shown[n] = display(*per[n], 5)
        summary[slug] = dict(shown=shown, serving=d["serving"], excludes=d["excludes"])
        out += [f"## {slug}", "", f"Recipe makes {s} serving(s). **Serving:** {d['serving']}  ", f"**Not included:** {d['excludes']}", "",
                "| Ingredient (whole recipe) | grams | kcal | protein | carbs | fat | fiber |", "|---|---|---|---|---|---|---|"]
        for name, lo_g, hi_g, r in rows:
            g = f"{lo_g:.0f}" if lo_g == hi_g else f"{lo_g:.0f}–{hi_g:.0f}"
            cells = [f"{r[n][0]:.0f}" if abs(r[n][0] - r[n][1]) < 0.5 else f"{r[n][0]:.0f}–{r[n][1]:.0f}" for n in NUTRIENTS]
            out.append(f"| {name} | {g} | " + " | ".join(cells) + " |")
        out.append("| **Per serving** | | " + " | ".join(f"**{per[n][0]:.0f}–{per[n][1]:.0f}**" for n in NUTRIENTS) + " |")
        out.append("| *Published (rounded)* | | " + " | ".join(f"{shown[n][0]}–{shown[n][1]}" if shown[n][0] != shown[n][1] else f"{shown[n][0]}" for n in NUTRIENTS) + " |")
        if slug in PAIRINGS:
            ptot, _ = add(PAIRINGS[slug])
            wk = display(per["kcal"][0] + ptot["kcal"][0], per["kcal"][1] + ptot["kcal"][1], 50)
            wp = display(per["protein"][0] + ptot["protein"][0], per["protein"][1] + ptot["protein"][1], 5)
            summary[slug]["pairing"] = {"kcal": wk, "protein": wp}
            out.append(f"\nWith the \"Make it a meal\" pairing ({', '.join(n for n, _ in PAIRINGS[slug])}): about {wk[0]}–{wk[1]} kcal, {wp[0]}–{wp[1]} g protein.")
        out.append("")
    out += ["## Ingredient values used", "", "| Ingredient | basis | kcal | protein | carbs | fat | fiber | source |", "|---|---|---|---|---|---|---|---|"]
    for name, (unit, vals, src) in DB.items():
        basis = f"per {unit} g unit" if unit else "per 100 g"
        cells = [f"{vals[n][0]}" if vals[n][0] == vals[n][1] else f"{vals[n][0]}–{vals[n][1]}" for n in NUTRIENTS]
        out.append(f"| {name} | {basis} | " + " | ".join(cells) + f" | {src} |")
    Path(f"editions/{month}/NUTRITION.md").write_text("\n".join(out) + "\n")
    import json
    print(json.dumps(summary, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "october")
