import os
import logging
import json
from api_client import API_Client
from extract_data import *
from postgres_helperfile import create_postgres_engine

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def cached_insert(match_id, skip_timeline=False):
    logging.info("Starting main process for match ID: %s", match_id)
    api_client = API_Client()
    match_dto = api_client.get_match_by_match_id(match_id)

    if match_dto is None:
        raise Exception("Riot API call failed. Check API key.")

    save_to_cache(f"match_{match_id}.json", match_dto)

    if skip_timeline:
        match_timeline_dto = None
    else:
        match_timeline_dto = api_client.get_match_timeline(match_id)
        if match_timeline_dto is None:
            raise Exception("Riot API call failed. Check API key.")
        save_to_cache(f"timeline_{match_id}.json", match_timeline_dto)

    # try to insert
    try:
        insert_match(match_dto, match_timeline_dto)
    except Exception as e:
        logging.error("Failed to insert match data for match ID %s: %s", match_id, e)
        print(f"Failed to insert match data: {e}")
        raise

    # Upon successful insertion, clean up cache
    cleanup_cache(match_id)


def cleanup_cache(match_id):
    cache_dir = "./cache"
    match_file = os.path.join(cache_dir, f"match_{match_id}.json")
    timeline_file = os.path.join(cache_dir, f"timeline_{match_id}.json")

    try:
        if os.path.exists(match_file):
            os.remove(match_file)
            logging.info("Deleted cache file: %s", match_file)

        if os.path.exists(timeline_file):
            os.remove(timeline_file)
            logging.info("Deleted cache file: %s", timeline_file)
    except Exception as e:
        logging.error("Failed to clean up cache for match ID %s: %s", match_id, e)


def save_to_cache(filename, data):
    """Save data to a file in the cache directory."""
    cache_dir = "./cache"  # Change to a relative path
    os.makedirs(
        cache_dir, exist_ok=True
    )  # Create the cache directory if it doesn't exist
    file_path = os.path.join(cache_dir, filename)
    with open(file_path, "w") as file:
        json.dump(data, file)


def insert_match(match_dto, match_timeline_dto=None):
    data_match_id = match_dto.get("metadata").get("matchId")
    engine = create_postgres_engine()
    logging.info(
        "Inserting match data for %s match DTO and timeline DTO", data_match_id
    )

    # Function to handle the insertion and catch exceptions
    def try_insert(df, table_name):
        try:
            df.to_sql(table_name, engine, if_exists="append", index=False)
        except Exception as e:
            logging.warning(f"Insertion to {table_name} failed: {e}")

    try_insert(get_match_metadata(match_dto), "match_metadata")
    try_insert(get_participant_dto(match_dto), "participant_dto")
    try_insert(get_perk_style_selections(match_dto), "perk_style_selections")
    try_insert(get_teams(match_dto), "teams")
    try_insert(get_bans(match_dto), "bans")

    if match_timeline_dto is not None:
        try_insert(get_participant_frames(match_timeline_dto), "participant_frames")
        try_insert(get_champion_stats(match_timeline_dto), "champion_stats")
        try_insert(get_match_events(match_timeline_dto), "match_events")
        try_insert(get_victim_damage_dealt(match_timeline_dto), "victim_damage_dealt")
        try_insert(get_victim_damage_received(match_timeline_dto), "victim_damage_received")
        try_insert(get_damage_stats(match_timeline_dto), "damage_stats")

    logging.info("Data insertion for match %s completed successfully", data_match_id)
