import streamlit as st
import json
import os
from datetime import datetime

# FIXED: Define PLAYERS FIRST before any Streamlit code
PLAYERS = [
    # GOALKEEPERS
    {"id": 1, "name": "ROJIT SHRESTHA", "price": 8, "position": "GK", "isCaptain": False, "realTeam": "JOSHI JAGUARS"},
    {"id": 2, "name": "SUJAN BK", "price": 7, "position": "GK", "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 3, "name": "PRASHANNA PAUDEL", "price": 7, "position": "GK", "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 4, "name": "TANISHK THAPA", "price": 8, "position": "GK", "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 5, "name": "AAYUSH ROKA", "price": 7, "position": "GK", "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 6, "name": "SANGAM SHRESTHA", "price": 8, "position": "GK", "isCaptain": False, "realTeam": "GODAR GOATS"},

    # FORWARDS - LOWER PRICES FOR ₹100 BUDGET
    {"id": 7, "name": "SABIN DAHAL", "price": 9, "position": "FWD", "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 8, "name": "SACHIN SEN", "price": 8, "position": "FWD", "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 9, "name": "SAKAR SUBEDI", "price": 7, "position": "FWD", "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 10, "name": "SANDIL KATUWAL", "price": 8, "position": "FWD", "isCaptain": False, "realTeam": "GODAR GOATS"},
    {"id": 11, "name": "SANJAYA ADHIKARI", "price": 7, "position": "FWD", "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 12, "name": "SANKALPA SHARMA", "price": 9, "position": "FWD", "isCaptain": False, "realTeam": "JOSHI JAGUARS"},
    {"id": 13, "name": "SHRIJAN BHUSAL", "price": 9, "position": "FWD", "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 14, "name": "SHUBHAM SINGH", "price": 8, "position": "FWD", "isCaptain": False, "realTeam": "GODAR GOATS"},
    {"id": 15, "name": "SHUSHANT ADHIKARI", "price": 7, "position": "FWD", "isCaptain": False, "realTeam": "JOSHI JAGUARS"},
    {"id": 16, "name": "SHYAM MAHATO", "price": 8, "position": "FWD", "isCaptain": False, "realTeam": "GODAR GOATS"},
    {"id": 17, "name": "SUDIP BARAL", "price": 8, "position": "FWD", "isCaptain": True, "realTeam": "BENZE BULLS"},
    {"id": 18, "name": "SUJIT GURUNG", "price": 9, "position": "FWD", "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 19, "name": "SUMAN CHHETRI", "price": 8, "position": "FWD", "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 20, "name": "UNIQUE REGMI", "price": 9, "position": "FWD", "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 21, "name": "SUMAN SHARMA", "price": 9, "position": "FWD", "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 22, "name": "UDHAY THAKUR", "price": 8, "position": "FWD", "isCaptain": False, "realTeam": "GODAR GOATS"},

    # DEFENDERS - LOWEST PRICES
    {"id": 23, "name": "SAJAN ROKAYA", "price": 6, "position": "DEF", "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 24, "name": "SAMEER ACHARYA", "price": 7, "position": "DEF", "isCaptain": True, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 25, "name": "SAMIR GODAR", "price": 6, "position": "DEF", "isCaptain": True, "realTeam": "GODAR GOATS"},
    {"id": 26, "name": "SANTOSH JOSHI", "price": 7, "position": "DEF", "isCaptain": True, "realTeam": "JOSHI JAGUARS"},
    {"id": 27, "name": "SUJAL PARAJULI", "price": 6, "position": "DEF", "isCaptain": False, "realTeam": "JOSHI JAGUARS"},
    {"id": 28, "name": "SUJAL SOTI", "price": 7, "position": "DEF", "isCaptain": True, "realTeam": "SOTI SOLDIERS"},
    {"id": 29, "name": "SUJAN BHAATTA", "price": 6, "position": "DEF", "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 30, "name": "SUSHAN PANDEY", "price": 7, "position": "DEF", "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 31, "name": "SWORNIM TIMILSINA", "price": 7, "position": "DEF", "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 32, "name": "VIVEK GAUTAM", "price": 6, "position": "DEF", "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 33, "name": "ZENITH SARU", "price": 7, "position": "DEF", "isCaptain": True, "realTeam": "ZENITH ZEBRAS"},

    # FOREIGN PLAYERS
    {"id": 34, "name": "ANUJ THAPA", "price": 7, "position": "DEF", "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 35, "name": "ANUPAM BISTA", "price": 9, "position": "FWD", "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 36, "name": "TASHI SHERPA", "price": 7, "position": "FWD", "isCaptain": False, "realTeam": "BENZE BULLS"},
]

TEAMS_FILE = "saved_teams.json"

@st.cache_data
def load_teams():
    if os.path.exists(TEAMS_FILE):
        try:
            with open(TEAMS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_team(team_data):
    teams = load_teams()
    teams.append(team_data)
    with open(TEAMS_FILE, 'w') as f:
        json.dump(teams, f, indent=2, ensure_ascii=False)

def download_teams():
    teams = load_teams()
    return json.dumps(teams, indent=2, ensure_ascii=False)

# MAIN APP
st.title("🏆 EF CUP FANTASY")
st.markdown("**Create your team (₹100 budget) - 6 players max**")

BUDGET = 100
team_name = st.text_input("🏷️ Team Name", placeholder="Enter your team name")

player_options = [f"{p['name']} ({p['position']}) - ₹{p['price']}" for p in PLAYERS]
selected_players = st.multiselect("⚽ Choose 6 players:", player_options, max_selections=6)

# Budget display
if selected_players:
    total_price = sum(int(sel.split(" - ₹")[1]) for sel in selected_players)
    budget_left = BUDGET - total_price
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Players", len(selected_players), "6")
    col2.metric("Budget Used", f"₹{total_price}", f"₹{budget_left}")
    col3.metric("Status", "✅ OK" if budget_left >= 0 else "❌ Over", "Budget")
    
    if budget_left < 0:
        st.error(f"❌ Over budget by ₹{-budget_left}!")
    else:
        st.success(f"✅ Budget OK! ({len(selected_players)}/6 players)")
        st.subheader("📋 Your Team")
        for player_str in selected_players:
            st.write(f"• {player_str}")

# FIXED SAVE BUTTON - MOVED OUTSIDE COLUMNS
st.subheader("Actions")
if st.button("💾 SAVE TEAM", type="primary", use_container_width=True):
    if not team_name.strip():
        st.error("❌ Enter a team name first!")
    elif len(selected_players) != 6:
        st.error(f"❌ Select exactly 6 players! (You have {len(selected_players)})")
    else:
        total_price = sum(int(sel.split(" - ₹")[1]) for sel in selected_players)
        if total_price > BUDGET:
            st.error(f"❌ Over budget! Total: ₹{total_price}")
        else:
            try:
                # Convert to player objects
                team_players = []
                for sel in selected_players:
                    name = sel.split(" - ₹")[0].split(" (")[0]
                    player = next(p for p in PLAYERS if p["name"] == name)
                    team_players.append(player)
                
                save_team({
                    "teamName": team_name.strip(),
                    "players": team_players,
                    "totalPrice": total_price,
                    "savedAt": datetime.now().isoformat()
                })
                
                st.success(f"🎉 Team '{team_name}' SAVED! (₹{total_price}/100)")
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Save failed: {str(e)}")

# Download button
st.download_button(
    "💾 DOWNLOAD TEAMS", 
    download_teams(), 
    "saved_teams.json", 
    "application/json"
)

# TABS
tab1, tab2 = st.tabs(["📱 My Teams", "🏆 All Teams"])

with tab1:
    teams = load_teams()
    if not teams:
        st.info("👆 Save your first team!")
    else:
        for team in teams[-5:]:
            st.markdown(f"**{team['teamName']}** - ₹{team['totalPrice']} - {team['savedAt'][:10]}")

with tab2:
    teams = load_teams()
    if not teams:
        st.info("No teams saved yet!")
    else:
        for team in teams:
            with st.expander(f"{team['teamName']} - ₹{team['totalPrice']}"):
                st.caption(f"Saved: {team['savedAt'][:16]}")
                for player in team['players']:
                    st.write(f"⚽ {player['name']} ({player['position']})")
