import csv, sqlite3, sys

DB_PATH = "data.db"
CSV_PATH = "sample_data.csv"
SCHEMA = "schema.sql"

def run():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    with open(SCHEMA, "r") as f:
        cur.executescript(f.read())

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [
            (r["year"], r["state"], r["NAME"], int(r["POP"]), int(r["MEDIAN_INCOME"]))
            for r in reader
        ]
    cur.executemany("""
        INSERT OR REPLACE INTO fact_demo_states (year, state, NAME, POP, MEDIAN_INCOME)
        VALUES (?, ?, ?, ?, ?)
    """, rows)

    con.commit()
    con.close()
    print(f"Loaded {len(rows)} rows into {DB_PATH}")

if __name__ == "__main__":
    run()
   
