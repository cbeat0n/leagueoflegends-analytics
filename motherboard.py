from flask import Flask, render_template, request
from datetime import datetime
from pathlib import Path
import os
import json

from utils.riot_api import get_puuid, get_match_ids
from utils.etl import merge_match_data
from utils.aggregators import (
    aggregate_by_champ,
    aggregate_by_role,
    aggregate_by_winloss,
    compute_timeseries_stats,
    compute_common_stats
)
from utils.file_helpers import (
    save_raw_games,
    save_agg_by_champion,
    save_agg_by_role,
    save_agg_by_winloss,
    get_today_folder,
    get_time_suffix
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # === Form Inputs ===
        summoner_name = request.form.get("summonerName")
        tag_line = request.form.get("tagLine")
        game_count = int(request.form.get("gameCount"))
        agg_type = request.form.get("aggregationType")  # champ / role / winloss

        # === Step 0: Validate OK gameCount ===
        if not (5 <= game_count <= 25):
            return render_template("index.html", error="Game count must be between 5 and 25")

        # === Step 1: Get PUUID ===
        puuid = get_puuid(summoner_name, tag_line)
        if not puuid:
            return render_template("index.html", error="Could not fetch PUUID")

        # === Step 2: Get Match IDs ===
        match_ids = get_match_ids(puuid, count=game_count)
        if not match_ids:
            return render_template("index.html", error="No match data found")

        # === Step 3: Get Zipped Data ===
        zipped_games = []
        for match_id in match_ids:
            zipped = merge_match_data(match_id)
            if zipped:
                zipped_games.append(zipped)

        if not zipped_games:
            return render_template("index.html", error="Failed to process matches")

        # === Step 4: Generate timestamp & save raw ===
        user_tag = summoner_name.lower()
        
        

        save_raw_games(zipped_games, user_tag)

        # === Step 5: Aggregate + Save ===
        champ_data = aggregate_by_champ(zipped_games, puuid)
        role_data = aggregate_by_role(zipped_games, puuid)
        winloss_data = aggregate_by_winloss(zipped_games, puuid)

        save_agg_by_champion(champ_data, user_tag)
        save_agg_by_role(role_data, user_tag)
        save_agg_by_winloss(winloss_data, user_tag)

        # === Step 6: Return selected aggregation ===
        if agg_type == "champion":
            aggregation_data = champ_data
        elif agg_type == "role":
            aggregation_data = role_data
        else:
            aggregation_data = winloss_data

        timestamp = get_time_suffix()
        datestamp = datetime.today().strftime('%Y-%m-%d')
        
        return render_template("index.html",
                               aggregation_data=aggregation_data,
                               aggregation_type=agg_type,
                               timestamp=timestamp,
                               user_tag=user_tag,
                               date = datestamp,
                               success=True)

    return render_template("index.html")


@app.route("/load", methods=["GET","POST"])
def load_old_aggregation():
    user_tag = request.form.get("userTag").lower()
    date = request.form.get("date")
    timestamp = request.form.get("timestamp")
    agg_type = request.form.get("aggregationType")

    filename = f"agg_by_{agg_type}_{user_tag}_{timestamp}.json"
    filepath = os.path.join("data", date, filename)

    if not os.path.exists(filepath):
        return render_template("index.html", error="File not found")

    with open(filepath, "r") as f:
        aggregation_data = json.load(f)

    return render_template("index.html",
                           aggregation_data=aggregation_data,
                           aggregation_type=agg_type,
                           timestamp=timestamp,
                           user_tag=user_tag,
                           date = date,
                           success=True)

@app.route("/visualize/<component>", methods=["GET"])
def visualize_component(component):
    user_tag = request.args.get("userTag")
    timestamp = request.args.get("timestamp")
    agg_type = request.args.get("aggregationType")
    date = request.args.get("date")

    if not all([user_tag, timestamp, agg_type, date]):
        return f"<h1>Missing required data</h1><p>{user_tag=}, {timestamp=}, {agg_type=}, {date=}</p>"

    try:
        filename = f"agg_by_{agg_type}_{user_tag}_{timestamp}.json"
        path = os.path.join("data", date, filename)
        with open(path, "r") as f:
            full_data = json.load(f)
            data = full_data.get(component, {})
    except Exception as e:
        return f"<h1>Error loading data for {component}</h1><p>{e}</p>"

    return render_template("component_view.html", component=component, aggregation_data=data)

if __name__ == '__main__':
    app.run(debug=True)