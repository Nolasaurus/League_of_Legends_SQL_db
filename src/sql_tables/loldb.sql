CREATE TABLE IF NOT EXISTS "match_metadata" (
  "data_version" VARCHAR(255),
  "match_id" VARCHAR(255) PRIMARY KEY,
  "game_creation" BIGINT,
  "game_duration" BIGINT,
  "game_end_timestamp" BIGINT,
  "game_id" BIGINT,
  "game_mode" VARCHAR(255),
  "game_name" VARCHAR(255),
  "game_start_timestamp" BIGINT,
  "game_type" VARCHAR(255),
  "game_version" VARCHAR(255),
  "map_id" INT,
  "platform_id" VARCHAR(255),
  "queue_id" INT,
  "tournament_code" VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS "participant_dto" (
  "match_id" VARCHAR(255),
  "participant_id" INT,
  "assists" INT,
  "baron_kills" INT,
  "bounty_level" INT,
  "champ_experience" INT,
  "champ_level" INT,
  "champion_id" INT,
  "champion_name" VARCHAR(255),
  "champion_transform" INT,
  "consumables_purchased" INT,
  "damage_dealt_to_buildings" INT,
  "damage_dealt_to_objectives" INT,
  "damage_dealt_to_turrets" INT,
  "damage_self_mitigated" INT,
  "deaths" INT,
  "detector_wards_placed" INT,
  "double_kills" INT,
  "dragon_kills" INT,
  "first_blood_assist" BOOLEAN,
  "first_blood_kill" BOOLEAN,
  "first_tower_assist" BOOLEAN,
  "first_tower_kill" BOOLEAN,
  "game_ended_in_early_surrender" BOOLEAN,
  "game_ended_in_surrender" BOOLEAN,
  "gold_earned" INT,
  "gold_spent" INT,
  "individual_position" VARCHAR(255),
  "inhibitor_kills" INT,
  "inhibitor_takedowns" INT,
  "inhibitors_lost" INT,
  "item0" INT,
  "item1" INT,
  "item2" INT,
  "item3" INT,
  "item4" INT,
  "item5" INT,
  "item6" INT,
  "items_purchased" INT,
  "killing_sprees" INT,
  "kills" INT,
  "lane" VARCHAR(255),
  "largest_critical_strike" INT,
  "largest_killing_spree" INT,
  "largest_multi_kill" INT,
  "longest_time_spent_living" INT,
  "magic_damage_dealt" INT,
  "magic_damage_dealt_to_champions" INT,
  "magic_damage_taken" INT,
  "neutral_minions_killed" INT,
  "nexus_kills" INT,
  "nexus_takedowns" INT,
  "nexus_lost" INT,
  "objectives_stolen" INT,
  "objectives_stolen_assists" INT,
  "penta_kills" INT,
  "physical_damage_dealt" INT,
  "physical_damage_dealt_to_champions" INT,
  "physical_damage_taken" INT,
  "profile_icon" INT,
  "puuid" VARCHAR(255),
  "quadra_kills" INT,
  "riot_id_name" VARCHAR(255),
  "riot_id_tagline" VARCHAR(255),
  "role" VARCHAR(255),
  "sight_wards_bought_in_game" INT,
  "spell1_casts" INT,
  "spell2_casts" INT,
  "spell3_casts" INT,
  "spell4_casts" INT,
  "summoner1_casts" INT,
  "summoner1_id" INT,
  "summoner2_casts" INT,
  "summoner2_id" INT,
  "summoner_id" VARCHAR(255),
  "summoner_level" INT,
  "summoner_name" VARCHAR(255),
  "team_early_surrendered" BOOLEAN,
  "team_id" INT,
  "team_position" VARCHAR(255),
  "time_ccing_others" INT,
  "time_played" INT,
  "total_damage_dealt" INT,
  "total_damage_dealt_to_champions" INT,
  "total_damage_shielded_on_teammates" INT,
  "total_damage_taken" INT,
  "total_heal" INT,
  "total_heals_on_teammates" INT,
  "total_minions_killed" INT,
  "total_time_cc_dealt" INT,
  "total_time_spent_dead" INT,
  "total_units_healed" INT,
  "triple_kills" INT,
  "true_damage_dealt" INT,
  "true_damage_dealt_to_champions" INT,
  "true_damage_taken" INT,
  "turret_kills" INT,
  "turret_takedowns" INT,
  "turrets_lost" INT,
  "unreal_kills" INT,
  "vision_score" INT,
  "vision_wards_bought_in_game" INT,
  "wards_killed" INT,
  "wards_placed" INT,
  "win" BOOLEAN,
  "perks_defense" INT,
  "perks_flex" INT,
  "perks_offense" INT,
  PRIMARY KEY ("match_id", "participant_id")
);

CREATE TABLE IF NOT EXISTS "perk_style_selections" (
  "match_id" VARCHAR(255),
  "participant_id" INT,
  "perk" INT,
  "var1" INT,
  "var2" INT,
  "var3" INT,
  "perks_description" VARCHAR(255),
  "perks_style" INT,
  PRIMARY KEY ("match_id", "participant_id", "perks_style")
);

CREATE TABLE IF NOT EXISTS "challenges" (
  "match_id" VARCHAR(255),
  "participant_id" INT,
  "assist_streak_count" INT,
  "ability_uses" INT,
  "aces_before_15_minutes" INT,
  "allied_jungle_monster_kills" INT,
  "baron_takedowns" INT,
  "blast_cone_opposite_opponent_count" INT,
  "bounty_gold" INT,
  "buffs_stolen" INT,
  "complete_support_quest_in_time" INT,
  "control_wards_placed" INT,
  "damage_per_minute" FLOAT,
  "damage_taken_on_team_percentage" FLOAT,
  "danced_with_rift_herald" INT,
  "deaths_by_enemy_champs" INT,
  "dodge_skill_shots_small_window" INT,
  "double_aces" INT,
  "dragon_takedowns" INT,
  "early_laning_phase_gold_exp_advantage" FLOAT,
  "effective_heal_and_shielding" INT,
  "elder_dragon_kills_with_opposing_soul" INT,
  "elder_dragon_multikills" INT,
  "enemy_champion_immobilizations" INT,
  "enemy_jungle_monster_kills" INT,
  "epic_monster_kills_near_enemy_jungler" INT,
  "epic_monster_kills_within_30_seconds_of_spawn" INT,
  "epic_monster_steals" INT,
  "epic_monster_stolen_without_smite" INT,
  "first_turret_killed" INT,
  "flawless_aces" INT,
  "full_team_takedown" INT,
  "game_length" FLOAT,
  "get_takedowns_in_all_lanes_early_jungle_as_laner" INT,
  "gold_per_minute" FLOAT,
  "had_open_nexus" INT,
  "immobilize_and_kill_with_ally" INT,
  "initial_buff_count" INT,
  "initial_crab_count" INT,
  "jungle_cs_before_10_minutes" INT,
  "jungler_takedowns_near_damaged_epic_monster" INT,
  "k_turrets_destroyed_before_plates_fall" INT,
  "kda" FLOAT,
  "kill_after_hidden_with_ally" INT,
  "kill_participation" FLOAT,
  "killed_champ_took_full_team_damage_survived" INT,
  "killing_sprees" INT,
  "kills_near_enemy_turret" INT,
  "kills_on_other_lanes_early_jungle_as_laner" INT,
  "kills_on_recently_healed_by_aram_pack" INT,
  "kills_under_own_turret" INT,
  "kills_with_help_from_epic_monster" INT,
  "knock_enemy_into_team_and_kill" INT,
  "land_skill_shots_early_game" INT,
  "lane_minions_first_10_minutes" INT,
  "laning_phase_gold_exp_advantage" FLOAT,
  "legendary_count" INT,
  "lost_an_inhibitor" INT,
  "max_cs_advantage_on_lane_opponent" INT,
  "max_kill_deficit" INT,
  "max_level_lead_lane_opponent" INT,
  "mejais_full_stack_in_time" INT,
  "more_enemy_jungle_than_opponent" INT,
  "multi_kill_one_spell" INT,
  "multi_turret_rift_herald_count" INT,
  "multikills" INT,
  "multikills_after_aggressive_flash" INT,
  "mythic_item_used" INT,
  "outer_turret_executes_before_10_minutes" INT,
  "outnumbered_kills" INT,
  "outnumbered_nexus_kill" INT,
  "perfect_dragon_souls_taken" INT,
  "perfect_game" INT,
  "pick_kill_with_ally" INT,
  "poro_explosions" INT,
  "quick_cleanse" INT,
  "quick_first_turret" INT,
  "quick_solo_kills" INT,
  "rift_herald_takedowns" INT,
  "save_ally_from_death" INT,
  "scuttle_crab_kills" INT,
  "skillshots_dodged" INT,
  "skillshots_hit" INT,
  "snowballs_hit" INT,
  "solo_baron_kills" INT,
  "solo_kills" INT,
  "stealth_wards_placed" INT,
  "survived_single_digit_hp_count" INT,
  "survived_three_immobilizes_in_fight" INT,
  "takedown_on_first_turret" INT,
  "takedowns" INT,
  "takedowns_after_gaining_level_advantage" INT,
  "takedowns_before_jungle_minion_spawn" INT,
  "takedowns_first_x_minutes" INT,
  "takedowns_in_alcove" INT,
  "takedowns_in_enemy_fountain" INT,
  "team_baron_kills" INT,
  "team_damage_percentage" FLOAT,
  "team_elder_dragon_kills" INT,
  "team_rift_herald_kills" INT,
  "took_large_damage_survived" INT,
  "turret_plates_taken" INT,
  "turret_takedowns" INT,
  "turrets_taken_with_rift_herald" INT,
  "twenty_minions_in_3_seconds_count" INT,
  "two_wards_one_sweeper_count" INT,
  "unseen_recalls" INT,
  "vision_score_advantage_lane_opponent" INT,
  "vision_score_per_minute" FLOAT,
  "ward_takedowns" INT,
  "ward_takedowns_before_20m" INT,
  "wards_guarded" INT,
  PRIMARY KEY ("match_id", "participant_id")
);

-- CREATE TABLE IF NOT EXISTS "participant_frames" (
--   "match_id" VARCHAR(255),
--   "participant_id" INT,
--   "frame_number" INT,
--   "timestamp" BIGINT,
--   "level" INT,
--   "current_gold" INT,
--   "gold_per_second" INT,
--   "total_gold" INT,
--   "xp" INT,
--   "minions_killed" INT,
--   "jungle_minions_killed" INT,
--   "time_enemy_spent_controlled" INT,
--   "position_x" INT,
--   "position_y" INT,
--   PRIMARY KEY ("match_id", "frame_number", "participant_id")
-- );

-- CREATE TABLE IF NOT EXISTS "champion_stats" (
--   "match_id" VARCHAR(255),
--   "frame_number" INT,
--   "participant_id" INT,
--   "ability_haste" INT,
--   "ability_power" INT,
--   "armor" INT,
--   "armor_pen" INT,
--   "armor_pen_percent" FLOAT,
--   "attack_damage" INT,
--   "attack_speed" FLOAT,
--   "bonus_armor_pen_percent" FLOAT,
--   "bonus_magic_pen_percent" FLOAT,
--   "cc_reduction" INT,
--   "cooldown_reduction" INT,
--   "health" INT,
--   "health_max" INT,
--   "health_regen" INT,
--   "lifesteal" FLOAT,
--   "magic_pen" INT,
--   "magic_pen_percent" FLOAT,
--   "magic_resist" INT,
--   "movement_speed" INT,
--   "omnivamp" FLOAT,
--   "physical_vamp" FLOAT,
--   "power" INT,
--   "power_max" INT,
--   "power_regen" INT,
--   "spell_vamp" FLOAT,
--   PRIMARY KEY ("match_id", "frame_number", "participant_id")
-- );

-- CREATE TABLE IF NOT EXISTS "match_events" (
--   "match_id" VARCHAR(255),
--   "frame_number" INT,
--   "event_number" INT,
--   "real_timestamp" BIGINT,
--   "timestamp" BIGINT,
--   "type" VARCHAR(255),
--   "item_id" INT,
--   "participant_id" INT,
--   "level_up_type" VARCHAR(255),
--   "skill_slot" INT,
--   "creator_id" INT,
--   "ward_type" VARCHAR(255),
--   "level" INT,
--   "bounty" INT,
--   "kill_streak_length" INT,
--   "killer_id" INT,
--   "position_x" INT,
--   "position_y" INT,
--   "victim_id" INT,
--   "kill_type" VARCHAR(255),
--   "lane_type" VARCHAR(255),
--   "team_id" INT,
--   "multi_kill_length" INT,
--   "killer_team_id" INT,
--   "monster_type" VARCHAR(255),
--   "monster_sub_type" VARCHAR(255),
--   "building_type" VARCHAR(255),
--   "tower_type" VARCHAR(255),
--   "after_id" INT,
--   "before_id" INT,
--   "gold_gain" INT,
--   "game_id" BIGINT,
--   "winning_team" INT,
--   "transform_type" VARCHAR(255),
--   "name" VARCHAR(255),
--   "shutdown_bounty" INT,
--   "actual_start_time" BIGINT,
--   PRIMARY KEY ("match_id", "frame_number", "event_number")
-- );

-- CREATE TABLE IF NOT EXISTS "victim_damage_dealt" (
--   "match_id" VARCHAR(255),
--   "frame_number" INT,
--   "event_number" INT,
--   "damage_number" INT,
--   "participant_id" INT,
--   "basic" BOOLEAN,
--   "magic_damage" INT,
--   "physical_damage" INT,
--   "name" VARCHAR(255),
--   "spell_name" VARCHAR(255),
--   "spell_slot" INT,
--   "true_damage" INT,
--   "type" VARCHAR(255),
--   PRIMARY KEY ("match_id", "frame_number", "event_number", "damage_number")
-- );

-- CREATE TABLE IF NOT EXISTS "victim_damage_received" (
--   "match_id" VARCHAR(255),
--   "frame_number" INT,
--   "event_number" INT,
--   "damage_number" INT,
--   "participant_id" INT,
--   "basic" BOOLEAN,
--   "magic_damage" INT,
--   "physical_damage" INT,
--   "name" VARCHAR(255),
--   "spell_name" VARCHAR(255),
--   "spell_slot" INT,
--   "true_damage" INT,
--   "type" VARCHAR(255),
--   PRIMARY KEY ("match_id", "frame_number", "event_number", "damage_number")
-- );

-- CREATE TABLE IF NOT EXISTS "damage_stats" (
--   "match_id" VARCHAR(255),
--   "frame_number" INT,
--   "participant_id" INT,
--   "magic_damage_done" INT,
--   "magic_damage_done_to_champions" INT,
--   "magic_damage_taken" INT,
--   "physical_damage_done" INT,
--   "physical_damage_done_to_champions" INT,
--   "physical_damage_taken" INT,
--   "total_damage_done" INT,
--   "total_damage_done_to_champions" INT,
--   "total_damage_taken" INT,
--   "true_damage_done" INT,
--   "true_damage_done_to_champions" INT,
--   "true_damage_taken" INT,
--   PRIMARY KEY ("match_id", "participant_id", "frame_number")
-- );

CREATE TABLE IF NOT EXISTS "teams" (
  "team_id" INT,
  "match_id" VARCHAR(255),
  "baron_first" BOOLEAN,
  "baron_kills" INT,
  "champion_first" BOOLEAN,
  "champion_kills" INT,
  "dragon_first" BOOLEAN,
  "dragon_kills" INT,
  "inhibitor_first" BOOLEAN,
  "inhibitor_kills" INT,
  "rift_herald_first" BOOLEAN,
  "rift_herald_kills" INT,
  "tower_first" BOOLEAN,
  "tower_kills" INT,
  "win" BOOLEAN,
  PRIMARY KEY ("match_id", "team_id")
);

CREATE TABLE IF NOT EXISTS "bans" (
  "match_id" VARCHAR(255),
  "champion_id" INT,
  "pick_turn" INT,
  PRIMARY KEY ("match_id", "pick_turn")
);

-- Foreign keys (skipped silently if already present)
DO $$ BEGIN
  ALTER TABLE "participant_dto" ADD FOREIGN KEY ("match_id") REFERENCES "match_metadata" ("match_id");
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- DO $$ BEGIN
--   ALTER TABLE "match_events" ADD FOREIGN KEY ("match_id") REFERENCES "match_metadata" ("match_id");
-- EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  ALTER TABLE "teams" ADD FOREIGN KEY ("match_id") REFERENCES "match_metadata" ("match_id");
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- DO $$ BEGIN
--   ALTER TABLE "challenges" ADD FOREIGN KEY ("match_id", "participant_id") REFERENCES "participant_dto" ("match_id", "participant_id");
-- EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  ALTER TABLE "perk_style_selections" ADD FOREIGN KEY ("match_id", "participant_id") REFERENCES "participant_dto" ("match_id", "participant_id");
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- DO $$ BEGIN
--   ALTER TABLE "victim_damage_dealt" ADD FOREIGN KEY ("match_id", "frame_number", "event_number") REFERENCES "match_events" ("match_id", "frame_number", "event_number");
-- EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- DO $$ BEGIN
--   ALTER TABLE "victim_damage_received" ADD FOREIGN KEY ("match_id", "frame_number", "event_number") REFERENCES "match_events" ("match_id", "frame_number", "event_number");
-- EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- DO $$ BEGIN
--   ALTER TABLE "champion_stats" ADD FOREIGN KEY ("match_id", "frame_number", "participant_id") REFERENCES "participant_frames" ("match_id", "frame_number", "participant_id");
-- EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- DO $$ BEGIN
--   ALTER TABLE "damage_stats" ADD FOREIGN KEY ("match_id", "frame_number", "participant_id") REFERENCES "participant_frames" ("match_id", "frame_number", "participant_id");
-- EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Schema migrations: add new columns to existing tables if not present
ALTER TABLE "match_metadata" ADD COLUMN IF NOT EXISTS "end_of_game_result" VARCHAR(255);

ALTER TABLE "participant_dto" ADD COLUMN IF NOT EXISTS "riot_id_game_name" VARCHAR(255);
ALTER TABLE "participant_dto" ADD COLUMN IF NOT EXISTS "damage_dealt_to_epic_monsters" INT;
ALTER TABLE "participant_dto" ADD COLUMN IF NOT EXISTS "retreat_pings" INT;
ALTER TABLE "participant_dto" ADD COLUMN IF NOT EXISTS "player_augment5" INT;
ALTER TABLE "participant_dto" ADD COLUMN IF NOT EXISTS "player_augment6" INT;
ALTER TABLE "participant_dto" ADD COLUMN IF NOT EXISTS "role_bound_item" INT;

-- ALTER TABLE "challenges" ADD COLUMN IF NOT EXISTS "earliest_baron" FLOAT;
-- ALTER TABLE "challenges" ADD COLUMN IF NOT EXISTS "earliest_dragon_takedown" FLOAT;
-- ALTER TABLE "challenges" ADD COLUMN IF NOT EXISTS "first_turret_killed_time" FLOAT;
-- ALTER TABLE "challenges" ADD COLUMN IF NOT EXISTS "baron_buff_gold_advantage_over_threshold" FLOAT;
-- ALTER TABLE "challenges" ADD COLUMN IF NOT EXISTS "control_ward_time_coverage_in_river_or_enemy_half" FLOAT;
-- ALTER TABLE "challenges" ADD COLUMN IF NOT EXISTS "legendary_item_used" INT;
-- ALTER TABLE "challenges" ADD COLUMN IF NOT EXISTS "solo_turrets_lategame" INT;
-- ALTER TABLE "challenges" ADD COLUMN IF NOT EXISTS "void_monster_kill" INT;
-- ALTER TABLE "challenges" ADD COLUMN IF NOT EXISTS "fist_bump_participation" INT;
-- ALTER TABLE "challenges" ADD COLUMN IF NOT EXISTS "played_champ_select_position" INT;
-- ALTER TABLE "challenges" ADD COLUMN IF NOT EXISTS "shortest_time_to_ace_from_first_takedown" FLOAT;
-- ALTER TABLE "challenges" ADD COLUMN IF NOT EXISTS "heal_from_map_sources" FLOAT;

-- ALTER TABLE "champion_stats" ADD COLUMN IF NOT EXISTS "cooldown_reduction" INT;