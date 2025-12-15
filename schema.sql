-- core table
CREATE TABLE IF NOT EXISTS fact_demo_states (
  year TEXT NOT NULL,
  state TEXT NOT NULL,     -- FIPS, e.g., "48"
  NAME TEXT NOT NULL,
  POP INTEGER,
  MEDIAN_INCOME INTEGER,
  PRIMARY KEY (year, state)
);

-- optional indices to speed filters
CREATE INDEX IF NOT EXISTS ix_fact_demo_states_year ON fact_demo_states (year);
CREATE INDEX IF NOT EXISTS ix_fact_demo_states_state ON fact_demo_states (state);
