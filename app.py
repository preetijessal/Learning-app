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
    # NEW topics below
    "word_problems": "Word Problems (Math)",
    "cells_life": "Science: Cells & Living Things",
    "forces_motion": "Science: Forces & Motion",
    "water_cycle": "Science: Weather & Water Cycle",
    "grammar": "English: Grammar & Parts of Speech",
    "comprehension": "English: Reading Comprehension",
    "percentages": "Percentages",
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


# NEW: Percentages generator
def gen_percentages(grade):
    question_type = random.choice(["find_percent_of", "what_percent", "percent_change"]) if grade >= 6 else random.choice(["find_percent_of", "what_percent"])

    if question_type == "find_percent_of":
        percents = [10, 20, 25, 50, 75] if grade <= 5 else [5, 15, 30, 35, 40, 60, 70, 80]
        p = random.choice(percents)
        whole = random.choice([20, 40, 50, 80, 100, 120, 200]) if grade <= 5 else random.choice([60, 75, 120, 150, 200, 240, 300, 500])
        ans = round(p * whole / 100, 2)
        ans_str = str(int(ans)) if ans == int(ans) else str(ans)
        question = f"What is {p}% of {whole}?"
        explanation = f"Convert percent to decimal: {p}% = {p/100}. Then multiply: {p/100} × {whole} = {ans_str}."
        return question, ans_str, explanation

    if question_type == "what_percent":
        whole = random.choice([20, 25, 40, 50, 80, 100, 200])
        part = random.choice([i for i in range(1, whole) if (i * 100) % whole == 0])
        ans = int(part * 100 / whole)
        question = f"What percentage is {part} out of {whole}?"
        explanation = f"Divide the part by the whole and multiply by 100: ({part} ÷ {whole}) × 100 = {ans}%."
        return question, str(ans), explanation

    if question_type == "percent_change":
        original = random.choice([20, 40, 50, 80, 100, 120, 150, 200])
        change_pct = random.choice([10, 20, 25, 50])
        change = int(original * change_pct / 100)
        direction = random.choice(["increase", "decrease"])
        new_val = original + change if direction == "increase" else original - change
        question = f"A price was ${original}. It had a {change_pct}% {direction}. What is the new price?"
        explanation = f"{change_pct}% of {original} = {change}. New price = {original} {'+ ' + str(change) if direction == 'increase' else '− ' + str(change)} = ${new_val}."
        return question, str(new_val), explanation


# -------------------- NEW: Multiple-Choice Question Banks --------------------

