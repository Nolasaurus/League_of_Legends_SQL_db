import sys
import logging
import pandas as pd


logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def get_bans(match_dto):
    metadata = match_dto.get("metadata", {})
    match_id = metadata.get("matchId", "")
    teams = match_dto.get("info", {}).get("teams", [])

    # Prepare a list to hold all the values to be inserted
    all_values = []
    for team in teams:
        for ban in team.get("bans", []):
            # Append each set of values as a dictionary to the list
            ban_dict = {
                "match_id": match_id,
                "champion_id": ban.get("championId"),
                "pick_turn": ban.get("pickTurn"),
            }
            all_values.append(ban_dict)

    return pd.DataFrame(all_values)


def get_champion_stats(match_timeline_dto):
    frames = match_timeline_dto.get("info", {}).get("frames", [])
    match_id = match_timeline_dto.get("metadata", {}).get("matchId", "")

    values_list = []
    for frame_number, frame in enumerate(frames):
        for participant_id, participant_frame in frame.get(
            "participant_frames", {}
        ).items():
            champion_stats = participant_frame.get("champion_stats", {})
            values = {
                "match_id": match_id,
                "frame_number": frame_number,
                "participant_id": participant_id,
                "ability_haste": champion_stats.get("abilityHaste", 0),
                "ability_power": champion_stats.get("abilityPower", 0),
                "armor": champion_stats.get("armor", 0),
                "armor_pen": champion_stats.get("armorPen", 0),
                "armor_pen_percent": champion_stats.get("armorPenPercent", 0.0),
                "attack_damage": champion_stats.get("attackDamage", 0),
                "attack_speed": champion_stats.get("attackSpeed", 0.0),
                "bonus_armor_pen_percent": champion_stats.get(
                    "bonusArmorPenPercent", 0.0
                ),
                "bonus_magic_pen_percent": champion_stats.get(
                    "bonusMagicPenPercent", 0.0
                ),
                "cc_reduction": champion_stats.get("ccReduction", 0),
                "cooldown_reduction": champion_stats.get("cooldownReduction", 0),
                "health": champion_stats.get("health", 0),
                "health_max": champion_stats.get("healthMax", 0),
                "health_regen": champion_stats.get("healthRegen", 0),
                "lifesteal": champion_stats.get("lifesteal", 0.0),
                "magic_pen": champion_stats.get("magicPen", 0),
                "magic_pen_percent": champion_stats.get("magicPenPercent", 0.0),
                "magic_resist": champion_stats.get("magicResist", 0),
                "movement_speed": champion_stats.get("movementSpeed", 0),
                "omnivamp": champion_stats.get("omnivamp", 0.0),
                "physical_vamp": champion_stats.get("physicalVamp", 0.0),
                "power": champion_stats.get("power", 0),
                "power_max": champion_stats.get("powerMax", 0),
                "power_regen": champion_stats.get("powerRegen", 0),
                "spell_vamp": champion_stats.get("spellVamp", 0.0),
            }

            values_list.append(values)

    return pd.DataFrame(values_list)


def get_match_metadata(match_dto):
    metadata = match_dto.get("metadata", {})
    info = match_dto.get("info", {})

    match_metadata_dict = {
        "data_version": metadata.get("dataVersion", ""),
        "match_id": metadata.get("matchId", ""),
        "game_creation": info.get("gameCreation", 0),
        "game_duration": info.get("gameDuration", 0),
        "game_end_timestamp": info.get("gameEndTimestamp", 0),
        "game_id": info.get("gameId", ""),
        "game_mode": info.get("gameMode", ""),
        "game_name": info.get("gameName", ""),
        "game_start_timestamp": info.get("gameStartTimestamp", 0),
        "game_type": info.get("gameType", ""),
        "game_version": info.get("gameVersion", ""),
        "map_id": info.get("mapId", 0),
        "platform_id": info.get("platformId", ""),
        "queue_id": info.get("queueId", 0),
        "tournament_code": info.get("tournamentCode", ""),
        "end_of_game_result": info.get("endOfGameResult", ""),
    }

    return pd.DataFrame([match_metadata_dict])


