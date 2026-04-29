import math
import os
import random
from fractions import Fraction

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "tutoring-with-sehaj-dev-secret")


# -------------------- TOPIC OF THE WEEK --------------------
TOPIC_OF_THE_WEEK = {
    "title": "Pressure: Why area changes everything",
    "body": (
        "This week we explore why a sharp knife cuts so easily, why snowshoes "
        "stop you from sinking, and why heavy tractors have wide tires. The "
        "secret formula behind all of it is P = F ÷ A."
    ),
    "tip": "Try the 'Pressure Concepts' quiz and the 'Science: Pressure' memory game!",
}


@app.route("/")
def home():
    return render_template("home.html", topic=TOPIC_OF_THE_WEEK)


# -------------------- MEMORY GAME --------------------

MEMORY_THEMES = {
    "symbols": {
        "name": "Math Symbols",
        "description": "Match each symbol with its name.",
        "pairs": [
            ("+", "Addition"),
            ("−", "Subtraction"),
            ("×", "Multiplication"),
            ("÷", "Division"),
            ("=", "Equals"),
            ("π", "Pi"),
            ("√", "Square Root"),
            ("%", "Percent"),
        ],
    },
    "formulas": {
        "name": "Math Formulas",
        "description": "Match each shape with its formula.",
        "pairs": [
            ("Area of Circle", "π × r²"),
            ("Circumference", "2 × π × r"),
            ("Area of Rectangle", "length × width"),
            ("Area of Triangle", "½ × base × height"),
            ("Volume of Cube", "side³"),
            ("Volume of Cylinder", "π × r² × h"),
            ("Perimeter of Rectangle", "2 × (l + w)"),
            ("Surface Area of Cube", "6 × side²"),
        ],
    },
    "science": {
        "name": "Science: Pressure",
        "description": "Match each science quantity with its formula or unit.",
        "pairs": [
            ("Pressure", "Force ÷ Area"),
            ("Force", "Pressure × Area"),
            ("Area", "Force ÷ Pressure"),
            ("Pressure Unit", "Pascal (Pa)"),
            ("Force Unit", "Newton (N)"),
            ("Area Unit", "m²"),
            ("High Pressure", "Small Area"),
            ("Low Pressure", "Large Area"),
        ],
    },
}


@app.route("/memory")
def memory_game():
    theme_key = request.args.get("theme", "symbols")
    if theme_key not in MEMORY_THEMES:
        theme_key = "symbols"
    try:
        pairs_count = int(request.args.get("pairs", "6"))
    except ValueError:
        pairs_count = 6
    pairs_count = max(4, min(8, pairs_count))

    theme = MEMORY_THEMES[theme_key]
    available = list(theme["pairs"])
    random.shuffle(available)
    selected = available[:pairs_count]

    cards = []
    for idx, (a, b) in enumerate(selected):
        cards.append({"pair_id": idx, "text": a})
        cards.append({"pair_id": idx, "text": b})
    random.shuffle(cards)

    return render_template(
        "memory.html",
        cards=cards,
        themes=MEMORY_THEMES,
        current_theme=theme_key,
        current_theme_name=theme["name"],
        current_description=theme["description"],
        pairs_count=pairs_count,
        total_pairs=len(selected),
    )


# -------------------- CALCULATORS --------------------

