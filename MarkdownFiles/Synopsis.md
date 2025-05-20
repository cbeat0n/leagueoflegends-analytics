# Synopsis.md

## Why This Product Was Made

This project was born from the intersection of two personal and professional passions: **data engineering / machine learning** and **League of Legends**.

As both a player and a developer, I’ve often wondered: _What if we could take real, granular performance data and turn it into something actionable — without needing a PhD in statistics or game theory?_ Most current tools provide only surface-level insights (e.g., winrates, match history), but lack customizability, cross-game aggregation, or detailed trends over time.

This tool aims to change that — and answer a few core questions:

- Can we create a **flexible backend architecture** that supports multiple styles of aggregation (by role, champion, win/loss)?
- Can we **visualize trends across games** in a clean, structured, and scalable way?
- Can we build something with real **engineering discipline** that could evolve into more advanced tooling like predictive analytics or build optimization?

The **practical value** of this app is simple:  
It allows players to reflect on _their own gameplay patterns_ across ranked games — especially trends in vision score, damage distribution, gold income, and more — and use those to **incrementally improve decision-making**, thereby increasing win potential and ultimately climbing in ranked ELO.

At the same time, this was a sandbox to explore the **intersection of analytics, engineering, and deployment** in a well-scoped, real-world project. It simulates the kind of data lifecycle you’d find in industry: ingestion, processing, aggregation, visualization, and user interaction.

In other words:  
It’s a **data engineering product disguised as a gaming tool** — one that blends personal interest with substance.


## Development Process & Project Architecture

### Development Commentary

This project was built over the course of several development cycles, beginning with exploratory data pulls and culminating in a fully functional Flask web application. The core challenge was bridging the **data engineering mindset** (ETL, structure, pipelines) with **usability and front-end presentation**.

Development began with manually pulling match data using the Riot API to understand the structure and richness of the game JSON. From there, a toy dataset was used to simulate and test functions before writing the modular architecture. Throughout the project, time was taken to analyze actual pain points in Riot’s live games (e.g., remakes, forfeits, inconsistent match quality), and strategies were implemented to filter or mitigate that noise.

An early decision was made to separate engineering tasks into **four layers**:
1. **API ingestion (riot_api.py)** – lightweight, reads only what is needed.
2. **ETL processing (etl.py)** – joins metadata and timeline, trims excess.
3. **Aggregation & analysis (aggregators.py)** – aggregates trends across games.
4. **Data persistence (file_helpers.py)** – saves structured folders of data, by date + tag.

On top of these, a `motherboard.py` app was created using Flask to route data, handle user inputs, and render outputs using Jinja2 and Plotly. The frontend itself (index.html + style.css) supports dual workflows: one for **live Riot API pulls** and one for **loading previously saved data**.

There were also project management decisions made along the way:
- A deliberate choice to avoid predictive machine learning in the MVP to retain clarity and scope.
- Avoiding advice or insight recommendations, staying grounded in **objective statistics** only.
- Use of simple JSON files for storage, instead of databases, to improve transparency for employers.

Each module was treated as its own microservice with clean inputs and outputs, meaning the architecture could scale with ease.

---

### Project Architecture

```plaintext
lol_dashboard_project/
│
├── app.py / motherboard.py       # Flask web app (entry point)
├── riot_api.py                   # Riot API querying (PUUID, match IDs)
├── etl.py                        # Metadata/timeline fetching and merging
├── aggregators.py                # Statistical aggregation and time series
├── file_helpers.py               # Saving raw and aggregated JSON by date
│
├── /data/                        # Raw & processed game data (by date/tag)
│   └── /YYYY-MM-DD/
│       ├── raw_*.json
│       ├── agg_by_champion_*.json
│       ├── agg_by_role_*.json
│       └── agg_by_winloss_*.json
│
├── /static/
│   ├── style.css                 # Optional styling
│   └── /plots/                   # (Optional) stored PNGs
│
├── /templates/
│   └── index.html                # Main web interface (Jinja + Plotly)
│
└── .env                          # Riot API Key (not committed to Git)
```

This setup ensures separation of concerns, modularity, and ease of testing. Each file can be worked on independently while still contributing to the overall pipeline — and new features (like predictive modeling or external database integration) could be added without rearchitecting the entire system.

## Development Hurdles & Lessons Learned

While the project was ultimately successful in delivering its core features, it also encountered several important development hurdles — both technical and structural. These challenges helped shape the final product and provided insight into what real-world data projects often entail: **incomplete data, fragile inputs, and unexpected dependencies**.

---

### In-Game Data Issues

One of the earliest challenges emerged from Riot’s **matchmaking ecosystem** itself: remakes and early forfeits.

- Games where players **quit before 4 minutes** or **teams surrendered at 15 minutes** were still technically listed in the API call but often resulted in skewed or **incomplete statistical data**.
- Initially, this created misleading summaries (e.g., 2-minute games registering 0 vision, no CS, etc.)
- The decision was made to restart data acquisition at these breakpoints in order to maintain clean data for clean API pulls according to the age old data analytics saying: Junk In, Junk Out.