# NEW: Word Problems (Math)
WORD_PROBLEM_QUESTIONS = [
    {
        "q": "A bookshop sold 145 books on Monday and 78 books on Tuesday. How many MORE books were sold on Monday than on Tuesday?",
        "options": [("A", "67"), ("B", "77"), ("C", "223"), ("D", "87")],
        "a": "A",
        "hint": "Subtract the smaller number from the larger: 145 − 78."
    },
    {
        "q": "Emma has $50. She buys 3 notebooks at $4.50 each and a pen for $2.75. How much money does she have left?",
        "options": [("A", "$34.25"), ("B", "$33.25"), ("C", "$36.25"), ("D", "$43.25")],
        "a": "B",
        "hint": "Find cost of 3 notebooks: 3 × $4.50 = $13.50. Add the pen: $13.50 + $2.75 = $16.25. Subtract from $50."
    },
    {
        "q": "A train travels at 90 km/h. How far will it travel in 2 hours and 30 minutes?",
        "options": [("A", "180 km"), ("B", "200 km"), ("C", "225 km"), ("D", "270 km")],
        "a": "C",
        "hint": "2 hours 30 minutes = 2.5 hours. Distance = speed × time = 90 × 2.5."
    },
    {
        "q": "A baker uses 2/3 kg of flour to make one loaf of bread. How much flour is needed for 6 loaves?",
        "options": [("A", "3 kg"), ("B", "4 kg"), ("C", "5 kg"), ("D", "6 kg")],
        "a": "B",
        "hint": "Multiply: 6 × 2/3 = 12/3 = 4 kg."
    },
    {
        "q": "There are 360 students in a school. 45% of them are boys. How many girls are there?",
        "options": [("A", "162"), ("B", "198"), ("C", "180"), ("D", "216")],
        "a": "B",
        "hint": "Boys = 45% of 360 = 162. Girls = 360 − 162 = 198."
    },
    {
        "q": "A rectangle has a perimeter of 48 cm. Its length is 14 cm. What is its width?",
        "options": [("A", "8 cm"), ("B", "10 cm"), ("C", "12 cm"), ("D", "20 cm")],
        "a": "B",
        "hint": "Perimeter = 2 × (length + width). So 48 = 2 × (14 + width). Divide 48 by 2, then subtract 14."
    },
    {
        "q": "Mia earns $12.50 per hour. She works 8 hours on Saturday and 5 hours on Sunday. How much does she earn in total?",
        "options": [("A", "$100", ), ("B", "$150"), ("C", "$162.50"), ("D", "$187.50")],
        "a": "C",
        "hint": "Total hours = 8 + 5 = 13. Earnings = 13 × $12.50."
    },
    {
        "q": "A water tank holds 1,200 litres. It is currently 3/4 full. How many litres of water are in the tank?",
        "options": [("A", "300 L"), ("B", "600 L"), ("C", "800 L"), ("D", "900 L")],
        "a": "D",
        "hint": "Find 3/4 of 1200: (3 ÷ 4) × 1200 = 900 litres."
    },
    {
        "q": "A car uses 8 litres of fuel every 100 km. How much fuel does it need for a 350 km trip?",
        "options": [("A", "24 L"), ("B", "28 L"), ("C", "32 L"), ("D", "40 L")],
        "a": "B",
        "hint": "Fuel per km = 8 ÷ 100 = 0.08 L. For 350 km: 0.08 × 350 = 28 litres."
    },
    {
        "q": "A bag of apples costs $3.60. If you buy 4 bags, how much change do you get from $20?",
        "options": [("A", "$5.60"), ("B", "$6.40"), ("C", "$14.40"), ("D", "$16.40")],
        "a": "B",
        "hint": "Cost of 4 bags = 4 × $3.60 = $14.40. Change = $20.00 − $14.40."
    },
    {
        "q": "A class of 30 students took a test. 18 students scored above 70%. What percentage scored 70% or below?",
        "options": [("A", "30%"), ("B", "40%"), ("C", "50%"), ("D", "60%")],
        "a": "B",
        "hint": "Students at 70% or below = 30 − 18 = 12. Percentage = (12 ÷ 30) × 100."
    },
    {
        "q": "A jacket costs $80. It is on sale with a 25% discount. What is the sale price?",
        "options": [("A", "$55"), ("B", "$60"), ("C", "$65"), ("D", "$75")],
        "a": "B",
        "hint": "Discount = 25% of $80 = $20. Sale price = $80 − $20 = $60."
    },
]

