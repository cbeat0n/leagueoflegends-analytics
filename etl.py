# Import Dependencies
from dotenv import load_dotenv
import os
import json
import requests

# Load environment variables from the .env file
load_dotenv()

# Retrieve the Riot API key
riot_api_key = os.getenv("RIOT_API_KEY")

# Riot API base URL
base_url = "https://americas.api.riotgames.com"

#Get match metadata for a matchId

def get_match_metadata(match_id):
    """
    Fetches match metadata for a given match ID using the base_url.
    Includes game duration and participant stats.
    """
    url = f"{base_url}/lol/match/v5/matches/{match_id}"
    headers = {
        "X-Riot-Token": riot_api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"[ERROR] Match metadata fetch failed for {match_id}: {response.status_code}")
        return None
    

#Get match timeline data by match id.

def get_timeline_data(matchId):
    
    endpoint = f"/lol/match/v5/matches/{matchId}/timeline"


    headers = {
        "X-Riot-Token": riot_api_key
    }

    url = base_url + endpoint


    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Timeline data
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    


# Pruning metadata function

def prune_metadata(metadata: dict) -> dict:
    info = metadata.get("info", {})
    teams = info.get("teams", [])
    participants = info.get("participants", [])

    pruned = {
        "matchId": metadata.get("metadata", {}).get("matchId"),
        "gameCreation": info.get("gameCreation"),
        "gameStartTimestamp": info.get("gameStartTimestamp"),
        "gameDuration": info.get("gameDuration"),
        "gameVersion": info.get("gameVersion"),
        "queueId": info.get("queueId"),
        "platformId": info.get("platformId"),
        "teams": [],
        "participants": []
    }

    for team in teams:
        pruned_team = {
            "teamId": team.get("teamId"),
            "win": team.get("win"),
            "objectives": team.get("objectives", {}),
            "bans": []  # We'll match these to puuids later if needed
        }
        pruned["teams"].append(pruned_team)

    for p in participants:
        
        pruned["participants"].append({
            "summonerName": p.get("summonerName"),
            "puuid": p.get("puuid"),
            "teamId": p.get("teamId"),
            "championName": p.get("championName"),
            "champLevel": p.get("champLevel"),
            "teamPosition": p.get("teamPosition"),
            "individualPosition": p.get("individualPosition"),
            "win": p.get("win"),
            "kills": p.get("kills"),
            "deaths": p.get("deaths"),
            "assists": p.get("assists"),
            "goldEarned": p.get("goldEarned"),
            "totalMinionsKilled": p.get("totalMinionsKilled"),
            "neutralMinionsKilled": p.get("neutralMinionsKilled"),
            "visionScore": p.get("visionScore"),
            "damageDealtToChampions": p.get("totalDamageDealtToChampions"),
            "damageDealtToChampionsPhysical": p.get("physicalDamageDealtToChampions"),
            "damageDealtToChampionsMagic": p.get("magicDamageDealtToChampions"),
            "damageDealtToChampionsTrue": p.get("trueDamageDealtToChampions"),
            "damageTaken": p.get("totalDamageTaken"),
            "damageTakenPhysical": p.get("physicalDamageTaken"),
            "damageTakenMagic": p.get("magicDamageTaken"),
            "damageTakenTrue": p.get("trueDamageTaken"),
            "damageSelfMitigated": p.get("damageSelfMitigated"),
            "damageSelfMitigatedPhysical": p.get("physicalDamageSelfMitigated", 0),  # fallback
            "damageSelfMitigatedMagic": p.get("magicDamageSelfMitigated", 0),
            "damageSelfMitigatedTrue": p.get("trueDamageSelfMitigated", 0),
            "summoner1Id": p.get("summoner1Id"),
            "summoner2Id": p.get("summoner2Id"),
            "perks": p.get("perks", {}),
            "items": [p.get(f"item{i}", 0) for i in range(7)]
        })

    return pruned


#Compose new zipped json function

def merge_match_data(match_id: str) -> dict | None:
    metadata = get_match_metadata(match_id)
    timeline = get_timeline_data(match_id)

    if not metadata or not timeline:
        print(f"[!] Skipping match {match_id} — missing metadata or timeline.")
        return None

    return {
        "generic": prune_metadata(metadata),
        "specific": timeline
    }