def get_perk_style_selections(match_dto):
    participants = match_dto.get("info", {}).get("participants", [])
    match_id = match_dto.get("metadata", {}).get("matchId", "")

    perk_style_selections_list = []
    for participant in participants:
        participant_id = participant.get("participantId", "")
        for _, style in enumerate(participant.get("perks", {}).get("styles", [])):
            for _, selection in enumerate(style.get("selections", [])):
                perk_style_selection_dict = {
                    "match_id": match_id,
                    "participant_id": participant_id,
                    "perks_style": style.get("style", 0),
                    "perks_description": style.get("description", ""),
                    "perk": selection.get("perk", 0),
                    "var1": selection.get("var1", 0),
                    "var2": selection.get("var2", 0),
                    "var3": selection.get("var3", 0),
                }

                perk_style_selections_list.append(perk_style_selection_dict)

    return pd.DataFrame(perk_style_selections_list)


def get_teams(match_dto):
    metadata = match_dto.get("metadata", {})
    match_id = metadata.get("matchId", )
    teams = match_dto.get("info", {}).get("teams", [])

    teams_list = []
    for team in teams:
        # Extracting objectives data
        objectives = team.get("objectives", {}).get("objectives", {})

        team_data = {
            "team_id": team.get("teamId", ""),
            "match_id": match_id,
            "baron_first": objectives.get("baron", {}).get("first", False),
            "baron_kills": objectives.get("baron", {}).get("kills", 0),
            "dragon_first": objectives.get("dragon", {}).get("first", False),
            "dragon_kills": objectives.get("dragon", {}).get("kills", 0),
            "champion_first": objectives.get("champion", {}).get("first", False),
            "champion_kills": objectives.get("champion", {}).get("kills", 0),
            "inhibitor_first": objectives.get("inhibitor", {}).get("first", False),
            "inhibitor_kills": objectives.get("inhibitor", {}).get("kills", 0),
            "rift_herald_first": objectives.get("riftHerald", {}).get("first", False),
            "rift_herald_kills": objectives.get("riftHerald", {}).get("kills", 0),
            "tower_first": objectives.get("tower", {}).get("first", False),
            "tower_kills": objectives.get("tower", {}).get("kills", 0),
            "win": team.get("win", ""),
        }

        teams_list.append(team_data)

    return pd.DataFrame(teams_list)


def get_damage_stats(match_timeline_dto):
    frames = match_timeline_dto.get("info", {}).get("frames", [])
    match_id = match_timeline_dto.get("metadata", {}).get("matchId", "")

    damage_stats_list = []
    for frame_number, frame in enumerate(frames):
        for participant_frame in frame.get("participantFrames", {}).values():

            participant_id = participant_frame.get("participantId")
            damage_stats = participant_frame.get("damageStats", {})

            damage_stat_dict = {
                "match_id": match_id,
                "frame_number": frame_number,
                "participant_id": participant_id,
                "magic_damage_done": damage_stats.get("magicDamageDone", 0),
                "magic_damage_done_to_champions": damage_stats.get(
                    "magicDamageDoneToChampions", 0
                ),
                "magic_damage_taken": damage_stats.get("magicDamageTaken", 0),
                "physical_damage_done": damage_stats.get("physicalDamageDone", 0),
                "physical_damage_done_to_champions": damage_stats.get(
                    "physicalDamageDoneToChampions", 0
                ),
                "physical_damage_taken": damage_stats.get("physicalDamageTaken", 0),
                "total_damage_done": damage_stats.get("totalDamageDone", 0),
                "total_damage_done_to_champions": damage_stats.get(
                    "totalDamageDoneToChampions", 0
                ),
                "total_damage_taken": damage_stats.get("totalDamageTaken", 0),
                "true_damage_done": damage_stats.get("trueDamageDone", 0),
                "true_damage_done_to_champions": damage_stats.get(
                    "trueDamageDoneToChampions", 0
                ),
                "true_damage_taken": damage_stats.get("trueDamageTaken", 0),
            }

            damage_stats_list.append(damage_stat_dict)

    return pd.DataFrame(damage_stats_list)


