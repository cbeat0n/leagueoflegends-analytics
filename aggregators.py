#Import dependencies
from collections import defaultdict
from statistics import mean, mode

# Compute common statistics
def compute_common_stats(entries):
    return {
        "gamesPlayed": len(entries),
        "avgKills": mean(p["kills"] for p in entries),
        "avgDeaths": mean(p["deaths"] for p in entries),
        "avgAssists": mean(p["assists"] for p in entries),
        "avgVisionScore": mean(p["visionScore"] for p in entries),
        "avgGold": mean(p["goldEarned"] for p in entries),
        "avgCS": mean(p["totalMinionsKilled"] + p["neutralMinionsKilled"] for p in entries),
        "avgDamageDealt": mean(p["damageDealtToChampions"] for p in entries),
        "avgDamageDealtPhysical": mean(p["damageDealtToChampionsPhysical"] for p in entries),
        "avgDamageDealtMagic": mean(p["damageDealtToChampionsMagic"] for p in entries),
        "avgDamageDealtTrue": mean(p["damageDealtToChampionsTrue"] for p in entries),
        "avgDamageTaken": mean(p["damageTaken"] for p in entries),
        "avgDamageTakenPhysical": mean(p["damageTakenPhysical"] for p in entries),
        "avgDamageTakenMagic": mean(p["damageTakenMagic"] for p in entries),
        "avgDamageTakenTrue": mean(p["damageTakenTrue"] for p in entries),
        "avgMitigated": mean(p["damageSelfMitigated"] for p in entries),
        "avgMitigatedPhysical": mean(p["damageSelfMitigatedPhysical"] for p in entries),
        "avgMitigatedMagic": mean(p["damageSelfMitigatedMagic"] for p in entries),
        "avgMitigatedTrue": mean(p["damageSelfMitigatedTrue"] for p in entries),
        "mostCommonSumm1": mode(p["summoner1Id"] for p in entries),
        "mostCommonSumm2": mode(p["summoner2Id"] for p in entries),
        "avgWinRate": sum(p["win"] for p in entries) / len(entries)
    }

#Compute timeseries data

def compute_timeseries_stats(games, target_puuid):
    def format_time(ms):
        total_seconds = ms // 1000
        return f"{total_seconds // 60}:{str(total_seconds % 60).zfill(2)}"

    timeseries = defaultdict(list)
    max_frame_len = 0

    for game in games:
        participant_id = None
        for p in game["specific"]['info']["participants"]:
            if p["puuid"] == target_puuid:
                participant_id = str(p.get("participantId"))
                break
        if not participant_id:
            continue

        frames = game["specific"].get("info", {}).get("frames", [])
        max_frame_len = max(max_frame_len, len(frames))

        gold_series, xp_series, cs_series, level_series = [], [], [], []

        for frame in frames:
            pf = frame.get("participantFrames", {}).get(participant_id, {})
            gold = pf.get("totalGold", 0)
            xp = pf.get("xp", 0)
            cs = pf.get("minionsKilled", 0) + pf.get("jungleMinionsKilled", 0)
            level = pf.get("level", 1)

            gold_series.append(gold)
            xp_series.append(xp)
            cs_series.append(cs)
            level_series.append(level)

        gpm = [round(g / ((i + 1) / 60), 2) for i, g in enumerate(gold_series)]
        xpm = [round(x / ((i + 1) / 60), 2) for i, x in enumerate(xp_series)]
        cspm = [round(c / ((i + 1) / 60), 2) for i, c in enumerate(cs_series)]

        timeseries["gold"].append(gold_series)
        timeseries["xp"].append(xp_series)
        timeseries["cs"].append(cs_series)
        timeseries["level"].append(level_series)
        timeseries["gpm"].append(gpm)
        timeseries["xpm"].append(xpm)
        timeseries["cspm"].append(cspm)

    timeseries["timestamps"] = [f"{i + 1}:00" for i in range(max_frame_len)]

    return dict(timeseries)

# Aggregate by Champion
def aggregate_by_champ(games, target_puuid):
    grouped = defaultdict(list)

    for game in games:
        for p in game["generic"]["participants"]:
            if p["puuid"] == target_puuid:
                champ = p["championName"]
                grouped[champ].append((p, game))

    result = {}
    for champ, player_games in grouped.items():
        player_entries = [pg[0] for pg in player_games]
        game_list = [pg[1] for pg in player_games]
        result[champ] = {
            "regular": compute_common_stats(player_entries),
            "timeseries": compute_timeseries_stats(game_list, target_puuid)
        }

    return result

#Aggregate by role
def aggregate_by_role(games, target_puuid):
    grouped = defaultdict(list)

    for game in games:
        for p in game["generic"]["participants"]:
            if p["puuid"] == target_puuid:
                role = p["teamPosition"]
                grouped[role].append((p, game))

    result = {}
    for role, player_games in grouped.items():
        player_entries = [pg[0] for pg in player_games]
        game_list = [pg[1] for pg in player_games]
        result[role] = {
            "regular": compute_common_stats(player_entries),
            "timeseries": compute_timeseries_stats(game_list, target_puuid)
        }

    return result

#Aggregate by Winloss
def aggregate_by_winloss(games, target_puuid):
    grouped = {"Win": [], "Loss": []}

    for game in games:
        for p in game["generic"]["participants"]:
            if p["puuid"] == target_puuid:
                key = "Win" if p["win"] else "Loss"
                grouped[key].append((p, game))

    result = {}
    for outcome, player_games in grouped.items():
        player_entries = [pg[0] for pg in player_games]
        game_list = [pg[1] for pg in player_games]
        result[outcome] = {
            "regular": compute_common_stats(player_entries),
            "timeseries": compute_timeseries_stats(game_list, target_puuid)
        }

    return result