# NEW: Science — Cells & Living Things
CELLS_LIFE_QUESTIONS = [
    {
        "q": "What is the basic unit of all living things?",
        "options": [("A", "Atom"), ("B", "Cell"), ("C", "Molecule"), ("D", "Organ")],
        "a": "B",
        "hint": "All living organisms — from bacteria to humans — are made of this."
    },
    {
        "q": "What is the function of the mitochondria in a cell?",
        "options": [("A", "Controls what enters and exits the cell"), ("B", "Stores the cell's genetic information"), ("C", "Produces energy for the cell"), ("D", "Makes food using sunlight")],
        "a": "C",
        "hint": "Think of it as the 'powerhouse' — it converts food into energy the cell can use."
    },
    {
        "q": "Which of these is found in plant cells but NOT in animal cells?",
        "options": [("A", "Cell membrane"), ("B", "Nucleus"), ("C", "Mitochondria"), ("D", "Cell wall")],
        "a": "D",
        "hint": "Animal cells have a flexible membrane. Plant cells have an extra rigid structure outside that."
    },
    {
        "q": "What process do plant cells use to make their own food?",
        "options": [("A", "Respiration"), ("B", "Digestion"), ("C", "Photosynthesis"), ("D", "Circulation")],
        "a": "C",
        "hint": "Plants use sunlight, water, and CO₂ to produce glucose. The green pigment chlorophyll helps."
    },
    {
        "q": "Which gas do plants absorb during photosynthesis?",
        "options": [("A", "Oxygen"), ("B", "Nitrogen"), ("C", "Carbon dioxide"), ("D", "Hydrogen")],
        "a": "C",
        "hint": "Plants take in CO₂ from the air through tiny pores called stomata."
    },
    {
        "q": "Which gas do plants release during photosynthesis?",
        "options": [("A", "Carbon dioxide"), ("B", "Nitrogen"), ("C", "Water vapour"), ("D", "Oxygen")],
        "a": "D",
        "hint": "Photosynthesis produces glucose and a gas that humans and animals need to breathe."
    },
    {
        "q": "What does the nucleus of a cell do?",
        "options": [("A", "Produces energy"), ("B", "Controls the cell and contains DNA"), ("C", "Allows substances to pass in and out"), ("D", "Stores water")],
        "a": "B",
        "hint": "Think of it as the 'control centre' or 'brain' of the cell."
    },
    {
        "q": "What is the function of the cell membrane?",
        "options": [("A", "Makes food for the cell"), ("B", "Provides rigid support"), ("C", "Controls what enters and exits the cell"), ("D", "Contains chlorophyll")],
        "a": "C",
        "hint": "It acts like a gatekeeper — deciding what goes in and out of the cell."
    },
    {
        "q": "Which part of the plant cell contains chlorophyll?",
        "options": [("A", "Vacuole"), ("B", "Cell wall"), ("C", "Nucleus"), ("D", "Chloroplast")],
        "a": "D",
        "hint": "This green-coloured organelle is where photosynthesis actually happens."
    },
    {
        "q": "True or False: All living things are made of cells.",
        "options": [("A", "True — every living organism is made of one or more cells"), ("B", "False — only animals are made of cells"), ("C", "False — plants are not made of cells"), ("D", "False — only large organisms have cells")],
        "a": "A",
        "hint": "This is one of the key principles of biology — called the Cell Theory."
    },
    {
        "q": "What does the large vacuole in a plant cell do?",
        "options": [("A", "Makes energy"), ("B", "Controls the cell"), ("C", "Stores water and helps keep the cell firm"), ("D", "Absorbs sunlight")],
        "a": "C",
        "hint": "When a plant is well watered, this structure fills up and keeps the plant from drooping."
    },
    {
        "q": "Which of these is NOT a living thing?",
        "options": [("A", "Mushroom"), ("B", "Bacterium"), ("C", "Rock"), ("D", "Fern")],
        "a": "C",
        "hint": "Living things grow, reproduce, and respond to their environment. Which one does none of these?"
    },
]