CALCULATORS = {
    "cylinder": {
        "title": "Volume of a Cylinder",
        "formula": "V = π × r² × h",
        "fields": [("radius", "Radius"), ("height", "Height")],
    },
    "cylinder-surface": {
        "title": "Surface Area of a Cylinder",
        "formula": "A = 2π × r × (r + h)",
        "fields": [("radius", "Radius"), ("height", "Height")],
    },
    "cube-volume": {
        "title": "Volume of a Cube",
        "formula": "V = side³",
        "fields": [("side", "Side")],
    },
    "cube-surface": {
        "title": "Surface Area of a Cube",
        "formula": "A = 6 × side²",
        "fields": [("side", "Side")],
    },
    "rectangular-prism": {
        "title": "Volume of a Rectangular Prism",
        "formula": "V = length × width × height",
        "fields": [("length", "Length"), ("width", "Width"), ("height", "Height")],
    },
    "rectangular-prism-surface": {
        "title": "Surface Area of a Rectangular Prism",
        "formula": "A = 2 × (lw + wh + lh)",
        "fields": [("length", "Length"), ("width", "Width"), ("height", "Height")],
    },
    "triangular-prism": {
        "title": "Volume of a Triangular Prism",
        "formula": "V = ½ × base × triangle height × prism length",
        "fields": [
            ("base", "Triangle Base"),
            ("triangle_height", "Triangle Height"),
            ("length", "Prism Length"),
        ],
    },
    "area-rectangle": {
        "title": "Area of a Rectangle",
        "formula": "A = length × width",
        "fields": [("length", "Length"), ("width", "Width")],
    },
    "perimeter-rectangle": {
        "title": "Perimeter of a Rectangle",
        "formula": "P = 2 × (length + width)",
        "fields": [("length", "Length"), ("width", "Width")],
    },
    "area-triangle": {
        "title": "Area of a Triangle",
        "formula": "A = ½ × base × height",
        "fields": [("base", "Base"), ("height", "Height")],
    },
    "area-circle": {
        "title": "Area of a Circle",
        "formula": "A = π × r²",
        "fields": [("radius", "Radius")],
    },
    "circumference-circle": {
        "title": "Circumference of a Circle",
        "formula": "C = 2 × π × r",
        "fields": [("radius", "Radius")],
    },
}


def fmt_num(x):
    if isinstance(x, int):
        return str(x)
    if float(x).is_integer():
        return str(int(x))
    return f"{x:.2f}"