def get_victim_damage_received(match_timeline_dto):
    frames = match_timeline_dto.get("info", {}).get("frames", [])
    match_id = match_timeline_dto.get("metadata", {}).get("matchId", "")

    damage_received_list = []

    for frame_number, frame in enumerate(frames):
        for event_number, event in enumerate(frame.get("events", [])):
            if event.get("type") == "CHAMPION_KILL":
                for damage_number, damage_received in enumerate(event.get("victimDamageReceived", [])):
                    received_values = {
                        "match_id": match_id,
                        "frame_number": frame_number,
                        "event_number": event_number,
                        "damage_number": damage_number,
                        "participant_id": damage_received.get("participantId"),
                        "basic": damage_received.get("basic"),
                        "magic_damage": damage_received.get("magicDamage"),
                        "physical_damage": damage_received.get("physicalDamage"),
                        "name": damage_received.get("name"),
                        "spell_name": damage_received.get("spellName", ""),
                        "spell_slot": damage_received.get("spellSlot", 0),
                        "true_damage": damage_received.get("trueDamage"),
                        "type": damage_received.get("type"),
                    }

                    damage_received_list.append(received_values)

    return pd.DataFrame(damage_received_list)


def get_victim_damage_dealt(match_timeline_dto):
    frames = match_timeline_dto.get("info", {}).get("frames", [])
    match_id = match_timeline_dto.get("metadata", {}).get("matchId", "")

    damage_dealt_list = []

    for frame_number, frame in enumerate(frames):
        for event_number, event in enumerate(frame.get("events", [])):
            if event.get("type") == "CHAMPION_KILL":
                for damage_number, damage_dealt in enumerate(event.get("victimDamageDealt", [])):
                    dealt_values = {
                        "match_id": match_id,
                        "frame_number": frame_number,
                        "event_number": event_number,
                        "damage_number": damage_number,
                        "basic": damage_dealt.get("basic"),
                        "magic_damage": damage_dealt.get("magicDamage"),
                        "physical_damage": damage_dealt.get("physicalDamage"),
                        "name": damage_dealt.get("name"),
                        "spell_name": damage_dealt.get("spellName", ""),
                        "spell_slot": damage_dealt.get("spellSlot", 0),
                        "true_damage": damage_dealt.get("trueDamage"),
                        "type": damage_dealt.get("type"),
                    }

                    damage_dealt_list.append(dealt_values)

    return pd.DataFrame(damage_dealt_list)


