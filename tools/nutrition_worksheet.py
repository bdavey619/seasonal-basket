"""
Seasonal — nutrition worksheet.

Editorial tool, not part of the build. For each dish it adds up per-serving
estimates from the ingredient amounts written in the recipe, using low/high
values per ingredient so uncertainty (fish choice, sausage brand, how much
frying oil is eaten) shows up as a range instead of false precision.

Run:  python3 tools/nutrition_worksheet.py <month>   (october, november)
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
    "yellowtail":      (None, dict(kcal=(146, 146), protein=(23.1, 23.1), carbs=(0, 0), fat=(5.2, 5.2), fiber=(0, 0)), "USDA: yellowtail, mixed species, raw"),
    "salmon, wild":    (None, dict(kcal=(131, 146), protein=(21.6, 22.3), carbs=(0, 0), fat=(4.7, 5.9), fiber=(0, 0)), "USDA: sockeye to coho salmon, wild, raw"),
    "salmon, farmed":  (None, dict(kcal=(208, 208), protein=(20.4, 20.4), carbs=(0, 0), fat=(13.4, 13.4), fiber=(0, 0)), "USDA: Atlantic salmon, farmed, raw"),
    "kale":            (None, dict(kcal=(35, 43), protein=(2.9, 2.9), carbs=(4.4, 4.4), fat=(0.5, 1.5), fiber=(4.1, 4.1)), "USDA: kale, raw (leaves)"),
    "chickpeas":       (None, dict(kcal=(138, 139), protein=(7, 7), carbs=(22.5, 22.5), fat=(2.8, 2.8), fiber=(6.4, 6.4)), "USDA: chickpeas, canned, drained"),
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
    "chicken thigh":   (None, dict(kcal=(190, 221), protein=(16.5, 17.1), carbs=(0, 0.3), fat=(13.3, 16.6), fiber=(0, 0)), "USDA: chicken thigh, meat and skin, raw (enter edible weight: about 70% of bone-in weight)"),
    "beef chuck":      (None, dict(kcal=(180, 250), protein=(18.5, 20), carbs=(0, 0), fat=(10, 19), fiber=(0, 0)), "USDA: beef chuck, lean and fat, raw (wide range: trim varies)"),
    "halibut":         (None, dict(kcal=(85, 91), protein=(17.7, 18.6), carbs=(0, 0), fat=(1, 1.5), fiber=(0, 0)), "USDA: halibut, Atlantic and Pacific, raw; lingcod and rockfish are about the same"),
    "leeks":           (None, dict(kcal=(61, 61), protein=(1.5, 1.5), carbs=(14.2, 14.2), fat=(0.3, 0.3), fiber=(1.8, 1.8)), "USDA: leeks, bulb and lower leaf, raw"),
    "fennel":          (None, dict(kcal=(31, 31), protein=(1.2, 1.2), carbs=(7.3, 7.3), fat=(0.2, 0.2), fiber=(3.1, 3.1)), "USDA: fennel bulb, raw"),
    "chard":           (None, dict(kcal=(19, 20), protein=(1.8, 1.9), carbs=(3.7, 4.1), fat=(0.1, 0.2), fiber=(1.6, 1.6)), "USDA: Swiss chard, raw"),
    "cauliflower":     (None, dict(kcal=(25, 25), protein=(1.9, 1.9), carbs=(5, 5), fat=(0.3, 0.3), fiber=(2, 2)), "USDA: cauliflower, raw"),
    "fuyu persimmon":  (None, dict(kcal=(70, 70), protein=(0.6, 0.6), carbs=(18.6, 18.6), fat=(0.2, 0.2), fiber=(3.6, 3.6)), "USDA: persimmon, Japanese, raw"),
    "satsuma":         (None, dict(kcal=(53, 53), protein=(0.8, 0.8), carbs=(13.3, 13.3), fat=(0.3, 0.3), fiber=(1.8, 1.8)), "USDA: tangerines (mandarin oranges), raw"),
    "lentils, dry":    (None, dict(kcal=(352, 352), protein=(24.6, 25.8), carbs=(63, 63), fat=(1.1, 1.1), fiber=(10.7, 10.7)), "USDA: lentils, raw (French green are similar)"),
    "white beans":     (None, dict(kcal=(114, 125), protein=(7.4, 7.6), carbs=(21, 22), fat=(0.4, 0.5), fiber=(5, 6.3)), "USDA: white / great northern beans, canned, drained"),
    "pasta, dry":      (None, dict(kcal=(357, 371), protein=(12.5, 13.6), carbs=(71, 75), fat=(1.2, 1.5), fiber=(2.5, 3.5)), "USDA: pasta, dry, enriched"),
    "parmesan":        (None, dict(kcal=(392, 392), protein=(35.8, 35.8), carbs=(3.2, 3.2), fat=(25.8, 25.8), fiber=(0, 0)), "USDA: Parmesan, hard"),
    "chicken stock":   (None, dict(kcal=(4, 15), protein=(0.5, 1.5), carbs=(0.3, 1), fat=(0, 0.5), fiber=(0, 0)), "USDA / labels: chicken stock, ready to use"),
    "pickled fennel":  (None, dict(kcal=(25, 35), protein=(1, 1.2), carbs=(6, 8), fat=(0.2, 0.2), fiber=(2.5, 3)), "Calculated from the November jar: fennel in a vinegar brine (the brine adds almost nothing)"),
    "italian sausage": (None, dict(kcal=(290, 346), protein=(13.9, 14.3), carbs=(0.6, 3), fat=(24.3, 31), fiber=(0, 0)), "USDA: Italian sausage, pork, raw (mild entry to the more common figure)"),
    "flat iron":       (None, dict(kcal=(170, 210), protein=(19, 20.5), carbs=(0, 0), fat=(9, 14), fiber=(0, 0)), "USDA: beef chuck, top blade (flat iron), lean and fat, raw (estimate)"),
    "farro, dry":      (None, dict(kcal=(340, 378), protein=(12, 15), carbs=(67, 75), fat=(2, 2.5), fiber=(7, 11)), "Labels: whole / semi-pearled farro, dry"),
    "carrots":         (None, dict(kcal=(41, 41), protein=(0.9, 0.9), carbs=(9.6, 9.6), fat=(0.2, 0.2), fiber=(2.8, 2.8)), "USDA: carrots, raw"),
    "canned tomatoes": (None, dict(kcal=(18, 21), protein=(0.8, 1), carbs=(4, 4.5), fat=(0.1, 0.3), fiber=(1, 1.9)), "USDA: tomatoes, canned, whole, with juice"),
    "fat poured off":  (None, dict(kcal=(884, 884), protein=(0, 0), carbs=(0, 0), fat=(100, 100), fiber=(0, 0)), "Rendered fat poured out of the pan (entered as a negative amount)"),
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
        # The fish is whatever's best at the market; each choice is estimated on its own.
        variants={"Local yellowtail": "yellowtail", "Wild salmon": "salmon, wild", "Farmed salmon": "salmon, farmed"},
        items=[("rich fish", 454), ("ajvar", 2 * 22), ("olive oil", 2 * TBSP_OIL), ("arugula", 40),
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
        # Checked: 1 lb sausage is ~5⅓ links at 160–190 kcal each (labels), so half the pan is ~430–510 kcal
        # of sausage alone; half a 3-lb kabocha (500–650 g usable) split two ways. The pan's 2 tbsp oil is
        # counted once; the ajvar includes its own oil; the bread is one slice per serving (or 1 cup rice,
        # about the same). Rendered sausage fat left on the pan isn't subtracted, so the top of the range is generous.
        # Half a bunch of lacinato kale is ~75–100 g of leaves once the ribs are stripped, with 1 tsp oil.
        items=[("chicken sausage", 454), ("kabocha", (500, 650)), ("red bell pepper", 240), ("olive oil", 2 * TBSP_OIL),
               ("ajvar", (3 * 22, 4 * 22)), ("sourdough", (2 * 60, 2 * 75)), ("kale", (75, 100)), ("olive oil", 4.5)]),
    "ajvar-egg-toast": dict(
        servings=1, serving="The whole recipe: two eggs on two thick slices of sourdough.",
        excludes="Nothing.",
        # 2 tbsp oil go in the pan once: the bread soaks up most of it and the eggs fry
        # in what's left, so count 1¼–1¾ tbsp eaten, not 2 for the bread plus more for the eggs.
        # The ajvar value already includes the jar's own oil; the ½ tbsp is the arugula's dressing.
        items=[("sourdough", (120, 150)), ("olive oil", (1.25 * TBSP_OIL, 1.75 * TBSP_OIL)), ("egg", 2 * 50),
               ("ajvar", (2 * 22, 3 * 22)), ("arugula", 20), ("olive oil", 0.5 * TBSP_OIL)]),
    "sweet-potatoes-black-beans": dict(
        servings=2, serving="Half the recipe: two baked sweet potatoes, half the beans, ¼ cup yogurt, feta, ajvar.",
        excludes="Nothing.",
        items=[("sweet potato", (600, 720)), ("olive oil", 4 * 4.5), ("black beans", 250), ("ajvar", (3 * 22, 4 * 22)),
               ("greek yogurt 2%", 113), ("feta", 28), ("lemon or lime", 30)]),
    "orzo-salad": dict(
        servings=4, serving="A lunch: a quarter of the salad, with pomegranate on top. As one of six snack bowls, about two-thirds of these numbers.",
        excludes="Nothing.",
        # One bunch of lacinato kale is ~150–200 g of leaves; one can of chickpeas is ~240–255 g drained.
        items=[("orzo, dry", 227), ("kabocha", (500, 650)), ("olive oil", (1 * TBSP_OIL, 1.5 * TBSP_OIL)), ("feta", 85),
               ("olive oil", 0.33 * 236 * 0.91), ("lemon or lime", 20), ("kale", (150, 200)), ("chickpeas", (240, 255)),
               ("pomegranate seeds", 85)]),
}

# Optional "Make it a meal" pairings, as extra items for ONE serving.
PAIRINGS_OCTOBER = {
    "ajvar-egg-toast": [("egg", 50), ("greek yogurt 2%", 57)],
    "sweet-potatoes-black-beans": [("egg", 100), ("olive oil", 0.5 * TBSP_OIL)],
    "orzo-salad": [("egg", 100), ("feta", 14)],
}

# Bone-in thighs: about 70% of the weight is meat and skin you eat (USDA yield).
THIGH_EDIBLE = 0.70
NOVEMBER = {
    "braised-chicken-leeks-fennel": dict(
        servings=3, serving="A third of the recipe: two thighs with leeks, fennel, and juices, and 1 cup cooked rice or a thick slice of sourdough.",
        excludes="Nothing beyond the rice or bread.",
        # Rendered fat is poured off before the vegetables go in; the thighs still keep their skin.
        items=[("chicken thigh", (1135 * THIGH_EDIBLE, 1360 * THIGH_EDIBLE)), ("leeks", (180, 240)), ("fennel", (200, 280)),
               ("satsuma", 150), ("chicken stock", 355), ("olive oil", (0.5 * TBSP_OIL, 1 * TBSP_OIL)), ("rice, cooked", 3 * 158)]),
    "chicken-white-beans-chard": dict(
        servings=2, serving="Half the recipe: two thighs over half the beans and chard, and a thick slice of sourdough.",
        excludes="Nothing beyond the bread.",
        # Rendered fat is poured off down to a tablespoon before the beans go in.
        items=[("chicken thigh", 795 * THIGH_EDIBLE), ("white beans", (240, 255)), ("chard", (150, 200)), ("chicken stock", 237),
               ("satsuma", 75), ("olive oil", (0.5 * TBSP_OIL, 1 * TBSP_OIL)), ("pickled fennel", 60), ("sourdough", (120, 150))]),
    "beef-white-bean-chard-soup": dict(
        servings=6, serving="One of six big bowls (about 2 cups), with a little grated Parmesan.",
        excludes="Bread.",
        items=[("beef chuck", 1135), ("leeks", (180, 240)), ("chard", (300, 400)), ("white beans", (480, 510)),
               ("chicken stock", 946), ("olive oil", 2 * TBSP_OIL), ("parmesan", (30, 45)), ("lemon or lime", 30)]),
    "minestrone-sausage": dict(
        servings=6, serving="One of six big bowls (about 2 cups), with a little grated Parmesan.",
        excludes="Bread.",
        # Sausage fat stays in the pot to cook the vegetables.
        items=[("italian sausage", 340), ("leeks", (180, 240)), ("fennel", (200, 280)), ("carrots", (120, 150)), ("chard", (300, 400)),
               ("canned tomatoes", 794), ("white beans", (480, 510)), ("chicken stock", 946), ("pasta, dry", (170, 180)),
               ("olive oil", 2 * TBSP_OIL), ("parmesan", (30, 45))]),
    "seared-halibut-persimmon": dict(
        servings=2, serving="One fillet with half the salad and 1 cup cooked rice.",
        excludes="Nothing beyond the rice.",
        items=[("halibut", 454), ("fuyu persimmon", (280, 340)), ("fennel", (200, 280)), ("parmesan", 28),
               ("olive oil", 3 * TBSP_OIL), ("lemon or lime", 30), ("rice, cooked", 2 * 158)]),
    "salmon-lentils-cauliflower": dict(
        servings=2, serving="Half the recipe: one piece of salmon over half the lentils and cauliflower.",
        excludes="Nothing.",
        variants={"Wild salmon": "salmon, wild", "Farmed salmon": "salmon, farmed"},
        # ¾ cup dry French green lentils is about 140–150 g.
        items=[("rich fish", 454), ("lentils, dry", (140, 150)), ("cauliflower", (550, 700)), ("pickled fennel", 60),
               ("olive oil", 4 * TBSP_OIL), ("parmesan", (15, 20))]),
    "orecchiette-sausage-chard": dict(
        servings=2, serving="Half the recipe: about 4 oz dry pasta with 6 oz sausage, leeks, chard, and Parmesan.",
        excludes="Nothing.",
        # ¾ lb sausage; most rendered fat is poured off, so the low end uses the leaner USDA entry
        # and the high end counts it all.
        # ¾ lb sausage is ~90 g of fat; about a third to a half renders, and all but a tablespoon is poured off.
        items=[("fat poured off", (-33, -15)), ("pasta, dry", 227), ("italian sausage", 340), ("leeks", (180, 240)), ("chard", (300, 400)),
               ("butter", 1 * TBSP_BUTTER), ("parmesan", 57), ("lemon or lime", 15)]),
    "flat-iron-steak-leeks": dict(
        servings=2, serving="Half the steak with half the leeks and 1 cup cooked farro.",
        excludes="Nothing beyond the farro (rice is about the same).",
        # 1 cup cooked farro is about 50 g dry.
        items=[("flat iron", 567), ("leeks", (180, 240)), ("butter", 1 * TBSP_BUTTER), ("olive oil", (0.5 * TBSP_OIL, 1 * TBSP_OIL)),
               ("pickled fennel", 60), ("farro, dry", (95, 105))]),
    "farro-braised-chicken-bowls": dict(
        servings=2, serving="Half the recipe: two braised thighs with their leeks and juices, about 1 cup cooked farro, chard, and Parmesan.",
        excludes="Nothing. These are the braise's leftovers, so don't count them twice.",
        # Two thirds of the braise (four of six thighs, and their share of the pot), without its rice.
        items=[("chicken thigh", (1135 * THIGH_EDIBLE * 2 / 3, 1360 * THIGH_EDIBLE * 2 / 3)), ("leeks", (120, 160)), ("fennel", (130, 190)),
               ("satsuma", 100), ("chicken stock", 237), ("olive oil", (0.33 * TBSP_OIL, 0.67 * TBSP_OIL)),
               ("farro, dry", (140, 150)), ("chard", (150, 200)), ("pickled fennel", 60), ("parmesan", (15, 20)), ("lemon or lime", 15)]),
}
PAIRINGS_NOVEMBER = {
    "minestrone-sausage": [("egg", 50), ("sourdough", (60, 75)), ("parmesan", 10)],
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
    if month not in MONTHS:
        sys.exit(f"No worksheet entered for {month}. Known: {', '.join(MONTHS)}")
    DISHES, PAIRINGS = MONTHS[month]
    out = [f"# {month.capitalize()} — nutrition worksheet", "",
           "Per-serving estimates from the ingredient amounts in each recipe. Low/high values carry the real uncertainty "
           "(fish choice, sausage brand, kabocha's density, how much frying fat stays in the pan). Rounded to the nearest "
           "50 kcal and 5 g before publishing. These are estimates, not lab measurements.", ""]
    summary = {}
    for slug, d in DISHES.items():
        s = d["servings"]
        variant_rows = []
        if d.get("variants"):
            # Estimate each fish on its own; the overall range spans all of them.
            per = {n: [float("inf"), 0.0] for n in NUTRIENTS}
            for label, fish in d["variants"].items():
                vtot, _ = add([(fish if name == "rich fish" else name, amt) for name, amt in d["items"]])
                vper = {n: (vtot[n][0] / s, vtot[n][1] / s) for n in NUTRIENTS}
                for n in NUTRIENTS:
                    per[n][0] = min(per[n][0], vper[n][0]); per[n][1] = max(per[n][1], vper[n][1])
                variant_rows.append(dict(label=label, kcal=display(*vper["kcal"], 50),
                                         **{n: display(*vper[n], 5) for n in ["protein", "carbs", "fat"]}))
            per = {n: tuple(per[n]) for n in NUTRIENTS}
            first = next(iter(d["variants"].values()))
            tot, rows = add([(first if name == "rich fish" else name, amt) for name, amt in d["items"]])
        else:
            tot, rows = add(d["items"])
            per = {n: (tot[n][0] / s, tot[n][1] / s) for n in NUTRIENTS}
        shown = {"kcal": display(*per["kcal"], 50)}
        for n in ["protein", "carbs", "fat", "fiber"]:
            shown[n] = display(*per[n], 5)
        summary[slug] = dict(shown=shown, serving=d["serving"], excludes=d["excludes"])
        if variant_rows:
            summary[slug]["variants"] = variant_rows
        out += [f"## {slug}", "", f"Recipe makes {s} serving(s). **Serving:** {d['serving']}  ", f"**Not included:** {d['excludes']}", "",
                "| Ingredient (whole recipe) | grams | kcal | protein | carbs | fat | fiber |", "|---|---|---|---|---|---|---|"]
        for name, lo_g, hi_g, r in rows:
            g = f"{lo_g:.0f}" if lo_g == hi_g else f"{lo_g:.0f}–{hi_g:.0f}"
            cells = [f"{r[n][0]:.0f}" if abs(r[n][0] - r[n][1]) < 0.5 else f"{r[n][0]:.0f}–{r[n][1]:.0f}" for n in NUTRIENTS]
            out.append(f"| {name} | {g} | " + " | ".join(cells) + " |")
        out.append("| **Per serving** | | " + " | ".join(f"**{per[n][0]:.0f}–{per[n][1]:.0f}**" for n in NUTRIENTS) + " |")
        if variant_rows:
            out.append(f"| *(rows above use {next(iter(d['variants']))})* | | | | | | |")
            for v in variant_rows:
                out.append(f"| **{v['label']}, per serving** | | {v['kcal'][0]}–{v['kcal'][1]} | {v['protein'][0]}–{v['protein'][1]} | "
                           f"{v['carbs'][0]}–{v['carbs'][1]} | {v['fat'][0]}–{v['fat'][1]} | |")
        out.append("| *Published (rounded)* | | " + " | ".join(f"{shown[n][0]}–{shown[n][1]}" if shown[n][0] != shown[n][1] else f"{shown[n][0]}" for n in NUTRIENTS) + " |")
        if slug in PAIRINGS:
            ptot, _ = add(PAIRINGS[slug])
            wk = display(per["kcal"][0] + ptot["kcal"][0], per["kcal"][1] + ptot["kcal"][1], 50)
            wp = display(per["protein"][0] + ptot["protein"][0], per["protein"][1] + ptot["protein"][1], 5)
            summary[slug]["pairing"] = {"kcal": wk, "protein": wp}
            out.append(f"\nWith the \"Make it a meal\" pairing ({', '.join(n for n, _ in PAIRINGS[slug])}): about {wk[0]}–{wk[1]} kcal, {wp[0]}–{wp[1]} g protein.")
        out.append("")
    out += ["## Ingredient values used", "", "| Ingredient | basis | kcal | protein | carbs | fat | fiber | source |", "|---|---|---|---|---|---|---|---|"]
    used = set()
    for d in DISHES.values():
        used.update(name for name, _ in d["items"])
        used.update(d.get("variants", {}).values())
    for items in PAIRINGS.values():
        used.update(name for name, _ in items)
    for name, (unit, vals, src) in DB.items():
        if name not in used:
            continue
        basis = f"per {unit} g unit" if unit else "per 100 g"
        cells = [f"{vals[n][0]}" if vals[n][0] == vals[n][1] else f"{vals[n][0]}–{vals[n][1]}" for n in NUTRIENTS]
        out.append(f"| {name} | {basis} | " + " | ".join(cells) + f" | {src} |")
    Path(f"editions/{month}/NUTRITION.md").write_text("\n".join(out) + "\n")
    import json
    print(json.dumps(summary, indent=1, ensure_ascii=False))


MONTHS = {"october": (OCTOBER, PAIRINGS_OCTOBER), "november": (NOVEMBER, PAIRINGS_NOVEMBER)}


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "october")