def compute_with_steps(slug, v):
    if slug == "cylinder":
        r, h = v["radius"], v["height"]
        result = math.pi * r**2 * h
        steps = [
            "Write the formula: V = π × r² × h",
            f"Substitute r = {fmt_num(r)}, h = {fmt_num(h)}: V = π × {fmt_num(r)}² × {fmt_num(h)}",
            f"Square the radius: V = π × {fmt_num(r * r)} × {fmt_num(h)}",
            f"Multiply: V = π × {fmt_num(r * r * h)}",
            f"Use π ≈ 3.14159: V ≈ {fmt_num(round(result, 2))}",
        ]
        return result, steps

    if slug == "cylinder-surface":
        r, h = v["radius"], v["height"]
        result = 2 * math.pi * r * (r + h)
        steps = [
            "Write the formula: A = 2π × r × (r + h)",
            f"Substitute r = {fmt_num(r)}, h = {fmt_num(h)}: A = 2π × {fmt_num(r)} × ({fmt_num(r)} + {fmt_num(h)})",
            f"Add inside the brackets: A = 2π × {fmt_num(r)} × {fmt_num(r + h)}",
            f"Multiply r × (r + h): A = 2π × {fmt_num(r * (r + h))}",
            f"Use π ≈ 3.14159: A ≈ {fmt_num(round(result, 2))}",
        ]
        return result, steps

    if slug == "cube-volume":
        s = v["side"]
        result = s**3
        steps = [
            "Write the formula: V = side³",
            f"Substitute side = {fmt_num(s)}: V = {fmt_num(s)}³",
            f"Multiply: V = {fmt_num(s)} × {fmt_num(s)} × {fmt_num(s)}",
            f"V = {fmt_num(round(result, 2))}",
        ]
        return result, steps

    if slug == "cube-surface":
        s = v["side"]
        result = 6 * s * s
        steps = [
            "Write the formula: A = 6 × side²",
            f"Substitute side = {fmt_num(s)}: A = 6 × {fmt_num(s)}²",
            f"Square the side: A = 6 × {fmt_num(s * s)}",
            f"Multiply: A = {fmt_num(round(result, 2))}",
        ]
        return result, steps

    if slug == "rectangular-prism":
        l, w, h = v["length"], v["width"], v["height"]
        result = l * w * h
        steps = [
            "Write the formula: V = length × width × height",
            f"Substitute: V = {fmt_num(l)} × {fmt_num(w)} × {fmt_num(h)}",
            f"Multiply length and width first: V = {fmt_num(l * w)} × {fmt_num(h)}",
            f"Multiply by the height: V = {fmt_num(round(result, 2))}",
        ]
        return result, steps

    if slug == "rectangular-prism-surface":
        l, w, h = v["length"], v["width"], v["height"]
        lw, wh, lh = l * w, w * h, l * h
        result = 2 * (lw + wh + lh)
        steps = [
            "Write the formula: A = 2 × (lw + wh + lh)",
            f"Substitute l = {fmt_num(l)}, w = {fmt_num(w)}, h = {fmt_num(h)}",
            f"Find each pair: lw = {fmt_num(lw)}, wh = {fmt_num(wh)}, lh = {fmt_num(lh)}",
            f"Add them: {fmt_num(lw)} + {fmt_num(wh)} + {fmt_num(lh)} = {fmt_num(lw + wh + lh)}",
            f"Multiply by 2: A = {fmt_num(round(result, 2))}",
        ]
        return result, steps

    if slug == "triangular-prism":
        b, th, length = v["base"], v["triangle_height"], v["length"]
        tri_area = 0.5 * b * th
        result = tri_area * length
        steps = [
            "Write the formula: V = ½ × base × triangle height × prism length",
            f"Substitute: V = ½ × {fmt_num(b)} × {fmt_num(th)} × {fmt_num(length)}",
            f"Find the triangle area first: ½ × {fmt_num(b)} × {fmt_num(th)} = {fmt_num(tri_area)}",
            f"Multiply by the prism length: V = {fmt_num(tri_area)} × {fmt_num(length)} = {fmt_num(round(result, 2))}",
        ]
        return result, steps

    if slug == "area-rectangle":
        l, w = v["length"], v["width"]
        result = l * w
        steps = [
            "Write the formula: A = length × width",
            f"Substitute: A = {fmt_num(l)} × {fmt_num(w)}",
            f"Multiply: A = {fmt_num(round(result, 2))}",
        ]
        return result, steps

    if slug == "perimeter-rectangle":
        l, w = v["length"], v["width"]
        result = 2 * (l + w)
        steps = [
            "Write the formula: P = 2 × (length + width)",
            f"Substitute: P = 2 × ({fmt_num(l)} + {fmt_num(w)})",
            f"Add inside the brackets: P = 2 × {fmt_num(l + w)}",
            f"Multiply by 2: P = {fmt_num(round(result, 2))}",
        ]
        return result, steps

    if slug == "area-triangle":
        b, h = v["base"], v["height"]
        result = 0.5 * b * h
        steps = [
            "Write the formula: A = ½ × base × height",
            f"Substitute: A = ½ × {fmt_num(b)} × {fmt_num(h)}",
            f"Multiply base × height first: A = ½ × {fmt_num(b * h)}",
            f"Halve it: A = {fmt_num(round(result, 2))}",
        ]
        return result, steps

    if slug == "area-circle":
        r = v["radius"]
        result = math.pi * r * r
        steps = [
            "Write the formula: A = π × r²",
            f"Substitute r = {fmt_num(r)}: A = π × {fmt_num(r)}²",
            f"Square the radius: A = π × {fmt_num(r * r)}",
            f"Use π ≈ 3.14159: A ≈ {fmt_num(round(result, 2))}",
        ]
        return result, steps

    if slug == "circumference-circle":
        r = v["radius"]
        result = 2 * math.pi * r
        steps = [
            "Write the formula: C = 2 × π × r",
            f"Substitute r = {fmt_num(r)}: C = 2 × π × {fmt_num(r)}",
            f"Multiply 2 × r: C = π × {fmt_num(2 * r)}",
            f"Use π ≈ 3.14159: C ≈ {fmt_num(round(result, 2))}",
        ]
        return result, steps

    return None, []


@app.route("/calculators")
def calculators():
    return render_template("calculators.html", calculators=CALCULATORS)


@app.route("/calculators/<slug>", methods=["GET", "POST"])
def calculator(slug):
    if slug not in CALCULATORS:
        return redirect(url_for("calculators"))

    spec = CALCULATORS[slug]
    inputs = {key: "" for key, _ in spec["fields"]}
    result = None
    steps = None
    error = None

    if request.method == "POST":
        try:
            values = {}
            for key, label in spec["fields"]:
                raw = request.form.get(key, "").strip()
                inputs[key] = raw
                num = float(raw)
                if num < 0:
                    raise ValueError(f"{label} must be non-negative.")
                values[key] = num
            raw_result, steps = compute_with_steps(slug, values)
            result = round(raw_result, 2)
        except ValueError as e:
            error = (
                str(e)
                if str(e) and "could not convert" not in str(e)
                else "Please enter valid non-negative numbers in every field."
            )

    return render_template(
        "calculator.html",
        slug=slug,
        spec=spec,
        inputs=inputs,
        result=result,
        steps=steps,
        error=error,
    )