def get_challenges(match_dto):
    challenges_list = []

    participants = match_dto.get("info", {}).get("participants", [])
    for participant in participants:
        challenges = participant.get("challenges") or {}

        values = {
            "match_id": match_dto.get("metadata", {}).get("matchId", ""),
            "participant_id": participant.get("participantId"),
            "assist_streak_count": challenges.get("assistStreakCount", 0),
            "ability_uses": challenges.get("abilityUses", 0),
            "aces_before_15_minutes": challenges.get("acesBefore15Minutes", 0),
            "allied_jungle_monster_kills": challenges.get(
                "alliedJungleMonsterKills", 0
            ),
            "baron_takedowns": challenges.get("baronTakedowns", 0),
            "blast_cone_opposite_opponent_count": challenges.get(
                "blastConeOppositeOpponentCount", 0
            ),
            "bounty_gold": challenges.get("bountyGold", 0),
            "buffs_stolen": challenges.get("buffsStolen", 0),
            "complete_support_quest_in_time": challenges.get(
                "completeSupportQuestInTime", 0
            ),
            "control_wards_placed": challenges.get("controlWardsPlaced", 0),
            "damage_per_minute": challenges.get("damagePerMinute", 0.0),
            "damage_taken_on_team_percentage": challenges.get(
                "damageTakenOnTeamPercentage", 0.0
            ),
            "danced_with_rift_herald": challenges.get("dancedWithRiftHerald", 0),
            "deaths_by_enemy_champs": challenges.get("deathsByEnemyChamps", 0),
            "dodge_skill_shots_small_window": challenges.get(
                "dodgeSkillShotsSmallWindow", 0
            ),
            "double_aces": challenges.get("doubleAces", 0),
            "dragon_takedowns": challenges.get("dragonTakedowns", 0),
            "early_laning_phase_gold_exp_advantage": challenges.get(
                "earlyLaningPhaseGoldExpAdvantage", 0.0
            ),
            "effective_heal_and_shielding": challenges.get(
                "effectiveHealAndShielding", 0
            ),
            "elder_dragon_kills_with_opposing_soul": challenges.get(
                "elderDragonKillsWithOpposingSoul", 0
            ),
            "elder_dragon_multikills": challenges.get("elderDragonMultikills", 0),
            "enemy_champion_immobilizations": challenges.get(
                "enemyChampionImmobilizations", 0
            ),
            "enemy_jungle_monster_kills": challenges.get("enemyJungleMonsterKills", 0),
            "epic_monster_kills_near_enemy_jungler": challenges.get(
                "epicMonsterKillsNearEnemyJungler", 0
            ),
            "epic_monster_kills_within_30_seconds_of_spawn": challenges.get(
                "epicMonsterKillsWithin30SecondsOfSpawn", 0
            ),
            "epic_monster_steals": challenges.get("epicMonsterSteals", 0),
            "epic_monster_stolen_without_smite": challenges.get(
                "epicMonsterStolenWithoutSmite", 0
            ),
            "first_turret_killed": challenges.get("firstTurretKilled", 0),
            "flawless_aces": challenges.get("flawlessAces", 0),
            "full_team_takedown": challenges.get("fullTeamTakedown", 0),
            "game_length": challenges.get("gameLength", 0.0),
            "get_takedowns_in_all_lanes_early_jungle_as_laner": challenges.get(
                "getTakedownsInAllLanesEarlyJungleAsLaner", 0
            ),
            "gold_per_minute": challenges.get("goldPerMinute", 0.0),
            "had_open_nexus": challenges.get("hadOpenNexus", 0),
            "immobilize_and_kill_with_ally": challenges.get(
                "immobilizeAndKillWithAlly", 0
            ),
            "initial_buff_count": challenges.get("initialBuffCount", 0),
            "initial_crab_count": challenges.get("initialCrabCount", 0),
            "jungle_cs_before_10_minutes": challenges.get("jungleCsBefore10Minutes", 0),
            "jungler_takedowns_near_damaged_epic_monster": challenges.get(
                "junglerTakedownsNearDamagedEpicMonster", 0
            ),
            "k_turrets_destroyed_before_plates_fall": challenges.get(
                "kTurretsDestroyedBeforePlatesFall", 0
            ),
            "kda": challenges.get("kda", 0.0),
            "kill_after_hidden_with_ally": challenges.get("killAfterHiddenWithAlly", 0),
            "kill_participation": challenges.get("killParticipation", 0.0),
            "killed_champ_took_full_team_damage_survived": challenges.get(
                "killedChampTookFullTeamDamageSurvived", 0
            ),
            "killing_sprees": challenges.get("killingSprees", 0),
            "kills_near_enemy_turret": challenges.get("killsNearEnemyTurret", 0),
            "kills_on_other_lanes_early_jungle_as_laner": challenges.get(
                "killsOnOtherLanesEarlyJungleAsLaner", 0
            ),
            "kills_on_recently_healed_by_aram_pack": challenges.get(
                "killsOnRecentlyHealedByAramPack", 0
            ),
            "kills_under_own_turret": challenges.get("killsUnderOwnTurret", 0),
            "kills_with_help_from_epic_monster": challenges.get(
                "killsWithHelpFromEpicMonster", 0
            ),
            "knock_enemy_into_team_and_kill": challenges.get(
                "knockEnemyIntoTeamAndKill", 0
            ),
            "land_skill_shots_early_game": challenges.get("landSkillShotsEarlyGame", 0),
            "lane_minions_first_10_minutes": challenges.get(
                "laneMinionsFirst10Minutes", 0
            ),
            "laning_phase_gold_exp_advantage": challenges.get(
                "laningPhaseGoldExpAdvantage", 0.0
            ),
            "legendary_count": challenges.get("legendaryCount", 0),
            "lost_an_inhibitor": challenges.get("lostAnInhibitor", 0),
            "max_cs_advantage_on_lane_opponent": challenges.get(
                "maxCsAdvantageOnLaneOpponent", 0
            ),
            "max_kill_deficit": challenges.get("maxKillDeficit", 0),
            "max_level_lead_lane_opponent": challenges.get(
                "maxLevelLeadLaneOpponent", 0
            ),
            "mejais_full_stack_in_time": challenges.get("mejaisFullStackInTime", 0),
            "more_enemy_jungle_than_opponent": challenges.get(
                "moreEnemyJungleThanOpponent", 0
            ),
            "multi_kill_one_spell": challenges.get("multiKillOneSpell", 0),
            "multi_turret_rift_herald_count": challenges.get(
                "multiTurretRiftHeraldCount", 0
            ),
            "multikills": challenges.get("multikills", 0),
            "multikills_after_aggressive_flash": challenges.get(
                "multikillsAfterAggressiveFlash", 0
            ),
            "mythic_item_used": challenges.get("mythicItemUsed", 0),
            "outer_turret_executes_before_10_minutes": challenges.get(
                "outerTurretExecutesBefore10Minutes", 0
            ),
            "outnumbered_kills": challenges.get("outnumberedKills", 0),
            "outnumbered_nexus_kill": challenges.get("outnumberedNexusKill", 0),
            "perfect_dragon_souls_taken": challenges.get("perfectDragonSoulsTaken", 0),
            "perfect_game": challenges.get("perfectGame", 0),
            "pick_kill_with_ally": challenges.get("pickKillWithAlly", 0),
            "poro_explosions": challenges.get("poroExplosions", 0),
            "quick_cleanse": challenges.get("quickCleanse", 0),
            "quick_first_turret": challenges.get("quickFirstTurret", 0),
            "quick_solo_kills": challenges.get("quickSoloKills", 0),
            "rift_herald_takedowns": challenges.get("riftHeraldTakedowns", 0),
            "save_ally_from_death": challenges.get("saveAllyFromDeath", 0),
            "scuttle_crab_kills": challenges.get("scuttleCrabKills", 0),
            "skillshots_dodged": challenges.get("skillshotsDodged", 0),
            "skillshots_hit": challenges.get("skillshotsHit", 0),
            "snowballs_hit": challenges.get("snowballsHit", 0),
            "solo_baron_kills": challenges.get("soloBaronKills", 0),
            "solo_kills": challenges.get("soloKills", 0),
            "stealth_wards_placed": challenges.get("stealthWardsPlaced", 0),
            "survived_single_digit_hp_count": challenges.get(
                "survivedSingleDigitHpCount", 0
            ),
            "survived_three_immobilizes_in_fight": challenges.get(
                "survivedThreeImmobilizesInFight", 0
            ),
            "takedown_on_first_turret": challenges.get("takedownOnFirstTurret", 0),
            "takedowns": challenges.get("takedowns", 0),
            "takedowns_after_gaining_level_advantage": challenges.get(
                "takedownsAfterGainingLevelAdvantage", 0
            ),
            "takedowns_before_jungle_minion_spawn": challenges.get(
                "takedownsBeforeJungleMinionSpawn", 0
            ),
            "takedowns_first_x_minutes": challenges.get("takedownsFirstXMinutes", 0),
            "takedowns_in_alcove": challenges.get("takedownsInAlcove", 0),
            "takedowns_in_enemy_fountain": challenges.get(
                "takedownsInEnemyFountain", 0
            ),
            "team_baron_kills": challenges.get("teamBaronKills", 0),
            "team_damage_percentage": challenges.get("teamDamagePercentage", 0.0),
            "team_elder_dragon_kills": challenges.get("teamElderDragonKills", 0),
            "team_rift_herald_kills": challenges.get("teamRiftHeraldKills", 0),
            "took_large_damage_survived": challenges.get("tookLargeDamageSurvived", 0),
            "turret_plates_taken": challenges.get("turretPlatesTaken", 0),
            "turret_takedowns": challenges.get("turretTakedowns", 0),
            "turrets_taken_with_rift_herald": challenges.get(
                "turretsTakenWithRiftHerald", 0
            ),
            "twenty_minions_in_3_seconds_count": challenges.get(
                "twentyMinionsIn3SecondsCount", 0
            ),
            "two_wards_one_sweeper_count": challenges.get("twoWardsOneSweeperCount", 0),
            "unseen_recalls": challenges.get("unseenRecalls", 0),
            "vision_score_advantage_lane_opponent": challenges.get(
                "visionScoreAdvantageLaneOpponent", 0.0
            ),
            "vision_score_per_minute": challenges.get("visionScorePerMinute", 0.0),
            "ward_takedowns": challenges.get("wardTakedowns", 0),
            "ward_takedowns_before_20m": challenges.get("wardTakedownsBefore20m", 0),
            "wards_guarded": challenges.get("wardsGuarded", 0),
            "earliest_baron": challenges.get("earliestBaron", None),
            "earliest_dragon_takedown": challenges.get("earliestDragonTakedown", None),
            "first_turret_killed_time": challenges.get("firstTurretKilledTime", None),
            "baron_buff_gold_advantage_over_threshold": challenges.get("baronBuffGoldAdvantageOverThreshold", None),
            "control_ward_time_coverage_in_river_or_enemy_half": challenges.get("controlWardTimeCoverageInRiverOrEnemyHalf", None),
            "legendary_item_used": challenges.get("legendaryItemUsed", None),
            "solo_turrets_lategame": challenges.get("soloTurretsLategame", 0),
            "void_monster_kill": challenges.get("voidMonsterKill", 0),
            "fist_bump_participation": challenges.get("fistBumpParticipation", 0),
            "played_champ_select_position": challenges.get("playedChampSelectPosition", 0),
            "shortest_time_to_ace_from_first_takedown": challenges.get("shortestTimeToAceFromFirstTakedown", None),
            "heal_from_map_sources": challenges.get("healFromMapSources", 0.0),
        }

        challenges_list.append(values)

    return pd.DataFrame(challenges_list)