# NEW: Science — Forces & Motion
FORCES_MOTION_QUESTIONS = [
    {
        "q": "A car travels 120 km in 2 hours. What is its average speed?",
        "options": [("A", "60 km/h"), ("B", "80 km/h"), ("C", "100 km/h"), ("D", "240 km/h")],
        "a": "A",
        "hint": "Speed = Distance ÷ Time = 120 ÷ 2."
    },
    {
        "q": "Why does a ball eventually stop rolling on a flat surface even if nothing blocks it?",
        "options": [("A", "Gravity pulls it sideways"), ("B", "The ball runs out of energy suddenly"), ("C", "Friction between the ball and surface slows it down"), ("D", "Air disappears around the ball")],
        "a": "C",
        "hint": "Think about the force that acts against motion at the surface where two objects touch."
    },
    {
        "q": "Which of these is a NON-CONTACT force?",
        "options": [("A", "Friction"), ("B", "Pushing a box"), ("C", "Kicking a ball"), ("D", "Gravity")],
        "a": "D",
        "hint": "This force acts on objects without them touching — like the pull between Earth and the Moon."
    },
    {
        "q": "What happens to friction when a surface becomes rougher?",
        "options": [("A", "Friction decreases"), ("B", "Friction increases"), ("C", "Friction disappears"), ("D", "Friction stays the same")],
        "a": "B",
        "hint": "More bumps and ridges on a surface means more resistance to movement."
    },
    {
        "q": "A bicycle slows down when the rider stops pedalling. What force is mainly responsible?",
        "options": [("A", "Magnetism"), ("B", "Air resistance and friction"), ("C", "Gravity pulling it forward"), ("D", "The engine stopping")],
        "a": "B",
        "hint": "Two forces act against the bicycle's motion — one between the tires and ground, one from the air."
    },
    {
        "q": "According to Newton's First Law, what happens to a moving object if no force acts on it?",
        "options": [("A", "It gradually slows down and stops"), ("B", "It speeds up"), ("C", "It keeps moving at the same speed in the same direction"), ("D", "It moves in a circle")],
        "a": "C",
        "hint": "Newton's First Law says objects don't change their motion unless a force makes them."
    },
    {
        "q": "Which of these is a CONTACT force?",
        "options": [("A", "Gravity"), ("B", "Magnetism"), ("C", "Friction"), ("D", "Static electricity pulling hair")],
        "a": "C",
        "hint": "Contact forces only act when two objects are physically touching."
    },
    {
        "q": "A car travels 300 km in 3 hours. What is its average speed?",
        "options": [("A", "90 km/h"), ("B", "100 km/h"), ("C", "150 km/h"), ("D", "900 km/h")],
        "a": "B",
        "hint": "Speed = Distance ÷ Time = 300 ÷ 3."
    },
    {
        "q": "Why is it harder to stop on an icy road than on dry pavement?",
        "options": [("A", "Ice makes cars go faster"), ("B", "Ice is heavier than pavement"), ("C", "Ice reduces friction, so there is less braking force"), ("D", "Cold weather weakens car engines")],
        "a": "C",
        "hint": "Less friction = harder to stop. That's why icy roads are dangerous."
    },
    {
        "q": "What is the unit of force?",
        "options": [("A", "Kilogram (kg)"), ("B", "Metre (m)"), ("C", "Newton (N)"), ("D", "Pascal (Pa)")],
        "a": "C",
        "hint": "Named after the scientist who described the laws of motion."
    },
    {
        "q": "A book sits still on a table. What does this tell us about the forces acting on it?",
        "options": [("A", "No forces are acting on it"), ("B", "Only gravity acts on it"), ("C", "The forces are balanced — gravity down and the table pushing up"), ("D", "The book is producing its own force")],
        "a": "C",
        "hint": "If an object is not moving, all forces on it must be balanced — they cancel each other out."
    },
    {
        "q": "Which example shows a force CHANGING THE DIRECTION of an object?",
        "options": [("A", "Pushing a stationary box to make it move"), ("B", "A goalkeeper kicking a ball that was rolling toward the net"), ("C", "Lifting a heavy suitcase"), ("D", "Squeezing clay")],
        "a": "B",
        "hint": "Forces can change speed, direction, or shape. Which example shows a change in direction?"
    },
]