# -------------------- QUIZ --------------------

QUIZ_TOPICS = {
    "arithmetic": "Arithmetic",
    "fractions": "Fractions",
    "area": "Area",
    "volume": "Volume",
    "pressure": "Pressure, Force & Area (Science)",
    "pressure_concepts": "Pressure Concepts (Word Problems)",
}

QUIZ_LENGTH = 5


def gen_arithmetic(grade):
    if grade <= 2:
        a, b = random.randint(1, 20), random.randint(1, 20)
        op = random.choice(["+", "-"])
    elif grade <= 4:
        a, b = random.randint(2, 50), random.randint(2, 12)
        op = random.choice(["+", "-", "×"])
    elif grade <= 6:
        a, b = random.randint(10, 100), random.randint(2, 12)
        op = random.choice(["+", "-", "×", "÷"])
        if op == "÷":
            a = a * b
    else:
        a = random.randint(-30, 30)
        b = random.randint(-30, 30)
        if b == 0:
            b = 1
        op = random.choice(["+", "-", "×", "÷"])
        if op == "÷":
            a = a * b

    if op == "+":
        ans = a + b
        explanation = f"Add the two numbers: {a} + {b} = {ans}."
    elif op == "-":
        if grade <= 6 and a < b:
            a, b = b, a
        ans = a - b
        explanation = f"Subtract: {a} − {b} = {ans}."
    elif op == "×":
        ans = a * b
        if grade >= 7 and (a < 0) != (b < 0):
            explanation = f"Multiply: {a} × {b} = {ans}. (A positive × a negative gives a negative.)"
        elif grade >= 7 and a < 0 and b < 0:
            explanation = f"Multiply: {a} × {b} = {ans}. (A negative × a negative gives a positive.)"
        else:
            explanation = f"Multiply: {a} × {b} = {ans}."
    else:
        ans = a // b if grade <= 6 else int(a / b)
        explanation = f"Divide: {a} ÷ {b} = {ans} (because {b} × {ans} = {a})."

    def fmt(n):
        return f"({n})" if n < 0 else str(n)

    if grade >= 7:
        question = f"What is {fmt(a)} {op} {fmt(b)}?"
    else:
        question = f"What is {a} {op} {b}?"
    return question, str(ans), explanation


def gen_fractions(grade):
    if grade <= 4:
        d = random.randint(2, 8)
        n1 = random.randint(1, d - 1)
        n2 = random.randint(1, d - 1)
        op = random.choice(["+", "-"])
        d1 = d2 = d
    else:
        d1 = random.randint(2, 10)
        d2 = random.randint(2, 10)
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        op = random.choice(["+", "-", "×"])

    f1 = Fraction(n1, d1)
    f2 = Fraction(n2, d2)

    a_str = f"{f1.numerator}/{f1.denominator}"
    b_str = f"{f2.numerator}/{f2.denominator}"

    if op == "+":
        result = f1 + f2
        if f1.denominator == f2.denominator:
            explanation = (
                f"The denominators are the same, so add only the numerators: "
                f"{f1.numerator} + {f2.numerator} = {f1.numerator + f2.numerator} "
                f"over {f1.denominator}, then simplify."
            )
        else:
            explanation = (
                f"Find a common denominator for {a_str} and {b_str}, "
                f"convert both fractions, then add the numerators. Final answer is shown simplified."
            )
    elif op == "-":
        if f1 < f2:
            f1, f2 = f2, f1
            a_str, b_str = b_str, a_str
        result = f1 - f2
        if f1.denominator == f2.denominator:
            explanation = (
                f"Same denominator — just subtract the numerators: "
                f"{f1.numerator} − {f2.numerator} = {f1.numerator - f2.numerator} "
                f"over {f1.denominator}, then simplify."
            )
        else:
            explanation = (
                f"Find a common denominator, then subtract the numerators. "
                f"Result is shown in simplest form."
            )
    else:
        result = f1 * f2
        explanation = (
            f"For multiplication, multiply across: "
            f"({f1.numerator} × {f2.numerator}) over ({f1.denominator} × {f2.denominator}), "
            f"then simplify."
        )

    question = (
        f"Calculate: {a_str} {op} {b_str} "
        f"(write as a fraction like 3/4 or whole number)"
    )
    if result.denominator == 1:
        answer = str(result.numerator)
    else:
        answer = f"{result.numerator}/{result.denominator}"
    return question, answer, explanation


