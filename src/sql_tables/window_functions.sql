-- ============================================================
-- champion_winrates
-- Rolling 7-day win rate and pick count per champion.
-- ============================================================
-- champion_winrates
WITH daily AS (
    SELECT
        DATE_TRUNC('day', TO_TIMESTAMP(m.game_creation / 1000))::date AS day,
        p.champion_name,
        COUNT(*)        AS games,
        SUM(p.win::int) AS wins
    FROM participant_dto p
    JOIN match_metadata m USING (match_id)
    GROUP BY 1, 2
)
SELECT
    day,
    champion_name,
    games,
    ROUND(wins::numeric / NULLIF(games, 0) * 100, 1)                            AS winrate_pct,
    SUM(games) OVER w                                                            AS rolling_7d_games,
    ROUND(SUM(wins)::numeric / NULLIF(SUM(games) OVER w, 0) * 100, 1)          AS rolling_7d_winrate
FROM daily
WINDOW w AS (
    PARTITION BY champion_name
    ORDER BY day
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
)
ORDER BY day DESC, rolling_7d_games DESC;


-- ============================================================
-- pick_rate_trend
-- Rolling 7-day pick rate (%) per champion, normalized by
-- total available player slots (10 per match).
-- ============================================================
-- pick_rate_trend
WITH totals AS (
    SELECT
        DATE_TRUNC('day', TO_TIMESTAMP(game_creation / 1000))::date AS day,
        COUNT(DISTINCT match_id) * 10 AS total_slots
    FROM match_metadata
    GROUP BY 1
),
picks AS (
    SELECT
        DATE_TRUNC('day', TO_TIMESTAMP(m.game_creation / 1000))::date AS day,
        p.champion_name,
        COUNT(*) AS picks
    FROM participant_dto p
    JOIN match_metadata m USING (match_id)
    GROUP BY 1, 2
)
SELECT
    p.day,
    p.champion_name,
    p.picks,
    ROUND(p.picks::numeric / NULLIF(t.total_slots, 0) * 100, 2) AS pick_rate_pct,
    ROUND(
        AVG(p.picks::numeric / NULLIF(t.total_slots, 0)) OVER (
            PARTITION BY p.champion_name
            ORDER BY p.day
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) * 100, 2
    ) AS rolling_7d_pick_rate
FROM picks p
JOIN totals t USING (day)
ORDER BY p.day DESC, rolling_7d_pick_rate DESC;


-- ============================================================
-- item_winrates
-- Weekly win rate and popularity rank for each item.
-- Unnests item0-item5 columns into individual rows.
-- ============================================================
-- item_winrates
WITH item_rows AS (
    SELECT
        DATE_TRUNC('week', TO_TIMESTAMP(m.game_creation / 1000))::date AS week,
        p.win::int AS win,
        unnest(ARRAY[p.item0, p.item1, p.item2, p.item3, p.item4, p.item5]) AS item_id
    FROM participant_dto p
    JOIN match_metadata m USING (match_id)
)
SELECT
    week,
    item_id,
    COUNT(*)                                                  AS games_with_item,
    ROUND(AVG(win) * 100, 1)                                 AS winrate_pct,
    RANK() OVER (PARTITION BY week ORDER BY COUNT(*) DESC)   AS popularity_rank
FROM item_rows
WHERE item_id IS NOT NULL AND item_id != 0
GROUP BY week, item_id
ORDER BY week DESC, games_with_item DESC;


-- ============================================================
-- meta_trend
-- Weekly champion pick rank + win rate rank, with
-- pick_rank_delta showing week-over-week rise/fall.
-- ============================================================
-- meta_trend
WITH weekly AS (
    SELECT
        DATE_TRUNC('week', TO_TIMESTAMP(m.game_creation / 1000))::date AS week,
        p.champion_name,
        COUNT(*)        AS games,
        AVG(p.win::int) AS winrate
    FROM participant_dto p
    JOIN match_metadata m USING (match_id)
    GROUP BY 1, 2
),
ranked AS (
    SELECT
        week,
        champion_name,
        games,
        ROUND(winrate * 100, 1)                                    AS winrate_pct,
        RANK() OVER (PARTITION BY week ORDER BY games DESC)        AS pick_rank,
        RANK() OVER (PARTITION BY week ORDER BY winrate DESC)      AS wr_rank
    FROM weekly
)
SELECT
    week,
    champion_name,
    games,
    winrate_pct,
    pick_rank,
    wr_rank,
    pick_rank - LAG(pick_rank) OVER (
        PARTITION BY champion_name ORDER BY week
    ) AS pick_rank_delta
FROM ranked
ORDER BY week DESC, pick_rank;