This challenge highlights a key point in real-world data: **not all valid data is useful data**.  

---

### Frontend Rendering & Variable Scope

In the frontend, one significant roadblock was the **interaction between Flask (Jinja2) and JavaScript (Plotly)**:

- Jinja variables like `{{ aggregation_data | tojson }}` initially threw JavaScript syntax errors due to incorrect scoping, timing, or unsafe rendering contexts.
- The issue was resolved by **properly deferring JSON assignments** to later in the .html file as well as breaking up declaration into two separate partitions to deliberately avoid confusion during rendering.
- Mistakes in **template variable names** (e.g., `plot_data` vs. `summary_data` vs. `aggregation_data`) caused confusion until naming conventions were standardized.

This became a powerful reminder that **cross-language coordination matters**: passing data from backend Python to frontend JS requires thoughtful orchestration, even in a lightweight Flask app.

---

### Conceptual Design Conflicts

There were also moments of architectural debate:

- Should we generate *and save plots* as PNGs, or render everything client-side with Plotly?
    - Decision: Keep frontend interactive, store raw JSON only.
- Should the app support *single-game visualizations*, or only aggregates?
    - Decision: Focus on **multi-game trends** for cleaner UX, cleaner analysis, and reduced scope creep.
- Should data be saved with plain indices (e.g., `game1.json`) or **timestamped filenames**?
    - Decision: Use timestamps for **disambiguation and traceability**.

Each decision reflects a balance between **technical practicality** and **user experience**, which ultimately informed both how the app works — and how cleanly it performs in real usage.

---

### Summary of Major Pain Points

| Category        | Issue                                                                 | Resolution                                             |
|----------------|------------------------------------------------------------------------|--------------------------------------------------------|
| In-game data    | Remakes, short games, surrenders skewing stats                        | Skipped games < 4 minutes, noted in Synopsis           |
| Jinja variables | Improper instantiation of `tojson` data into JS                       | Refactored variable flow, moved JSON safely into script|
| Plot logic      | Deciding between saved PNGs vs. dynamic Plotly visuals                | Client-side Plotly used exclusively                    |
| Aggregation     | Unexpected lack of per-game detail post-aggregation                   | Adjusted expectations — showed only summaries          |
| Summoner input  | Some Riot IDs caused failed PUUID lookups due to incorrect formatting | Added tagLine validation and quoting fixes             |

These hurdles improved the project’s robustness and revealed the kinds of **scrappy, adaptable debugging** that often defines good engineering.

## Future Expansion & Competitive Differentiators

While this project already stands as a full-cycle data analytics application, its modular design and clear functional separation leave ample room for future development — both in terms of **feature set** and **market competitiveness**.

---

### Possible Feature Expansions

1. **Predictive Analytics & Machine Learning**
   - Implement models to estimate win probability based on player performance, item builds, or rune selections.
   - Example: "Would switching from Conqueror to First Strike yield a higher winrate in jungle matchups?"
   - This could be integrated into a Phase 2 `ml_models.py` and frontend slider inputs.

2. **Performance Benchmarking by ELO**
   - Compare the user’s metrics (vision score, gold per minute, etc.) against **rank-tier averages**.
   - Could help users gauge what “good” looks like at their level, similar to U.GG or OP.GG but with **personalized deltas**.

3. **Cross-Player Data Aggregation**
   - Currently, the tool is designed for **individual players**.
   - With minor adjustments, it could support multiple users for comparative dashboards or team-based scrims.

4. **Role-Specific or Champion-Specific Insights**
   - Offer deeper insights tailored to unique playstyles (e.g., roaming mids, farming supports, power-farming junglers).
   - Extend aggregators to analyze subtypes within roles.

5. **Database + User Login Integration**
   - Use PostgreSQL or Firebase to let players log in and track their performance across weeks or seasons.
   - This would allow **long-term trends** and **returning user support**.

---

### Competitive Positioning

This tool already sets itself apart in several key ways:

- It provides **custom aggregation logic** that is _not_ limited to static tiers or global stats.
- The visualizations are **fully dynamic**, leveraging Plotly for detailed per-game breakdowns.
- The application is **open-source and modular**, making it ideal for employers, analysts, or developers to extend.

However, larger platforms like U.GG and Blitz remain dominant due to integration, speed, and polish. To compete:

- The UI/UX could be upgraded using **React or Next.js**.
- The app could expand into a **browser extension or desktop client**.
- Real-time feedback based on post-game analysis could be implemented via **event streaming or message queues**.

---

### TL;DR – Future Value

This project is a strong baseline for any number of professional or public-facing applications — ranging from:
- **Data analyst portfolios**
- **Solo queue coaching**
- **Player scouting dashboards**
- **Esports analytics workflows**

Its extensibility is its greatest asset — the structure is ready, and the vision can evolve.
