from insert_match import get_champion_stats, get_bans, get_teams, get_match_metadata
from unittest import TestCase
import pytest
import json

from pathlib import Path
_FILES = Path(__file__).parent / "files"
match_timeline_data_filepath = _FILES / "NA1_4729149632_match_timeline.json"
match_data_filepath = _FILES / "NA1_4729149632_match_data.json"

# Load JSON data and create DTOs
with open(match_data_filepath, 'r') as file:
    match_json = json.load(file)

with open(match_timeline_data_filepath, 'r') as file:
    match_timeline_json = json.load(file)


class TestGetChampionStats(TestCase):
    def test_get_champion_stats(self):
        # DataFrame
        champion_stats = get_champion_stats(match_timeline_json)

        frame_number_to_extract = 3
        participant_id_to_extract = '1'

        sample_stats = champion_stats.loc[(champion_stats['frame_number'] == frame_number_to_extract) & 
                                  (champion_stats['participant_id'] == participant_id_to_extract)]
        
        self.assertFalse(sample_stats.empty, "The DataFrame 'sample_stats' is unexpectedly empty.")


        expected_length = len(match_timeline_json['info']['frames']) * len(match_timeline_json['info']['frames'][0]['participantFrames'])
        expected_cols = [
                        "match_id", "frame_number", "timestamp", "participant_id",
                        "ability_haste", "ability_power", "armor", "armor_pen", "armor_pen_percent",
                        "attack_damage", "attack_speed", "bonus_armor_pen_percent", "bonus_magic_pen_percent",
                        "cc_reduction", "cooldown_reduction", "health", "health_max", "health_regen", "lifesteal",
                        "magic_pen", "magic_pen_percent", "magic_resist", "movement_speed",
                        "omnivamp", "physical_vamp", "power", "power_max", "power_regen", "spell_vamp"
                        ]

        self.assertEqual(list(sample_stats.columns), expected_cols)
        self.assertEqual(len(champion_stats), expected_length)

        self.assertEqual(sample_stats['ability_haste'].iloc[0], 0)
        self.assertEqual(sample_stats['ability_power'].iloc[0], 0)
        self.assertEqual(sample_stats['armor'].iloc[0], 52)
        self.assertEqual(sample_stats['armor_pen'].iloc[0], 0)
        self.assertEqual(sample_stats['armor_pen_percent'].iloc[0], 0)
        self.assertEqual(sample_stats['attack_damage'].iloc[0], 95)
        self.assertEqual(sample_stats['attack_speed'].iloc[0], 170)
        self.assertEqual(sample_stats['bonus_armor_pen_percent'].iloc[0], 0)
        self.assertEqual(sample_stats['bonus_magic_pen_percent'].iloc[0], 0)
        self.assertEqual(sample_stats['cc_reduction'].iloc[0], 0)
        self.assertEqual(sample_stats['cooldown_reduction'].iloc[0], 0)
        self.assertEqual(sample_stats['health'].iloc[0], 724)
        self.assertEqual(sample_stats['health_max'].iloc[0], 915)
        self.assertEqual(sample_stats['health_regen'].iloc[0], 15)
        self.assertEqual(sample_stats['lifesteal'].iloc[0], 0.0)
        self.assertEqual(sample_stats['magic_pen'].iloc[0], 0)
        self.assertEqual(sample_stats['magic_pen_percent'].iloc[0], 0.0)
        self.assertEqual(sample_stats['magic_resist'].iloc[0], 53)
        self.assertEqual(sample_stats['movement_speed'].iloc[0], 340)
        self.assertEqual(sample_stats['omnivamp'].iloc[0], 0.0)
        self.assertEqual(sample_stats['physical_vamp'].iloc[0], 0.0)
        self.assertEqual(sample_stats['power'].iloc[0], 0)
        self.assertEqual(sample_stats['power_max'].iloc[0], 60)
        self.assertEqual(sample_stats['power_regen'].iloc[0], 0)
        self.assertEqual(sample_stats['spell_vamp'].iloc[0], 0.0)



class TestGetBansFunction(TestCase):
    def test_get_bans(self):

        # Expected output
        expected_bans = []

        # Call the function with the mock data
        actual_bans = get_bans(match_json)

        # Assert that the actual output matches the expected output
        self.assertEqual(actual_bans, expected_bans)



class TestGetTeams(TestCase):

    def test_get_teams(self):
        teams = get_teams(match_json)

        # Assert the basic structure
        self.assertEqual(len(teams), 2)

        # Assertions for team 1
        self.assertEqual(teams[0]['team_id'], 100)
        self.assertEqual(teams[0]['match_id'], "NA1_4729149632")
        self.assertFalse(teams[0]['baron_first'])
        self.assertEqual(teams[0]['baron_kills'], 0)
        self.assertTrue(teams[0]['champion_first'])
        self.assertEqual(teams[0]['champion_kills'], 33)
        self.assertFalse(teams[0]['dragon_first'])
        self.assertEqual(teams[0]['dragon_kills'], 0)
        self.assertFalse(teams[0]['inhibitor_first'])
        self.assertEqual(teams[0]['inhibitor_kills'], 0)
        self.assertFalse(teams[0]['rift_herald_first'])
        self.assertEqual(teams[0]['rift_herald_kills'], 0)
        self.assertFalse(teams[0]['tower_first'])
        self.assertEqual(teams[0]['tower_kills'], 1)
        self.assertFalse(teams[0]['win'])

        # Assertions for team 2
        self.assertEqual(teams[1]['team_id'], 200)
        self.assertEqual(teams[1]['match_id'], "NA1_4729149632")
        self.assertFalse(teams[1]['baron_first'])
        self.assertEqual(teams[1]['baron_kills'], 0)
        self.assertFalse(teams[1]['champion_first'])
        self.assertEqual(teams[1]['champion_kills'], 76)
        self.assertFalse(teams[1]['dragon_first'])
        self.assertEqual(teams[1]['dragon_kills'], 0)
        self.assertTrue(teams[1]['inhibitor_first'])
        self.assertEqual(teams[1]['inhibitor_kills'], 1)
        self.assertFalse(teams[1]['rift_herald_first'])
        self.assertEqual(teams[1]['rift_herald_kills'], 0)
        self.assertTrue(teams[1]['tower_first'])
        self.assertEqual(teams[1]['tower_kills'], 4)
        self.assertTrue(teams[1]['win'])


class TestGetMatchMetadata(TestCase):

    def test_get_match_metadata(self):
        match_metadata = get_match_metadata(match_json)

        self.assertEqual(match_metadata['match_id'], 'NA1_4729149632')
        self.assertEqual(match_metadata['data_version'],'2')
        self.assertEqual(match_metadata['game_creation'],1690599967579)
        self.assertEqual(match_metadata['game_duration'],1178)
        self.assertEqual(match_metadata['game_end_timestamp'],1690601198047)
        self.assertEqual(match_metadata['game_id'],4729149632)
        self.assertEqual(match_metadata['game_mode'],'ARAM')
        self.assertEqual(match_metadata['game_name'],'teambuilder-match-4729149632')
        self.assertEqual(match_metadata['game_start_timestamp'],1690600019437)
        self.assertEqual(match_metadata['game_type'],'MATCHED_GAME')
        self.assertEqual(match_metadata['game_version'],'13.14.522.7601')
        self.assertEqual(match_metadata['map_id'],12)
        self.assertEqual(match_metadata['platform_id'],'NA1')
        self.assertEqual(match_metadata['queue_id'],450)
        self.assertEqual(match_metadata['tournament_code'],'')


