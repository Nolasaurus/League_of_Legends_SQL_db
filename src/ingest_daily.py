"""
Daily ingestion script for GitHub Actions.

Fetches the Challenger + GrandMaster ladder, then inserts any new matches
(those not already in match_metadata) into the database.

Capped at SUMMONER_SAMPLE summoners per run to stay within Riot rate limits.
"""

import logging
import random
import sys
from pathlib import Path

from api_client import API_Client
from insert_data import cached_insert
from postgres_helperfile import connect_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

SUMMONER_SAMPLE = 50   # max summoners to process per run
MATCHES_PER_SUMMONER = 20
MAX_INSERTS = 1000     # stop after inserting this many new matches per run
_SCHEMA = Path(__file__).parent / "sql_tables" / "loldb.sql"


def ensure_schema():
    """Apply loldb.sql to the database if tables don't exist yet."""
    sql = _SCHEMA.read_text()
    with connect_db("admin") as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    logging.info("Schema verified/applied.")


def match_id_exists(match_id: str) -> bool:
    """Point lookup against the PK index — no full table scan."""
    with connect_db("readonly") as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM match_metadata WHERE match_id = %s LIMIT 1", (match_id,)
            )
            return cur.fetchone() is not None


def main():
    ensure_schema()
    client = API_Client()

    challenger_ids = client.get_challenger_league() or []
    gm_ids = client.get_grandmaster_league() or []
    all_ids = list(set(challenger_ids + gm_ids))
    logging.info("Ladder size: %d summoners", len(all_ids))

    sample = random.sample(all_ids, min(SUMMONER_SAMPLE, len(all_ids)))
    # In-memory set tracks only IDs inserted this run so the same match_id
    # seen via multiple summoners doesn't trigger redundant API calls.
    inserted_this_run: set[str] = set()
    inserted = 0
    skipped = 0

    for puuid in sample:
        # Modern Riot API returns puuid directly from league endpoints.
        # If it's still a summonerId (older API), resolve it to puuid.
        if len(puuid) < 50:
            puuid = client.get_puuid_by_summon_id(puuid)
        if not puuid:
            continue

        match_ids = client.get_match_ids_by_puuid(puuid, count=MATCHES_PER_SUMMONER) or []
        for match_id in match_ids:
            if inserted >= MAX_INSERTS:
                logging.info("Reached MAX_INSERTS limit (%d), stopping.", MAX_INSERTS)
                break
            if match_id in inserted_this_run or match_id_exists(match_id):
                skipped += 1
                continue
            try:
                cached_insert(match_id)
                inserted_this_run.add(match_id)
                inserted += 1
                logging.info("Inserted %s", match_id)
            except Exception as e:
                logging.warning("Skipping %s: %s", match_id, e)

        if inserted >= MAX_INSERTS:
            break

    logging.info("Done. Inserted: %d, Already present: %d", inserted, skipped)


if __name__ == "__main__":
    main()
