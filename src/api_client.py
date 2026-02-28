import os
import time
import logging
import requests


from dotenv import load_dotenv

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class RateLimitExceededError(Exception):
    pass


class APIKeyExpiredError(Exception):
    def __init__(self, message="API key has expired"):
        super().__init__(message)


class RateLimiter:
    def __init__(self, max_requests, period):
        self.max_requests = max_requests
        self.period = period
        self.timestamps = []

    def __call__(self):
        now = time.time()
        self.timestamps = [ts for ts in self.timestamps if ts > now - self.period]

        if len(self.timestamps) < self.max_requests:
            self.timestamps.append(now)
        else:
            oldest_request = min(self.timestamps)
            time_to_wait = self.period - (now - oldest_request)
            time.sleep(time_to_wait)
            self.timestamps.append(time.time())


rl_sec = RateLimiter(20, 1)  # 20 requests per 1 second
rl_min = RateLimiter(100, 120)  # 100 requests per 2 minutes


class API_Client:
    def __init__(self):
        load_dotenv(".env", verbose=True)  # Construct the correct path
        self.api_key = os.environ.get("RIOT_API_KEY")
        if not self.api_key:
            logging.error("API key is not set in environment variables")
            raise Exception("API key is not set in environment variables")
        logging.debug("API key loaded")

    def _make_request(self, url, timeout=2):
        logging.info("Making request to URL: %s", url)

        # Enforce rate limiting before making a request
        rl_sec()
        rl_min()

        headers = {"X-Riot-Token": self.api_key}

        # Common code to make an HTTP request to the API
        try:
            response = requests.get(url, headers=headers, timeout=2)
            response.raise_for_status()  # Raises HTTPError for 4xx/5xx responses

            return response.json()

        except requests.exceptions.HTTPError as e:
            if response.status_code == 403:
                logging.error("403 Forbidden: API key may have expired.")
                raise APIKeyExpiredError("403: Riot API key expired.") from e

            if response.status_code == 429:
                logging.error("429 Too Many Requests: Rate limit exceeded.")
                raise RateLimitExceededError(
                    "429: Rate limited. Too many API calls recently."
                ) from e

            logging.error("HTTP error occurred: %s", e)
            return None

        except requests.exceptions.Timeout:
            logging.error("Request timed out for URL: %s", url)
            return None

        except requests.exceptions.RequestException as e:
            logging.error("Request exception for URL: %s - %s", url, e)
            return None

        except Exception as e:
            logging.error(
                "An unexpected error occurred during request to %s: %s", url, e
            )
            return None

    def get_summoner_by_name(self, summoner_name):
        logging.info("Fetching summoner data for: %s", summoner_name)
        summoner_name_encoded = summoner_name.strip().replace(" ", "%20")
        url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name_encoded}"
        response = self._make_request(url, timeout=5)
        return response if response else None

    def get_match_ids_by_puuid(self, puuid, start=0, count=20):
        logging.info("Fetching match IDs for PUUID: %s", puuid)
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
        response = self._make_request(url, timeout=5)
        return response if response else None

    def get_match_by_match_id(self, match_id):
        logging.info("Fetching match data for match ID: %s", match_id)
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
        response = self._make_request(url, timeout=5)
        return response if response else None

    def get_match_timeline(self, match_id):
        logging.info("Fetching match timeline for match ID: %s", match_id)
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
        response = self._make_request(url, timeout=5)
        return response if response else None

    def get_puuid_by_summon_id(self, summoner_id):
        logging.info("Fetching PUUID for summoner ID: %s", summoner_id)
        url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}"
        response = self._make_request(url, timeout=5)
        return response["puuid"] if response else None

    def get_summoner_ids_from_league_id(self, league_id):
        logging.info("Fetching summoner IDs for league ID: %s", league_id)
        url = f"https://na1.api.riotgames.com/lol/league/v4/leagues/{league_id}"
        response = self._make_request(url, timeout=5)
        if response:
            summoner_ids = [entry["summonerId"] for entry in response["entries"]]
            return summoner_ids
        else:
            return None

    def get_challenger_league(self, queue="RANKED_SOLO_5x5"):
        logging.info("Fetching Challenger league for queue: %s", queue)
        url = f"https://na1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/{queue}"
        response = self._make_request(url, timeout=5)
        if response:
            return [entry["summonerId"] for entry in response["entries"]]
        return None

    def get_grandmaster_league(self, queue="RANKED_SOLO_5x5"):
        logging.info("Fetching GrandMaster league for queue: %s", queue)
        url = f"https://na1.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/{queue}"
        response = self._make_request(url, timeout=5)
        if response:
            return [entry["summonerId"] for entry in response["entries"]]
        return None
