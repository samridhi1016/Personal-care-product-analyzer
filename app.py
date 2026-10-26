from flask import Flask, render_template, request
import sqlite3
import os
import sys

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "care.db")
EXCEL_PATH = os.path.join(BASE_DIR, "database", "care_ingredients.xlsx")

sys.path.insert(0, os.path.join(BASE_DIR, "database"))
from build_database import build_database  # type: ignore


def ensure_database_is_current():
    if not os.path.exists(DB_PATH) or os.path.getmtime(EXCEL_PATH) > os.path.getmtime(DB_PATH):
        build_database()


def get_db_connection():
    ensure_database_is_current()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def analyze_product(ingredient_text, skin_type=None):
    conn = get_db_connection()
    ingredients_db = conn.execute("SELECT * FROM ingredients").fetchall()
    conn.close()

    typed_ingredients = [i.strip().lower() for i in ingredient_text.split(",") if i.strip()]

    score = 100
    flags = []
    matched_names = set()

    for typed in typed_ingredients:
        for ing in ingredients_db:
            names_to_check = [ing["name"].lower()] + [a.strip() for a in (ing["aliases"] or "").lower().split(",") if a.strip()]
            names_to_check = [n for n in names_to_check if n]
            if typed in names_to_check or any(typed in n or n in typed for n in names_to_check):
                if ing["name"] not in matched_names:
                    matched_names.add(ing["name"])
                    category = ing["category"]
                    if category == "Harmful":
                        score -= 20
                    elif category == "Caution":
                        score -= 8
                    # Safe ingredients don't reduce the score

                    message = f"{ing['name']}: {ing['reason']}"
                    if skin_type and skin_type.lower() == "sensitive" and ing["skin_note"]:
                        message += f" ({ing['skin_note']})"

                    flags.append({
                        "type": "Ingredient",
                        "severity": category,
                        "message": message
                    })

    score = max(0, min(100, score))

    if score >= 80:
        grade = "Low Concern"
        grade_color = "green"
    elif score >= 50:
        grade = "Moderate Concern"
        grade_color = "orange"
    else:
        grade = "High Concern"
        grade_color = "red"

    return {
        "score": score,
        "grade": grade,
        "grade_color": grade_color,
        "flags": flags
    }

@app.route("/", methods=["GET"])
def index():
    conn = get_db_connection()
    ingredient_names = [row["name"] for row in conn.execute("SELECT name FROM ingredients ORDER BY name")]
    conn.close()
    return render_template("index.html", ingredient_names=ingredient_names)


@app.route("/analyze", methods=["POST"])
def analyze():
    product_name = request.form.get("product_name", "").strip() or "Your product"
    ingredients = request.form.get("ingredients", "")
    skin_type = request.form.get("skin_type", "")

    result = analyze_product(ingredients, skin_type)

    return render_template(
        "result.html",
        product_name=product_name,
        result=result,
        skin_type=skin_type
    )


if __name__ == "__main__":
    app.run(debug=True)