# Import Dependencies
from dotenv import load_dotenv
import os
import json
import requests
import urllib.parse

# Load environment variables from the .env file
load_dotenv()

# Retrieve the Riot API key
riot_api_key = os.getenv("RIOT_API_KEY")

# Riot API base URL
base_url = "https://americas.api.riotgames.com"

# Grab a Summoner's puuid

def get_puuid(game_name, tag_line):
    """
    Get the PUUID (Player Unique ID) for a given summoner using their Riot ID (gameName and tagLine).
    
    Parameters:
    - game_name (str): Summoner's game name (e.g., 'SummonerOne')
    - tag_line (str): Summoner's tag line (e.g., '0xZZk')
    
    Returns:
    - str: The PUUID of the summoner, or None if the request fails.
    """

    # Endpoint to get account info by Riot ID
    endpoint = f"/riot/account/v1/accounts/by-riot-id/{urllib.parse.quote(game_name)}/{urllib.parse.quote(tag_line)}"
    
    # Construct the full URL
    url = base_url + endpoint
    
    # Define headers, including the API Key
    headers = {
        "X-Riot-Token": riot_api_key
    }
    
    # Make the API request
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Extract PUUID from the response
        return data.get("puuid", None)
    else:
        print(f"Error fetching PUUID: {response.status_code} - {response.text}")
        return None
    
# Grab Summoners last n matches

def get_match_ids(puuid, count=10):
    headers = {
        "X-Riot-Token": riot_api_key
    }
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {
        "start": 0,
        "count": count,
        "queue": 420
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()  # List of match IDs
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None