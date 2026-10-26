import sqlite3
import openpyxl
import os

EXCEL_FILE = "care_ingredients.xlsx"
DB_FILE = "care.db"


def build_database():
    here = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(here, EXCEL_FILE)
    db_path = os.path.join(here, DB_FILE)

    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            aliases TEXT,
            category TEXT NOT NULL,
            reason TEXT,
            skin_note TEXT
        )
    """)

    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws = wb["ingredients"]

    rows_added = 0
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        name, aliases, category, reason, skin_note = row
        cur.execute(
            "INSERT INTO ingredients (name, aliases, category, reason, skin_note) VALUES (?, ?, ?, ?, ?)",
            (name, (aliases or ""), category, reason, (skin_note or ""))
        )
        rows_added += 1

    conn.commit()
    conn.close()
    return rows_added


if __name__ == "__main__":
    n = build_database()
    print(f"Done. Imported {n} ingredients into {DB_FILE}")
    