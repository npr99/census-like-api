from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import sqlite3, json

DB_PATH = "data.db"

app = FastAPI(title="Census-like API")

def db():
    return sqlite3.connect(DB_PATH)

# --- Discovery endpoints ---
@app.get("/datasets")
def list_datasets():
    with open("datasets.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/variables")
def list_variables():
    with open("variables.json", "r", encoding="utf-8") as f:
        return json.load(f)

# --- Data endpoint (Census-like: /data?get=var1,var2&for=state:48&time=2023) ---
@app.get("/data")
def get_data(
    get: str = Query(..., description="Comma-separated variable names, e.g. POP,MEDIAN_INCOME"),
    for_: str = Query(..., alias="for", description="Geography filter, e.g. state:48 or state:*"),
    time: str = Query(None, description="Year filter, e.g. 2023 or *")
):
    # parse geography (only state supported in this basic demo)
    try:
        geo_type, geo_value = for_.split(":")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid 'for' parameter. Use state:48 or state:*")
    if geo_type != "state":
        raise HTTPException(status_code=400, detail="Only 'state' geography is supported in this demo.")

    vars_requested = [v.strip() for v in get.split(",") if v.strip()]
    with open("variables.json", "r", encoding="utf-8") as f:
        vars_meta = json.load(f)

    # validate requested variables
    for v in vars_requested:
        if v not in vars_meta:
            raise HTTPException(status_code=400, detail=f"Unknown variable: {v}")

    # construct SQL
    columns = ["year", "state"] + vars_requested + ["NAME"]  # include label
    select_cols = ", ".join(columns)
    sql = f"SELECT {select_cols} FROM fact_demo_states WHERE 1=1"
    params = []

    if geo_value != "*":
        sql += " AND state = ?"
        params.append(geo_value)

    if time and time != "*":
        sql += " AND year = ?"
        params.append(time)

    sql += " ORDER BY year, state"

    # run query
    con = db()
    cur = con.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    con.close()

    # Census API-like response: header row + values
    header = columns
    data = [header] + [list(map(lambda x: int(x) if isinstance(x, int) else x, row)) for row in rows]
    return data