def gen_area(grade):
    shape = (
        random.choice(["rectangle", "triangle", "square"])
        if grade <= 5
        else random.choice(["rectangle", "triangle", "square", "circle"])
    )

    if shape == "rectangle":
        length = random.randint(2, 20)
        width = random.randint(2, 20)
        ans = length * width
        return (
            f"Find the area of a rectangle with length {length} and width {width}.",
            str(ans),
            f"Area of a rectangle = length × width = {length} × {width} = {ans}.",
        )
    if shape == "square":
        side = random.randint(2, 20)
        ans = side * side
        return (
            f"Find the area of a square with side {side}.",
            str(ans),
            f"A square has all sides equal: A = side × side = {side} × {side} = {ans}.",
        )
    if shape == "triangle":
        base = random.choice([2, 4, 6, 8, 10, 12])
        height = random.randint(2, 15)
        ans = base * height // 2
        return (
            f"Find the area of a triangle with base {base} and height {height}.",
            str(ans),
            f"Area of a triangle = ½ × base × height = ½ × {base} × {height} = {ans}.",
        )
    if shape == "circle":
        r = random.randint(2, 10)
        ans = round(math.pi * r * r, 2)
        return (
            f"Find the area of a circle with radius {r}. "
            f"Use π ≈ 3.14159. Round to 2 decimal places.",
            f"{ans}",
            f"Area of a circle = π × r² = π × {r}² = π × {r * r} ≈ {ans}.",
        )


def gen_volume(grade):
    shape = (
        random.choice(["cube", "rectangular_prism"])
        if grade <= 5
        else random.choice(
            ["cube", "rectangular_prism", "triangular_prism", "cylinder"]
        )
    )

    if shape == "cube":
        side = random.randint(2, 12)
        ans = side**3
        return (
            f"Find the volume of a cube with side {side}.",
            str(ans),
            f"Volume of a cube = side³ = {side} × {side} × {side} = {ans}.",
        )
    if shape == "rectangular_prism":
        l = random.randint(2, 12)
        w = random.randint(2, 12)
        h = random.randint(2, 12)
        ans = l * w * h
        return (
            f"Find the volume of a rectangular prism with length {l}, width {w}, height {h}.",
            str(ans),
            f"Volume = length × width × height = {l} × {w} × {h} = {ans}.",
        )
    if shape == "triangular_prism":
        b = random.choice([2, 4, 6, 8, 10])
        th = random.randint(2, 10)
        length = random.randint(2, 12)
        ans = b * th * length // 2
        return (
            f"Find the volume of a triangular prism with triangle base {b}, "
            f"triangle height {th}, prism length {length}.",
            str(ans),
            f"Find the triangle area first: ½ × {b} × {th} = {b * th // 2}. "
            f"Then multiply by the prism length: {b * th // 2} × {length} = {ans}.",
        )
    if shape == "cylinder":
        r = random.randint(2, 8)
        h = random.randint(2, 12)
        ans = round(math.pi * r * r * h, 2)
        return (
            f"Find the volume of a cylinder with radius {r} and height {h}. "
            f"Use π ≈ 3.14159. Round to 2 decimal places.",
            f"{ans}",
            f"Volume of a cylinder = π × r² × h = π × {r}² × {h} = π × {r * r * h} ≈ {ans}.",
        )


def gen_pressure(grade):
    unknown = random.choice(["pressure", "force", "area"])
    area_options = [2, 4, 5, 8, 10] if grade <= 6 else [2, 4, 5, 8, 10, 12, 20, 25]
    pressure_options = [2, 4, 5, 6, 8, 10] if grade <= 6 else [3, 5, 7, 8, 12, 15, 20]
    area = random.choice(area_options)
    pressure = random.choice(pressure_options)
    force = pressure * area

    if unknown == "pressure":
        question = f"A force of {force} N is applied on a surface of area {area} m². What is the pressure (in Pa)? Use P = F ÷ A."
        answer = str(pressure)
        explanation = f"P = F ÷ A = {force} ÷ {area} = {pressure} Pa."
    elif unknown == "force":
        question = f"The pressure on a surface is {pressure} Pa and the area is {area} m². What is the force (in N)? Use F = P × A."
        answer = str(force)
        explanation = f"F = P × A = {pressure} × {area} = {force} N."
    else:
        question = f"A force of {force} N produces a pressure of {pressure} Pa. What is the area (in m²)? Use A = F ÷ P."
        answer = str(area)
        explanation = f"A = F ÷ P = {force} ÷ {pressure} = {area} m²."

    return question, answer, explanation