# NEW: Science — Weather & Water Cycle
WATER_CYCLE_QUESTIONS = [
    {
        "q": "What are the four main stages of the water cycle in the correct order?",
        "options": [("A", "Condensation → Precipitation → Evaporation → Collection"), ("B", "Evaporation → Condensation → Precipitation → Collection"), ("C", "Precipitation → Evaporation → Collection → Condensation"), ("D", "Collection → Precipitation → Condensation → Evaporation")],
        "a": "B",
        "hint": "Water heats up and rises first, then cools and forms clouds, then falls, then gathers."
    },
    {
        "q": "What causes evaporation in the water cycle?",
        "options": [("A", "Cold temperatures freezing the water"), ("B", "Wind blowing water away"), ("C", "The Sun's heat warming water so it turns into water vapour"), ("D", "Clouds absorbing water from the ground")],
        "a": "C",
        "hint": "The Sun heats oceans, lakes, and rivers. The water turns from liquid to gas (water vapour)."
    },
    {
        "q": "What is condensation in the water cycle?",
        "options": [("A", "Water vapour rising into the atmosphere"), ("B", "Water falling from clouds as rain or snow"), ("C", "Water vapour cooling and turning back into liquid droplets, forming clouds"), ("D", "Water soaking into the ground")],
        "a": "C",
        "hint": "It's the opposite of evaporation. When the gas cools down enough, it becomes liquid again."
    },
    {
        "q": "What is precipitation?",
        "options": [("A", "Water heating up and becoming steam"), ("B", "Water vapour forming clouds"), ("C", "Water falling from clouds as rain, snow, sleet, or hail"), ("D", "Rivers flowing into the ocean")],
        "a": "C",
        "hint": "Precipitation is the word for all forms of water falling from the sky."
    },
    {
        "q": "What is the difference between weather and climate?",
        "options": [("A", "Weather is long-term average conditions; climate is the daily conditions"), ("B", "Weather is what happens day to day; climate is the long-term average for a region"), ("C", "They mean exactly the same thing"), ("D", "Weather is only about temperature; climate includes wind and rain")],
        "a": "B",
        "hint": "One changes day to day; the other describes patterns over many years."
    },
    {
        "q": "Why is the water cycle important for life on Earth? Choose the BEST answer.",
        "options": [("A", "It creates mountains and volcanoes"), ("B", "It provides fresh water for drinking and supports plant growth and rainfall"), ("C", "It keeps the Sun shining brightly"), ("D", "It prevents earthquakes")],
        "a": "B",
        "hint": "Think about where the fresh water we drink and the rain that grows our food comes from."
    },
    {
        "q": "Where does most of the water that evaporates into the atmosphere come from?",
        "options": [("A", "Underground rivers"), ("B", "Clouds"), ("C", "Oceans, lakes, and rivers on the Earth's surface"), ("D", "Polar ice caps only")],
        "a": "C",
        "hint": "Most of the Earth's surface is water. The Sun heats it, turning it into vapour."
    },
    {
        "q": "What happens to water after it falls as precipitation?",
        "options": [("A", "It immediately evaporates again"), ("B", "It collects in rivers, lakes, and oceans, or soaks into the ground"), ("C", "It turns into rock"), ("D", "It floats up to form new clouds immediately")],
        "a": "B",
        "hint": "This stage is called 'collection' — water gathers before the cycle starts again."
    },
    {
        "q": "What type of cloud is typically associated with heavy rain and thunderstorms?",
        "options": [("A", "Cirrus"), ("B", "Stratus"), ("C", "Cumulonimbus"), ("D", "Cumulus")],
        "a": "C",
        "hint": "This tall, dark, towering cloud type is sometimes called a thundercloud."
    },
    {
        "q": "A puddle on the street disappears after a sunny day even though nobody wiped it up. Which stage of the water cycle explains this?",
        "options": [("A", "Condensation"), ("B", "Precipitation"), ("C", "Collection"), ("D", "Evaporation")],
        "a": "D",
        "hint": "The Sun's heat caused the liquid water to turn into water vapour and rise into the air."
    },
]

