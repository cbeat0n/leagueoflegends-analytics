#  League of Legends Analytics Aggregator

This is a full-stack web analytics platform that processes and visualizes recent ranked match history for a League of Legends summoner using Riot’s official developer API. The tool retrieves game metadata and timeline data, applies aggregation logic (by champion, role, or win/loss), and produces interactive charts rendered in-browser.

It’s built to demonstrate real-world data engineering, backend/frontend integration, and game data insights — suitable for analysts, engineers, and portfolio reviewers alike.

This project was made in part by and using Prompt Engineering technology with Chat GPT. Not all projects are made this way but many are increasingly being developed this way.


Thank you for using this servable and I hope you enjoy & are able to increase your ELO with its visualizations.

---

##  0. Requirements

This project relies on a combination of programming libraries, development tools, API credentials, and structured project organization. Below is a complete list of everything you’ll need to run the project successfully.

---

###  Software & Tools

| Tool           | Purpose                                                                 | Download / Info                                           |
|----------------|-------------------------------------------------------------------------|-----------------------------------------------------------|
| **Python 3.10+** | Primary backend development language                                     | [https://www.python.org/downloads/](https://www.python.org/downloads/) |
| **Visual Studio Code (VSC)** | Recommended IDE for writing, editing, and debugging code          | [https://code.visualstudio.com/](https://code.visualstudio.com/) |
| **Git**        | Version control & project cloning                                       | [https://git-scm.com/](https://git-scm.com/)              |
| **Git Bash**   | Terminal environment for Windows users (Bash shell emulator)            | [https://gitforwindows.org/](https://gitforwindows.org/) |
| **Terminal / Shell** | macOS/Linux command line interface; also works on Windows with Git Bash | Preinstalled on macOS/Linux; use Git Bash on Windows     |
| **Browser (Chrome/Firefox)** | To view your Flask app locally (at `localhost:5000`)                | Any modern browser                                        |

---

###  Riot Games Developer Access

To query data, you must:

- Create an account at [https://developer.riotgames.com](https://developer.riotgames.com)
- Generate an API key (rate-limited unless upgraded to production)
- Store it in a `.env` file in your project root directory as follows:

```env
RIOT_API_KEY="your-api-key-here"
```

### Python Libraries
| Library                  | Purpose                                                      |
| ------------------------ | ------------------------------------------------------------ |
| `Flask`                  | Web server to handle routing and HTML serving                |
| `requests`               | API calls to Riot’s match and timeline endpoints             |
| `python-dotenv`          | Loads your Riot API key from `.env` securely                 |
| `pandas`                 | (Optional) Data handling in testing phases                   |
| `plotly`                 | Renders JavaScript visualizations dynamically                |
| `jinja2`                 | Renders variables inside HTML via Flask                      |
| `statistics`             | For computing means and modes in aggregation                 |
| `collections`            | For handling grouped data cleanly                            |
| `datetime`, `os`, `json` | Standard Python utilities for file paths, saving, formatting |

## 1. Instructions

This section walks you through setting up the project, creating your API key, installing dependencies, and using the app via live or saved data.

---

### Installation Steps

**Clone the Repository**

```bash
git clone https://github.com/cbeat0n/leagueoflegends-analytics.git
cd leagueoflegends-analytics
```

---

### (Optional) Create a Dev Environment
 
**In your Terminal or Git Bash:**

# macOS / Linux
```
python3 -m venv venv
source venv/bin/activate
```

# Windows
```
python -m venv venv
venv\Scripts\activate
```

**Then you can download all the Python Libraries and add them to the environment above**

### Riot API Key

You’ll need to store your Riot API key safely:

Get a developer key from https://developer.riotgames.com

Create a file in the root directory called .env

Paste the following inside:

```
RIOT_API_KEY="your-api-key-here"
```

Make sure .env is not committed to Git. It should be in your .gitignore.

### Running the App
Once setup is complete, start the Flask server:

```
python motherboard.py
```

Open your favorite browser and go to the local server at http://127.0.0.1:5000

### Using the App
**Live Pull (API Mode)**

Enter a summoner name and tag (e.g., Unearthed#NA1)
    - In the browser you only would type NA1 into the survey input, ignore the #

Choose how many recent ranked games to retrieve (5–25)

Select aggregation mode:
    - Champion
    - Role
    - Win/Loss

Submit the form to pull live data, aggregate it, and render visualizations via a button you click on.

**Load from Storage**

If data was already pulled and saved previously, you can re-render it:

Provide summoner name, choose the aggregation type.

Enter date and timestamp (from saved folder name).

This skips the Riot API and shows the stored plots instantly.

Once again click on the buttons to choose which visualizations to open.


## 2. Table of Contents

| File / Folder           | Purpose                                                                               |
| ----------------------- | ------------------------------------------------------------------------------------- |
| `motherboard.py`        | Main Flask application, handles routing and frontend logic                            |
| `riot_api.py`           | Grabs `puuid` and match IDs using summoner + tag                                      |
| `etl.py`                | Prunes and zips match metadata + timeline into usable JSON                            |
| `aggregators.py`        | Aggregates game data by win/loss, role, or champion; includes time series computation |
| `file_helpers.py`       | Auto-saves raw and aggregated data in a structured date/timestamp directory           |
| `/templates/index.html` | Frontend UI with form inputs and dynamic Plotly graphs                                |
| `/static/style.css`     | Optional styles for cleaner layout                                                    |
| `/static/plots/`        | Directory for plot images (optional if visualized in browser)                         |
| `/data/YYYY-MM-DD/`     | Automatically generated storage for raw + processed JSON data                         |
| `README.md`        | Basic information and instructions on this servable
| `Synopsis.md`        | Development lifecycle and project management commentary on the project overall
| `chatlogs.md`        | Chat logs between the developer and Chat GPT.


## 3. Data Compliance

### GDPR & Usage Outside NA Server

```
This project is developed in accordance with Riot Games’ Developer Terms of Service and Riot’s API usage guidelines.

> **Disclaimer:** This application is intended for use with North American (NA) Riot accounts only.  
> Due to regional data protection laws such as the **General Data Protection Regulation (GDPR)** enforced in the EU, it is advised that summoners on EU-based servers do **not** use this app unless they fully consent to their data being pulled and visualized.  
> The developer of this tool is based in the United States, and the application is structured to avoid direct handling or storage of personally identifiable information (PII). All user interactions are explicitly initiated and voluntarily entered.
```

### Riot Legal Information

```
"League of Legends Analytics Aggregator" isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc. Otherwise, you are responsible for your usage and compliance with Riot’s API Terms:  
https://developer.riotgames.com/docs/portal
```