PRESSURE_CONCEPT_QUESTIONS = [
    {"q": "Why does a person sink in snow when wearing normal shoes?", "options": [("A", "Because the person's weight is too heavy for snow"), ("B", "Because normal shoes have a small area, so the pressure on the snow is high"), ("C", "Because snow always melts under any shoe"), ("D", "Because the shoes are too warm")], "a": "B", "hint": "Pressure = Force ÷ Area. A small shoe area means a large pressure on the snow."},
    {"q": "Why do snowshoes help a person walk on snow without sinking?", "options": [("A", "They make the person lighter"), ("B", "They keep the feet warm so snow doesn't stick"), ("C", "They spread the body's weight over a larger area, lowering the pressure on the snow"), ("D", "They have spikes that grip the snow")], "a": "C", "hint": "Same weight, but a much bigger area underneath. What does that do to pressure?"},
    {"q": "If the force stays the same and the area increases, what happens to the pressure?", "options": [("A", "Pressure increases"), ("B", "Pressure decreases"), ("C", "Pressure stays the same"), ("D", "Pressure becomes zero")], "a": "B", "hint": "Use P = F ÷ A. If the bottom number (area) gets bigger, what happens to the answer?"},
    {"q": "Why are tires on a large tractor or construction truck much wider than tires on a small car?", "options": [("A", "To make the truck go faster"), ("B", "To use more rubber and look bigger"), ("C", "Wider tires increase the contact area, which lowers the pressure on the ground so the truck doesn't sink into soft soil"), ("D", "Wider tires make the engine more powerful")], "a": "C", "hint": "Heavy vehicles need to spread their weight. Bigger area means lower pressure on the ground."},
    {"q": "Why is a knife sharpened to have a thin edge?", "options": [("A", "A thin edge looks nicer"), ("B", "A thin edge has a very small area, so a small force creates a large pressure that cuts easily"), ("C", "A thin edge weighs less"), ("D", "A thin edge stays cool")], "a": "B", "hint": "The same push you give creates much more pressure when the area is tiny."},
    {"q": "Why does a school bag with a wide strap feel more comfortable than one with a thin strap?", "options": [("A", "Wide straps are softer materials"), ("B", "Wide straps make the bag lighter"), ("C", "A wider strap spreads the weight over a larger area on your shoulder, lowering the pressure"), ("D", "Wide straps prevent the bag from falling")], "a": "C", "hint": "Same weight on your shoulder, but spread over more area. What happens to pressure?"},
    {"q": "Why does a camel have wide, flat feet?", "options": [("A", "To run faster in the desert"), ("B", "Wide feet increase the area, lowering the pressure on the sand so the camel doesn't sink"), ("C", "To stay cool in hot weather"), ("D", "To carry more water inside")], "a": "B", "hint": "Just like snowshoes — but on sand instead of snow."},
    {"q": "Why is the pointed tip of a nail used to hammer it into wood, instead of the flat head?", "options": [("A", "The point is heavier"), ("B", "The point is sharper looking"), ("C", "The pointed tip has a very small area, so the same hammer force creates a much higher pressure that pushes through the wood"), ("D", "The point is made of stronger metal")], "a": "C", "hint": "Pressure depends on area. A tiny tip = huge pressure for the same hammer hit."},
    {"q": "A woman wearing high-heeled shoes makes deeper marks on a soft floor than a man wearing flat shoes, even when she is lighter. Why?", "options": [("A", "High heels are made of harder material"), ("B", "High heels have a very small contact area, so the pressure on the floor is much higher"), ("C", "High heels increase the woman's weight"), ("D", "High heels make the floor weaker")], "a": "B", "hint": "Force can be smaller, but if the area is tiny, pressure can still be very large."},
    {"q": "Why do skis help a skier glide on top of snow without sinking?", "options": [("A", "Skis are lighter than the skier"), ("B", "Skis melt the snow as they move"), ("C", "Skis have a large surface area, which spreads the skier's weight and lowers the pressure on the snow"), ("D", "Skis are coated in oil")], "a": "C", "hint": "More area underneath → less pressure on the snow."},
    {"q": "Why is a doctor's needle made very thin and pointed?", "options": [("A", "To save metal"), ("B", "Because a tiny tip area produces high pressure with a small force, allowing it to pass through skin easily"), ("C", "So that medicine flows faster"), ("D", "So it is easier to see")], "a": "B", "hint": "A very small area + a small push = a very large pressure."},
    {"q": "A heavy box is placed first on its small face and then on its larger face on a soft floor. In which case is the pressure on the floor greater?", "options": [("A", "When placed on the small face — same weight over a smaller area means more pressure"), ("B", "When placed on the larger face"), ("C", "Pressure is the same in both cases"), ("D", "Pressure becomes zero on the small face")], "a": "A", "hint": "Same force (weight). The smaller the area, the greater the pressure."},
]