# NEW: English — Grammar & Parts of Speech
GRAMMAR_QUESTIONS = [
    {
        "q": "Identify the NOUN in this sentence: 'The brave knight defeated the enormous dragon.'",
        "options": [("A", "brave"), ("B", "defeated"), ("C", "knight"), ("D", "enormous")],
        "a": "C",
        "hint": "A noun is a person, place, thing, or idea. Look for the 'who' in the sentence."
    },
    {
        "q": "Identify the VERB in this sentence: 'The brave knight quickly defeated the enormous dragon.'",
        "options": [("A", "brave"), ("B", "defeated"), ("C", "quickly"), ("D", "enormous")],
        "a": "B",
        "hint": "A verb is an action or state word — what the subject is doing."
    },
    {
        "q": "Identify the ADJECTIVE in this sentence: 'The brave knight defeated the enormous dragon.'",
        "options": [("A", "knight"), ("B", "defeated"), ("C", "quickly"), ("D", "brave")],
        "a": "D",
        "hint": "An adjective describes a noun. Which word describes what the knight is like?"
    },
    {
        "q": "Identify the ADVERB in this sentence: 'The brave knight quickly defeated the enormous dragon.'",
        "options": [("A", "quickly"), ("B", "brave"), ("C", "enormous"), ("D", "knight")],
        "a": "A",
        "hint": "An adverb describes how, when, or where an action happens. It often ends in '-ly'."
    },
    {
        "q": "Which sentence is grammatically CORRECT?",
        "options": [("A", "They was going to the park."), ("B", "They were going to the park."), ("C", "They is going to the park."), ("D", "They be going to the park.")],
        "a": "B",
        "hint": "The subject 'They' is plural, so it needs a plural verb form."
    },
    {
        "q": "Which word is a PRONOUN in this sentence: 'Maria forgot her lunchbox at school.'",
        "options": [("A", "Maria"), ("B", "forgot"), ("C", "her"), ("D", "lunchbox")],
        "a": "C",
        "hint": "A pronoun replaces a noun. Which word stands in for Maria's name?"
    },
    {
        "q": "What type of sentence is this: 'It was raining, but we still played outside.'",
        "options": [("A", "Simple sentence"), ("B", "Compound sentence"), ("C", "Complex sentence"), ("D", "Fragment")],
        "a": "B",
        "hint": "This sentence has TWO main ideas joined by a connecting word (but, and, or, so)."
    },
    {
        "q": "Which word is a suitable ADVERB to complete this sentence: 'The dog barked ________.'",
        "options": [("A", "loudly"), ("B", "loud"), ("C", "louder"), ("D", "loudness")],
        "a": "A",
        "hint": "An adverb describing how the dog barked. Adverbs describing manner often end in '-ly'."
    },
    {
        "q": "Which sentence uses the CORRECT punctuation?",
        "options": [("A", "where are you going asked the teacher"), ("B", "\"Where are you going?\" asked the teacher."), ("C", "Where are you going, asked the teacher"), ("D", "where are you going. asked the teacher")],
        "a": "B",
        "hint": "Spoken words (dialogue) go inside quotation marks, with a question mark if it is a question."
    },
    {
        "q": "Which of these is a COMPLEX sentence?",
        "options": [("A", "The cat sat on the mat."), ("B", "The cat sat and the dog slept."), ("C", "The cat sat on the mat because it was warm there."), ("D", "The cat. The mat.")],
        "a": "C",
        "hint": "A complex sentence has a main clause AND a dependent clause joined by words like 'because', 'although', 'when', or 'if'."
    },
    {
        "q": "What is the SUBJECT of this sentence: 'Every morning, the children walk to school.'",
        "options": [("A", "Every morning"), ("B", "walk"), ("C", "school"), ("D", "the children")],
        "a": "D",
        "hint": "The subject is WHO or WHAT the sentence is about — who is doing the action?"
    },
    {
        "q": "Which word correctly completes the sentence: 'She _______ finished her homework before dinner.'",
        "options": [("A", "quick"), ("B", "quickest"), ("C", "quickly"), ("D", "quickness")],
        "a": "C",
        "hint": "We need a word describing HOW she finished — an adverb, not an adjective."
    },
]

