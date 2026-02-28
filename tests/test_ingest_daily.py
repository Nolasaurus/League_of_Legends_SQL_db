"""
Unit tests for ingest_daily.py.

All external I/O (Riot API, DB) is mocked so these run locally without
credentials or a live database.
"""
from unittest.mock import MagicMock, patch

import pytest

from ingest_daily import _bar, _eta, main, MAX_INSERTS, MATCHES_PER_SUMMONER


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _puuids(n: int) -> list:
    """Return n fake 78-char PUUIDs (long enough to skip summonerId resolution)."""
    return [f"{'x' * 72}{i:06d}" for i in range(n)]


def _match_ids(prefix: str, n: int) -> list:
    return [f"NA1_{prefix}_{i}" for i in range(n)]


def _make_client(challenger_puuids, match_ids_by_puuid=None):
    """Return a mocked API_Client with sensible defaults."""
    client = MagicMock()
    client.get_challenger_league.return_value = challenger_puuids
    client.get_grandmaster_league.return_value = []
    if match_ids_by_puuid is None:
        client.get_match_ids_by_puuid.return_value = _match_ids("default", MATCHES_PER_SUMMONER)
    else:
        client.get_match_ids_by_puuid.side_effect = match_ids_by_puuid
    return client


# Patch targets shared by all main() tests.
# connect_db is called directly in main() for the persistent readonly connection.
# existing_in_db takes (cursor, match_ids) and returns a set — default empty.
_COMMON_PATCHES = [
    ("ingest_daily.ensure_schema", {}),
    ("ingest_daily.connect_db", {}),          # returns a MagicMock with .cursor()/.close()
    ("ingest_daily.existing_in_db", {"return_value": set()}),
    ("ingest_daily.cached_insert", {}),
]


# ---------------------------------------------------------------------------
# _bar
# ---------------------------------------------------------------------------

def test_bar_empty():
    result = _bar(0, 10)
    assert "0/10" in result
    assert result.startswith("[")


def test_bar_full():
    result = _bar(10, 10)
    assert "10/10" in result
    inner = result[1: result.index("]")]
    assert " " not in inner


def test_bar_partial():
    result = _bar(5, 10)
    assert "5/10" in result


def test_bar_zero_total_no_crash():
    _bar(0, 0)


# ---------------------------------------------------------------------------
# _eta
# ---------------------------------------------------------------------------

def test_eta_no_inserts_yet():
    assert _eta(0, 10) == "ETA=?"


def test_eta_zero_elapsed():
    assert _eta(5, 0) == "ETA=?"


def test_eta_format():
    result = _eta(500, 250)
    assert "m" in result
    assert "s" in result


def test_eta_at_limit():
    result = _eta(MAX_INSERTS, 300)
    assert "0m00s" in result


# ---------------------------------------------------------------------------
# main() — happy path
# ---------------------------------------------------------------------------

@patch("ingest_daily.ensure_schema")
@patch("ingest_daily.connect_db")
@patch("ingest_daily.existing_in_db", return_value=set())
@patch("ingest_daily.cached_insert")
@patch("ingest_daily.API_Client")
def test_inserts_new_matches(MockClient, mock_insert, _exists, _conn, _schema):
    puuids = _puuids(2)
    MockClient.return_value = _make_client(
        challenger_puuids=puuids,
        match_ids_by_puuid=lambda p, count: _match_ids(p[-4:], count),
    )

    main()

    assert mock_insert.call_count == 2 * MATCHES_PER_SUMMONER


# ---------------------------------------------------------------------------
# Skipping existing matches
# ---------------------------------------------------------------------------

@patch("ingest_daily.ensure_schema")
@patch("ingest_daily.connect_db")
@patch("ingest_daily.existing_in_db", side_effect=lambda cur, ids: set(ids))
@patch("ingest_daily.cached_insert")
@patch("ingest_daily.API_Client")
def test_skips_existing_matches(MockClient, mock_insert, _exists, _conn, _schema):
    """When existing_in_db returns all candidates as already present, nothing is inserted."""
    MockClient.return_value = _make_client(_puuids(3))

    main()

    mock_insert.assert_not_called()


# ---------------------------------------------------------------------------
# Deduplication within a single run
# ---------------------------------------------------------------------------

@patch("ingest_daily.ensure_schema")
@patch("ingest_daily.connect_db")
@patch("ingest_daily.existing_in_db", return_value=set())
@patch("ingest_daily.cached_insert")
@patch("ingest_daily.API_Client")
def test_deduplication_within_run(MockClient, mock_insert, _exists, _conn, _schema):
    """Same match IDs from multiple summoners are inserted exactly once."""
    shared_ids = _match_ids("shared", MATCHES_PER_SUMMONER)
    MockClient.return_value = _make_client(
        challenger_puuids=_puuids(3),
        match_ids_by_puuid=lambda p, count: shared_ids,
    )

    main()

    assert mock_insert.call_count == len(shared_ids)


# ---------------------------------------------------------------------------
# MAX_INSERTS cap
# ---------------------------------------------------------------------------

@patch("ingest_daily.ensure_schema")
@patch("ingest_daily.connect_db")
@patch("ingest_daily.existing_in_db", return_value=set())
@patch("ingest_daily.cached_insert")
@patch("ingest_daily.API_Client")
def test_max_inserts_cap(MockClient, mock_insert, _exists, _conn, _schema):
    """Insert count never exceeds MAX_INSERTS even with unlimited candidates."""
    def per_summoner_ids(puuid, count):
        return _match_ids(puuid[-4:], MAX_INSERTS + 50)

    MockClient.return_value = _make_client(
        challenger_puuids=_puuids(5),
        match_ids_by_puuid=per_summoner_ids,
    )

    main()

    assert mock_insert.call_count == MAX_INSERTS


# ---------------------------------------------------------------------------
# Error resilience
# ---------------------------------------------------------------------------

@patch("ingest_daily.ensure_schema")
@patch("ingest_daily.connect_db")
@patch("ingest_daily.existing_in_db", return_value=set())
@patch("ingest_daily.cached_insert", side_effect=RuntimeError("DB error"))
@patch("ingest_daily.API_Client")
def test_failed_insert_continues(MockClient, mock_insert, _exists, _conn, _schema):
    """An exception from cached_insert skips the match but does not abort the run."""
    MockClient.return_value = _make_client(
        challenger_puuids=_puuids(1),
        match_ids_by_puuid=lambda p, count: _match_ids("err", 3),
    )

    main()  # must not raise

    assert mock_insert.call_count == 3


# ---------------------------------------------------------------------------
# Schema is applied before any API call
# ---------------------------------------------------------------------------

@patch("ingest_daily.ensure_schema")
@patch("ingest_daily.connect_db")
@patch("ingest_daily.existing_in_db", return_value=set())
@patch("ingest_daily.cached_insert")
@patch("ingest_daily.API_Client")
def test_schema_applied_before_api(MockClient, _insert, _exists, _conn, mock_schema):
    call_order = []
    mock_schema.side_effect = lambda: call_order.append("schema")
    MockClient.return_value.get_challenger_league.side_effect = lambda: call_order.append("api") or []
    MockClient.return_value.get_grandmaster_league.return_value = []

    main()

    assert call_order[0] == "schema"
    assert "api" in call_order