GENERATORS = {
    "arithmetic": gen_arithmetic,
    "fractions": gen_fractions,
    "area": gen_area,
    "volume": gen_volume,
    "pressure": gen_pressure,
}


def build_questions(topic, grade, count):
    if topic == "pressure_concepts":
        pool = list(PRESSURE_CONCEPT_QUESTIONS)
        random.shuffle(pool)
        selected = pool[:count]
        return [{"q": item["q"], "a": item["a"], "options": [list(opt) for opt in item["options"]], "hint": item["hint"], "explanation": item["hint"]} for item in selected]
    gen = GENERATORS[topic]
    out = []
    for _ in range(count):
        q, a, explanation = gen(grade)
        out.append({"q": q, "a": a, "explanation": explanation})
    return out


def normalize_answer(s):
    return s.strip().lower().replace(" ", "")


def check_answer(user, correct):
    u = normalize_answer(user)
    c = normalize_answer(correct)
    if u == c:
        return True
    try:
        return abs(float(u) - float(c)) < 0.02
    except ValueError:
        return False


@app.route("/quiz", methods=["GET", "POST"])
def quiz_setup():
    if request.method == "POST":
        try:
            grade = int(request.form.get("grade", "1"))
            topic = request.form.get("topic", "arithmetic")
            if topic not in QUIZ_TOPICS or not 1 <= grade <= 9:
                raise ValueError
        except ValueError:
            return render_template("quiz_setup.html", topics=QUIZ_TOPICS, error="Please choose a valid grade and topic.")
        questions = build_questions(topic, grade, QUIZ_LENGTH)
        session["quiz"] = {"grade": grade, "topic": topic, "questions": questions, "index": 0, "score": 0, "history": []}
        return redirect(url_for("quiz_play"))
    return render_template("quiz_setup.html", topics=QUIZ_TOPICS, error=None)


@app.route("/quiz/play", methods=["GET", "POST"])
def quiz_play():
    quiz = session.get("quiz")
    if not quiz:
        return redirect(url_for("quiz_setup"))
    feedback = None
    if request.method == "POST":
        idx = quiz["index"]
        question = quiz["questions"][idx]
        user_answer = request.form.get("answer", "").strip()
        correct = check_answer(user_answer, question["a"])
        if correct:
            quiz["score"] += 1
        quiz["history"].append({"q": question["q"], "your_answer": user_answer, "correct_answer": question["a"], "correct": correct, "explanation": question.get("explanation", "")})
        quiz["index"] += 1
        session["quiz"] = quiz
        if quiz["index"] >= len(quiz["questions"]):
            return redirect(url_for("quiz_result"))
        feedback = {"correct": correct, "correct_answer": question["a"], "explanation": question.get("explanation", "")}
    current = quiz["questions"][quiz["index"]]
    return render_template("quiz_play.html", question=current["q"], options=current.get("options"), hint=current.get("hint"), index=quiz["index"] + 1, total=len(quiz["questions"]), topic=QUIZ_TOPICS[quiz["topic"]], grade=quiz["grade"], feedback=feedback)


@app.route("/quiz/result")
def quiz_result():
    quiz = session.get("quiz")
    if not quiz:
        return redirect(url_for("quiz_setup"))
    return render_template("quiz_result.html", score=quiz["score"], total=len(quiz["questions"]), history=quiz["history"], topic=QUIZ_TOPICS[quiz["topic"]], topic_key=quiz["topic"], grade=quiz["grade"])


@app.route("/progress")
def progress():
    return render_template("progress.html")


@app.route("/codelab")
def codelab():
    return render_template("codelab.html")


@app.route("/learn")
def learn_to_read():
    return render_template("learn.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
