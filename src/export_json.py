"""
Runs the window-function SQL queries and writes results to docs/data/
as JSON files consumed by the GitHub Pages frontend.

Run after ingest_daily.py in the GitHub Actions workflow.
"""

import logging
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import text

from postgres_helperfile import create_postgres_engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

OUT_DIR = Path(__file__).parent.parent / "docs" / "data"

# Queries keyed by output filename (without .json)
SQL_FILE = Path(__file__).parent / "sql_tables" / "window_functions.sql"


def parse_queries(sql_file: Path) -> dict[str, str]:
    """Split window_functions.sql on '-- <name>' comment markers.

    A line is treated as a query name only when the previous non-blank line
    was a separator (starts with '-- ='), avoiding false matches on
    description comments inside the separator block.
    """
    queries = {}
    current_name = None
    current_lines: list[str] = []
    prev_was_separator = False

    for line in sql_file.read_text().splitlines():
        stripped = line.strip()
        is_separator = stripped.startswith("-- =")
        is_comment = stripped.startswith("-- ") and not is_separator

        if is_comment and prev_was_separator:
            # This is a query name marker immediately after a separator block
            if current_name and current_lines:
                queries[current_name] = "\n".join(current_lines).strip()
            current_name = stripped[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)

        if stripped:  # only update on non-blank lines
            prev_was_separator = is_separator

    if current_name and current_lines:
        queries[current_name] = "\n".join(current_lines).strip()

    return queries


def export(query_name: str, sql: str, conn) -> None:
    df = pd.read_sql(text(sql), conn)
    # Convert date columns to ISO strings for JSON serialisation
    for col in df.select_dtypes(include=["datetime64[ns]", "object"]):
        try:
            df[col] = pd.to_datetime(df[col]).dt.strftime("%Y-%m-%d")
        except Exception:
            pass

    out_path = OUT_DIR / f"{query_name}.json"
    df.to_json(out_path, orient="records", date_format="iso")
    logging.info("Wrote %d rows → %s", len(df), out_path)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    queries = parse_queries(SQL_FILE)
    logging.info("Found %d queries: %s", len(queries), list(queries.keys()))

    failures = []
    engine = create_postgres_engine()
    with engine.connect() as conn:
        for name, sql in queries.items():
            try:
                export(name, sql, conn)
            except Exception as e:
                logging.error("Failed to export %s: %s", name, e)
                failures.append(name)

    if failures:
        logging.error("Export failed for: %s", failures)
        sys.exit(1)


if __name__ == "__main__":
    main()