# NEW: English — Reading Comprehension
COMPREHENSION_QUESTIONS = [
    {
        "q": "PASSAGE: 'The ocean covers more than 70% of Earth's surface and is home to millions of species. Scientists estimate that more than 80% of the ocean remains unexplored. The deep ocean is pitch black, freezing cold, and under enormous pressure.'\n\nAccording to the passage, what percentage of the ocean remains unexplored?",
        "options": [("A", "70%"), ("B", "80%"), ("C", "50%"), ("D", "90%")],
        "a": "B",
        "hint": "Look for the exact number mentioned in the passage about unexplored ocean."
    },
    {
        "q": "PASSAGE: 'The ocean covers more than 70% of Earth's surface and is home to millions of species. Scientists estimate that more than 80% of the ocean remains unexplored. The deep ocean is pitch black, freezing cold, and under enormous pressure. Strange creatures thrive there, including the anglerfish, which uses a glowing lure to attract prey in the darkness.'\n\nHow does the anglerfish find its prey in the dark?",
        "options": [("A", "It uses its sharp eyesight"), ("B", "It uses a glowing lure to attract prey"), ("C", "It uses sonar like a bat"), ("D", "It follows ocean currents")],
        "a": "B",
        "hint": "Find the sentence in the passage that describes the anglerfish specifically."
    },
    {
        "q": "PASSAGE: 'Every year, new ocean species are discovered, reminding us how much we still have to learn about our planet. The deep ocean is one of the most mysterious places on Earth.'\n\nWhat is the MAIN IDEA of this passage?",
        "options": [("A", "Anglerfish are dangerous predators"), ("B", "The ocean is too deep for humans to ever explore"), ("C", "The ocean is largely unexplored and full of mysteries yet to be discovered"), ("D", "Scientists have mapped the entire ocean floor")],
        "a": "C",
        "hint": "The main idea is the overall message of the passage, not just one detail."
    },
    {
        "q": "PASSAGE: 'Bees are essential to our food supply. As they fly from flower to flower collecting nectar, they transfer pollen, which allows plants to reproduce. Scientists estimate that one third of all the food we eat depends on pollination by bees.'\n\nWhat do bees do as they collect nectar?",
        "options": [("A", "They build their honeycombs"), ("B", "They transfer pollen between flowers, helping plants reproduce"), ("C", "They drink water from flowers"), ("D", "They protect flowers from insects")],
        "a": "B",
        "hint": "Look for what happens AS the bees collect nectar — what else are they doing at the same time?"
    },
    {
        "q": "PASSAGE: 'Bees are essential to our food supply. Scientists estimate that one third of all the food we eat depends on pollination by bees. Without bees, many fruits, vegetables, and nuts would disappear from our diet.'\n\nAccording to the passage, what fraction of our food depends on bee pollination?",
        "options": [("A", "One half"), ("B", "Two thirds"), ("C", "One quarter"), ("D", "One third")],
        "a": "D",
        "hint": "Look for the fraction stated directly in the passage."
    },
    {
        "q": "PASSAGE: 'The Amazon rainforest covers over 5.5 million square kilometres and produces about 20% of the world's oxygen. It is home to 10% of all species on Earth. However, deforestation is destroying around 10,000 square kilometres of forest every year.'\n\nWhat is one THREAT mentioned to the Amazon rainforest?",
        "options": [("A", "Flooding from the Amazon River"), ("B", "Earthquakes destroying the trees"), ("C", "Deforestation — cutting down the forest"), ("D", "Invasive animals eating all the plants")],
        "a": "C",
        "hint": "The passage mentions something that is 'destroying' the forest. What word is used?"
    },
    {
        "q": "PASSAGE: 'The Amazon rainforest produces about 20% of the world's oxygen and is home to 10% of all species on Earth.'\n\nWhat TWO important roles does the Amazon play? Choose the BEST answer.",
        "options": [("A", "It provides clean drinking water and generates electricity"), ("B", "It produces oxygen and provides habitat for a huge variety of species"), ("C", "It controls the world's temperature and creates rainfall only in South America"), ("D", "It produces food for humans and supplies timber to the world")],
        "a": "B",
        "hint": "Both roles are stated clearly in the passage — look for what it 'produces' and what it is 'home to'."
    },
    {
        "q": "PASSAGE: 'Marie Curie was the first woman to win a Nobel Prize, and the only person ever to win Nobel Prizes in two different sciences — Physics in 1903 and Chemistry in 1911. Born in Poland, she moved to Paris to study because women were not allowed to attend university in her home country at the time.'\n\nWhy did Marie Curie move to Paris?",
        "options": [("A", "Paris had better laboratories than Poland"), ("B", "She wanted to be closer to other scientists"), ("C", "Women were not permitted to attend university in Poland at the time"), ("D", "She was offered a scholarship to study in France")],
        "a": "C",
        "hint": "The passage gives a direct reason. Look for the sentence about why she left her home country."
    },
    {
        "q": "PASSAGE: 'Marie Curie was the first woman to win a Nobel Prize, and the only person ever to win Nobel Prizes in two different sciences — Physics in 1903 and Chemistry in 1911.'\n\nWhat makes Marie Curie's Nobel Prize achievement unique?",
        "options": [("A", "She was the youngest person to ever win a Nobel Prize"), ("B", "She is the only person to have won Nobel Prizes in two different sciences"), ("C", "She won three Nobel Prizes in total"), ("D", "She shared her prize with Albert Einstein")],
        "a": "B",
        "hint": "The passage says she is the 'only person ever to...' — what exactly does it say she is the only one to have done?"
    },
    {
        "q": "READING SKILL — When answering a comprehension question asking you to EXPLAIN something, what should you always do?",
        "options": [("A", "Give your personal opinion only"), ("B", "Copy the question back out as your answer"), ("C", "Use evidence from the text to support your answer"), ("D", "Write as many sentences as possible regardless of relevance")],
        "a": "C",
        "hint": "Good comprehension answers always refer back to what the passage actually says."
    },
]