def get_match_events(match_timeline_dto):
    frames = match_timeline_dto.get("info", {}).get("frames", [])
    match_id = match_timeline_dto.get("metadata", {}).get("matchId", None)

    events_list = []
    for frame_number, frame in enumerate(frames):
        for event_number, event in enumerate(frame.get("events", [])):
            events_dict = {
                "match_id": match_id,
                "frame_number": frame_number,
                "event_number": event_number,
                "real_timestamp": event.get("realTimestamp", None),
                "timestamp": event.get("timestamp", None),
                "type": event.get("type", None),
                "item_id": event.get("itemId", None),
                "participant_id": event.get("participantId", None),
                "level_up_type": event.get("levelUpType", ""),
                "skill_slot": event.get("skillSlot", None),
                "creator_id": event.get("creatorId", None),
                "ward_type": event.get("wardType", ""),
                "level": event.get("level", None),
                "bounty": event.get("bounty", None),
                "kill_streak_length": event.get("killStreakLength", None),
                "killer_id": event.get("killerId", None),
                "position_x": event.get("position", {}).get("x", None),
                "position_y": event.get("position", {}).get("y", None),
                "victim_id": event.get("victimId", None),
                "kill_type": event.get("killType", ""),
                "lane_type": event.get("laneType", ""),
                "team_id": event.get("teamId", None),
                "multi_kill_length": event.get("multiKillLength", None),
                "killer_team_id": event.get("killerTeamId", None),
                "monster_type": event.get("monsterType", ""),
                "monster_sub_type": event.get("monsterSubType", ""),
                "building_type": event.get("buildingType", ""),
                "tower_type": event.get("towerType", ""),
                "after_id": event.get("afterId", None),
                "before_id": event.get("beforeId", None),
                "gold_gain": event.get("goldGain", None),
                "game_id": event.get("gameId", None),
                "winning_team": event.get("winningTeam", None),
                "transform_type": event.get("transformType", ""),
                "name": event.get("name", ""),
                "shutdown_bounty": event.get("shutdownBounty", None),
                "actual_start_time": event.get("actualStartTime", None),
            }

            events_list.append(events_dict)

    return pd.DataFrame(events_list)


