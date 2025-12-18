
import streamlit as st
import json
import os
from datetime import datetime

# Sample player data
players = [

    # GOALKEEPERS
    {"id": 1, "name": "ROJIT SHRESTHA", "price": 10, "position": "GK",
        "isCaptain": False, "realTeam": "JOSHI JAGUARS"},
    {"id": 2, "name": "SUJAN BK", "price": 8, "position": "GK",
        "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 3, "name": "PRASHANNA PAUDEL", "price": 7, "position": "GK",
        "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 4, "name": "TANISHK THAPA", "price": 9, "position": "GK",
        "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 5, "name": "AAYUSH ROKA", "price": 8, "position": "GK",
        "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 6, "name": "SANGAM SHRESTHA", "price": 10, "position": "GK",
        "isCaptain": False, "realTeam": "GODAR GOATS"},

    # FORWARDS
    {"id": 7, "name": "SABIN DAHAL", "price": 10, "position": "FWD",
        "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 8, "name": "SACHIN SEN", "price": 8, "position": "FWD",
        "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 9, "name": "SAKAR SUBEDI", "price": 7, "position": "FWD",
        "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 10, "name": "SANDIL KATUWAL", "price": 9, "position": "FWD",
        "isCaptain": False, "realTeam": "GODAR GOATS"},
    {"id": 11, "name": "SANJAYA ADHIKARI", "price": 8, "position": "FWD",
        "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 12, "name": "SANKALPA SHARMA", "price": 10, "position": "FWD",
        "isCaptain": False, "realTeam": "JOSHI JAGUARS"},
    {"id": 13, "name": "SHRIJAN BHUSAL", "price": 10, "position": "FWD",
        "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 14, "name": "SHUBHAM SINGH", "price": 8, "position": "FWD",
        "isCaptain": False, "realTeam": "GODAR GOATS"},
    {"id": 15, "name": "SHUSHANT ADHIKARI", "price": 7, "position": "FWD",
        "isCaptain": False, "realTeam": "JOSHI JAGAURS"},
    {"id": 16, "name": "SHYAM MAHATO", "price": 9, "position": "FWD",
        "isCaptain": False, "realTeam": "GODAR GOATS"},
    {"id": 17, "name": "SUDIP BARAL", "price": 8, "position": "FWD",
        "isCaptain": True, "realTeam": "BENZE BULLS"},
    {"id": 18, "name": "SUJIT GURUNG", "price": 10, "position": "FWD",
        "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 19, "name": "SUMAN CHHETRI", "price": 8, "position": "FWD",
        "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 20, "name": "UNIQUE REGMI", "price": 10, "position": "FWD",
        "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 21, "name": "SUMAN SHARMA", "price": 10, "position": "FWD",
        "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 22, "name": "UDHAY THAKUR", "price": 8, "position": "FWD",
        "isCaptain": False, "realTeam": "GODAR GOATS"},


    # DEFENDERS
    {"id": 23, "name": "SAJAN ROKAYA", "price": 7, "position": "DEF",
        "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 24, "name": "SAMEER ACHARYA", "price": 9, "position": "DEF",
        "isCaptain": True, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 25, "name": "SAMIR GODAR", "price": 8, "position": "DEF",
        "isCaptain": True, "realTeam": "GODAR GOATS"},
    {"id": 26, "name": "SANTOSH JOSHI", "price": 10, "position": "DEF",
        "isCaptain": True, "realTeam": "JOSHI JAGUARS"},
    {"id": 27, "name": "SUJAL PARAJULI", "price": 7, "position": "DEF",
        "isCaptain": False, "realTeam": "JOSHI JAGUARS"},
    {"id": 28, "name": "SUJAL SOTI", "price": 9, "position": "DEF",
        "isCaptain": True, "realTeam": "SOTI SOLDIERS"},
    {"id": 29, "name": "SUJAN BHAATTA", "price": 8, "position": "DEF",
        "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 30, "name": "SUSHAN PANDEY", "price": 10, "position": "DEF",
        "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 31, "name": "SWORNIM TIMILSINA", "price": 10, "position": "DEF",
        "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 32, "name": "VIVEK GAUTAM", "price": 7, "position": "DEF",
        "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 33, "name": "ZENITH SARU", "price": 9, "position": "DEF",
        "isCaptain": True, "realTeam": "ZENITH ZEBRAS"},

    # FOREIGN PLAYERS
    {"id": 34, "name": "ANUJ THAPA", "price": 8, "position": "DEF",
        "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 35, "name": "ANUPAM BISTA", "price": 10, "position": "FWD",
        "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 36, "name": "TASHI SHERPA", "price": 7, "position": "FWD",
        "isCaptain": False, "realTeam": "BENZE BULLS"},
]