# -------------------- ORIGINAL: Pressure Concept Questions --------------------

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

# -------------------- Map all MC question banks --------------------

MC_QUESTION_BANKS = {
    "pressure_concepts": PRESSURE_CONCEPT_QUESTIONS,
    "word_problems":     WORD_PROBLEM_QUESTIONS,
    "cells_life":        CELLS_LIFE_QUESTIONS,
    "forces_motion":     FORCES_MOTION_QUESTIONS,
    "water_cycle":       WATER_CYCLE_QUESTIONS,
    "grammar":           GRAMMAR_QUESTIONS,
    "comprehension":     COMPREHENSION_QUESTIONS,
}

GENERATORS = {
    "arithmetic":  gen_arithmetic,
    "fractions":   gen_fractions,
    "area":        gen_area,
    "volume":      gen_volume,
    "pressure":    gen_pressure,
    "percentages": gen_percentages,  # NEW
}


def build_questions(topic, grade, count):
    # Multiple-choice banks
    if topic in MC_QUESTION_BANKS:
        pool = list(MC_QUESTION_BANKS[topic])
        random.shuffle(pool)
        selected = pool[:count]
        return [
            {
                "q": item["q"],
                "a": item["a"],
                "options": [list(opt) for opt in item["options"]],
                "hint": item["hint"],
                "explanation": item["hint"],
            }
            for item in selected
        ]
    # Generated (numeric) topics
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