def get_participant_dto(match_dto):
    participants = match_dto.get("info", {}).get("participants", [])
    match_id = match_dto.get("metadata", {}).get("matchId", "")

    participant_dto_list = []

    for participant in participants:
        values = {
            "match_id": match_id,
            "participant_id": participant.get("participantId", 0),
            "assists": participant.get("assists", 0),
            "baron_kills": participant.get("baronKills", 0),
            "bounty_level": participant.get("bountyLevel", 0),
            "champ_experience": participant.get("champExperience", 0),
            "champ_level": participant.get("champLevel", 0),
            "champion_id": participant.get("championId", 0),
            "champion_name": participant.get("championName", ""),
            "champion_transform": participant.get("championTransform", 0),
            "consumables_purchased": participant.get("consumablesPurchased", 0),
            "damage_dealt_to_buildings": participant.get("damageDealtToBuildings", 0),
            "damage_dealt_to_objectives": participant.get("damageDealtToObjectives", 0),
            "damage_dealt_to_turrets": participant.get("damageDealtToTurrets", 0),
            "damage_self_mitigated": participant.get("damageSelfMitigated", 0),
            "deaths": participant.get("deaths", 0),
            "detector_wards_placed": participant.get("detectorWardsPlaced", 0),
            "double_kills": participant.get("doubleKills", 0),
            "dragon_kills": participant.get("dragonKills", 0),
            "first_blood_assist": participant.get("firstBloodAssist", False),
            "first_blood_kill": participant.get("firstBloodKill", False),
            "first_tower_assist": participant.get("firstTowerAssist", False),
            "first_tower_kill": participant.get("firstTowerKill", False),
            "game_ended_in_early_surrender": participant.get("gameEndedInEarlySurrender", False),
            "game_ended_in_surrender": participant.get("gameEndedInSurrender", False),
            "gold_earned": participant.get("goldEarned", 0),
            "gold_spent": participant.get("goldSpent", 0),
            "individual_position": participant.get("individualPosition", ""),
            "inhibitor_kills": participant.get("inhibitorKills", 0),
            "inhibitor_takedowns": participant.get("inhibitorTakedowns", 0),
            "inhibitors_lost": participant.get("inhibitorsLost", 0),
            "item0": participant.get("item0", 0),
            "item1": participant.get("item1", 0),
            "item2": participant.get("item2", 0),
            "item3": participant.get("item3", 0),
            "item4": participant.get("item4", 0),
            "item5": participant.get("item5", 0),
            "item6": participant.get("item6", 0),
            "items_purchased": participant.get("itemsPurchased", 0),
            "killing_sprees": participant.get("killingSprees", 0),
            "kills": participant.get("kills", 0),
            "lane": participant.get("lane", ""),
            "largest_critical_strike": participant.get("largestCriticalStrike", 0),
            "largest_killing_spree": participant.get("largestKillingSpree", 0),
            "largest_multi_kill": participant.get("largestMultiKill", 0),
            "longest_time_spent_living": participant.get("longestTimeSpentLiving", 0),
            "magic_damage_dealt": participant.get("magicDamageDealt", 0),
            "magic_damage_dealt_to_champions": participant.get("magicDamageDealtToChampions", 0),
            "magic_damage_taken": participant.get("magicDamageTaken", 0),
            "neutral_minions_killed": participant.get("neutralMinionsKilled", 0),
            "nexus_kills": participant.get("nexusKills", 0),
            "nexus_takedowns": participant.get("nexusTakedowns", 0),
            "nexus_lost": participant.get("nexusLost", 0),
            "objectives_stolen": participant.get("objectivesStolen", 0),
            "objectives_stolen_assists": participant.get("objectivesStolenAssists", 0),
            "penta_kills": participant.get("pentaKills", 0),
            "physical_damage_dealt": participant.get("physicalDamageDealt", 0),
            "physical_damage_dealt_to_champions": participant.get("physicalDamageDealtToChampions", 0),
            "physical_damage_taken": participant.get("physicalDamageTaken", 0),
            "profile_icon": participant.get("profileIcon", 0),
            "puuid": participant.get("puuid", ""),
            "quadra_kills": participant.get("quadraKills", 0),
            "riot_id_name": participant.get("riotIdName", ""),
            "riot_id_game_name": participant.get("riotIdGameName") or participant.get("riotIdName", ""),
            "riot_id_tagline": participant.get("riotIdTagline", ""),
            "role": participant.get("role", ""),
            "sight_wards_bought_in_game": participant.get("sightWardsBoughtInGame", 0),
            "spell1_casts": participant.get("spell1Casts", 0),
            "spell2_casts": participant.get("spell2Casts", 0),
            "spell3_casts": participant.get("spell3Casts", 0),
            "spell4_casts": participant.get("spell4Casts", 0),
            "summoner1_casts": participant.get("summoner1Casts", 0),
            "summoner1_id": participant.get("summoner1Id", 0),
            "summoner2_casts": participant.get("summoner2Casts", 0),
            "summoner2_id": participant.get("summoner2Id", 0),
            "summoner_id": participant.get("summonerId", ""),
            "summoner_level": participant.get("summonerLevel", 0),
            "summoner_name": participant.get("summonerName", ""),
            "team_early_surrendered": participant.get("teamEarlySurrendered", False),
            "team_id": participant.get("teamId", 0),
            "team_position": participant.get("teamPosition", ""),
            "time_ccing_others": participant.get("timeCCingOthers", 0),
            "time_played": participant.get("timePlayed", 0),
            "total_damage_dealt": participant.get("totalDamageDealt", 0),
            "total_damage_dealt_to_champions": participant.get("totalDamageDealtToChampions", 0),
            "total_damage_shielded_on_teammates": participant.get("totalDamageShieldedOnTeammates", 0),
            "total_damage_taken": participant.get("totalDamageTaken", 0),
            "total_heal": participant.get("totalHeal", 0),
            "total_heals_on_teammates": participant.get("totalHealsOnTeammates", 0),
            "total_minions_killed": participant.get("totalMinionsKilled", 0),
            "total_time_cc_dealt": participant.get("totalTimeCCDealt", 0),
            "total_time_spent_dead": participant.get("totalTimeSpentDead", 0),
            "total_units_healed": participant.get("totalUnitsHealed", 0),
            "triple_kills": participant.get("tripleKills", 0),
            "true_damage_dealt": participant.get("trueDamageDealt", 0),
            "true_damage_dealt_to_champions": participant.get("trueDamageDealtToChampions", 0),
            "true_damage_taken": participant.get("trueDamageTaken", 0),
            "turret_kills": participant.get("turretKills", 0),
            "turret_takedowns": participant.get("turretTakedowns", 0),
            "turrets_lost": participant.get("turretsLost", 0),
            "unreal_kills": participant.get("unrealKills", 0),
            "vision_score": participant.get("visionScore", 0),
            "vision_wards_bought_in_game": participant.get("visionWardsBoughtInGame", 0),
            "wards_killed": participant.get("wardsKilled", 0),
            "wards_placed": participant.get("wardsPlaced", 0),
            "win": participant.get("win", False),
            "damage_dealt_to_epic_monsters": participant.get("damageDealtToEpicMonsters", 0),
            "retreat_pings": participant.get("retreatPings", 0),
            "player_augment5": participant.get("playerAugment5", 0),
            "player_augment6": participant.get("playerAugment6", 0),
            "role_bound_item": participant.get("roleBoundItem", 0),
            "perks_defense": participant.get("perks", {}).get("defense", 0),
            "perks_flex": participant.get("perks", {}).get("flex", 0),
            "perks_offense": participant.get("perks", {}).get("offense", 0),
        }

        participant_dto_list.append(values)

    return pd.DataFrame(participant_dto_list)

