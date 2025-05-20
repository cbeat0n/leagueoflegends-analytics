import os
import json
from datetime import datetime

# Create or return today's data folder path
def get_today_folder(base_dir="data"):
    today = datetime.now().strftime("%Y-%m-%d")
    full_path = os.path.join(base_dir, today)

    os.makedirs(full_path, exist_ok=True)
    return full_path

# Generate a timestamp string like "153042" (HHMMSS)
def get_time_suffix():
    return datetime.now().strftime("%H%M%S")


# Save each zipped game JSON individually
def save_raw_games(games: list, user_tag: str):
    folder = get_today_folder()
    time_suffix = get_time_suffix()

    for i, game in enumerate(games):
        filename = f"raw_{user_tag}_game{i+1}_{time_suffix}.json"
        path = os.path.join(folder, filename)
        with open(path, "w") as f:
            json.dump(game, f, indent=4)


# Save aggregated by champion
def save_agg_by_champion(data: dict, user_tag: str):
    folder = get_today_folder()
    time_suffix = get_time_suffix()
    filename = f"agg_by_champion_{user_tag}_{time_suffix}.json"
    path = os.path.join(folder, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    

# Save aggregated by role
def save_agg_by_role(data: dict, user_tag: str):
    folder = get_today_folder()
    time_suffix = get_time_suffix()
    filename = f"agg_by_role_{user_tag}_{time_suffix}.json"
    path = os.path.join(folder, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


# Save aggregated by win/loss
def save_agg_by_winloss(data: dict, user_tag: str):
    folder = get_today_folder()
    time_suffix = get_time_suffix()
    filename = f"agg_by_winloss_{user_tag}_{time_suffix}.json"
    path = os.path.join(folder, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