# Load/save teams to YOUR local file
TEAMS_FILE = "saved_teams.json"

@st.cache_data
def load_teams():
    if os.path.exists(TEAMS_FILE):
        with open(TEAMS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_team(team_data):
    teams = load_teams()
    teams.append(team_data)
    with open(TEAMS_FILE, 'w') as f:
        json.dump(teams, f, indent=2)

st.title("🏆 EF CUP FANTASY")
st.markdown("### Create your team (₹100 budget)")

# Budget check
BUDGET = 100

# Team name
team_name = st.text_input("Team Name")

# Player selection (fixed reference to PLAYERS)
st.subheader("Select Players")
selected_players = st.multiselect(
    "Choose 6 players (₹100 budget):",
    [f"{p['name']} ({p['position']}) - ₹{p['price']}" for p in PLAYERS],
    max_selections=6
)

# Calculate total cost and check budget
if selected_players:
    total_price = 0
    team_players_data = []
    for sel in selected_players:
        name_pos_price = sel.split(" - ₹")
        name = name_pos_price[0].split(" (")[0]
        price = int(name_pos_price[1])
        total_price += price
        player = next(p for p in PLAYERS if p["name"] == name)
        team_players_data.append(player)
    
    # Show budget status
    budget_left = BUDGET - total_price
    st.metric("Budget Used", f"₹{total_price}", f"₹{budget_left}")
    
    if budget_left < 0:
        st.error("❌ Over budget!")
    else:
        st.success(f"✅ **YOUR TEAM ({len(selected_players)}/6)** - Budget OK!")
        for player_str in selected_players:
            st.write(f"• {player_str}")

# Save button with validation
if st.button("💾 SAVE TEAM") and len(selected_players) == 6 and team_name:
    total_price = sum(int(sel.split(" - ₹")[1]) for sel in selected_players)
    
    if total_price > BUDGET:
        st.error("Cannot save: Over budget!")
    else:
        # Convert selection back to player data
        team_players = []
        for sel in selected_players:
            name_pos_price = sel.split(" - ₹")
            name = name_pos_price[0].split(" (")[0]
            player = next(p for p in PLAYERS if p["name"] == name)
            team_players.append(player)
        
        save_team({
            "teamName": team_name,
            "players": team_players,
            "totalPrice": total_price,
            "savedAt": datetime.now().isoformat()
        })
        
        st.balloons()
        st.success(f"✅ Team '{team_name}' saved! (₹{total_price}/100)")
        st.rerun()

# Tabs for viewing teams (FIXED SYNTAX ERROR HERE)
tab1, tab2 = st.tabs(["📱 My Teams", "🏆 All Teams"])

with tab1:
    st.subheader("Your Recent Teams")
    teams = load_teams()
    if not teams:
        st.info("👆 Create and save teams above!")
    else:
        for team in teams[-5:]:  # Last 5 teams
            st.markdown(f"**{team['teamName']}** - ₹{team['totalPrice']} - {team['savedAt'][:10]}")

with tab2:
    st.subheader("All Saved Teams")
    teams = load_teams()
    if not teams:
        st.info("No teams saved yet!")
    else:
        for team in teams:
            with st.expander(f"{team['teamName']} - ₹{team['totalPrice']}"):
                st.write(f"**Saved:** {team['savedAt'][:16]}")
                for player in team['players']:
                    st.write(f"• {player['name']} ({player['position']}) - {player['realTeam']}")