def get_participant_frames(match_timeline_dto):
    logging.info("Starting get_participant_frames function")

    frames = match_timeline_dto.get("info", {}).get("frames", [])
    match_id = match_timeline_dto.get("metadata", {}).get("matchId", None)
    logging.info(f"Match ID: {match_id}")

    if not match_id:
        logging.warning("Match ID is None")

    participant_frames_list = []
    for frame_number, frame in enumerate(frames):
        participant_frames = frame.get("participantFrames", {})
        for participant_id, participant_frame in participant_frames.items():
            pframes_dict = {
                "match_id": match_id,
                "frame_number": frame_number,
                "participant_id": participant_id,
                "timestamp": frame.get("timestamp", None),
                "level": participant_frame.get("level", None),
                "current_gold": participant_frame.get("currentGold", None),
                "gold_per_second": participant_frame.get("goldPerSecond", None),
                "total_gold": participant_frame.get("totalGold", None),
                "xp": participant_frame.get("xp", None),
                "minions_killed": participant_frame.get("minionsKilled", None),
                "jungle_minions_killed": participant_frame.get("jungleMinionsKilled", None),
                "time_enemy_spent_controlled": participant_frame.get("timeEnemySpentControlled", None),
                "position_x": participant_frame.get("position", {}).get("x"),
                "position_y": participant_frame.get("position", {}).get("y"),
            }

            participant_frames_list.append(pframes_dict)
            logging.debug(f"Added participant frame: {pframes_dict}")

    df = pd.DataFrame(participant_frames_list)
    if df.empty:
        logging.warning("The dataframe is empty")
    return df
