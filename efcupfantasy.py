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

@st.cache_data(ttl=10)  # Short cache for debugging
def load_teams():
    if os.path.exists(TEAMS_FILE):
        try:
            with open(TEAMS_FILE, 'r') as f:
                teams = json.load(f)
                st.write(f"📂 Loaded {len(teams)} teams from {TEAMS_FILE}")
                return teams
        except Exception as e:
            st.error(f"❌ Load error: {e}")
            return []
    st.info("📂 No teams file found")
    return []

def save_team(team_data):
    try:
        teams = load_teams()
        teams.append(team_data)
        
        # FORCE WRITE with full path check
        full_path = os.path.abspath(TEAMS_FILE)
        st.write(f"💾 Writing to: {full_path}")
        
        with open(TEAMS_FILE, 'w') as f:
            json.dump(teams, f, indent=2, ensure_ascii=False)
        
        st.success(f"✅ SAVED! File size: {os.path.getsize(TEAMS_FILE)} bytes")
        return True
    except Exception as e:
        st.error(f"❌ SAVE FAILED: {e}")
        return False

# UI
st.title("🏆 EF CUP FANTASY - DEBUG MODE")
BUDGET = 100
team_name = st.text_input("🏷️ Team Name")
selected_players = st.multiselect(
    "⚽ Choose 6 players:", 
    [f"{p['name']} ({p['position']}) - ₹{p['price']}" for p in PLAYERS],
    max_selections=6
)

# Budget check
if selected_players:
    total_price = sum(int(sel.split(" - ₹")[1]) for sel in selected_players)
    st.metric("Budget", f"₹{total_price}", f"₹{BUDGET-total_price}")
    
    if total_price <= BUDGET and len(selected_players) == 6:
        st.success("✅ READY TO SAVE!")

# TEST BUTTONS
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧪 TEST SAVE", type="primary"):
        if team_name and len(selected_players) == 6:
            team_players = []
            for sel in selected_players:
                name = sel.split(" - ₹")[0].split(" (")[0]
                player = next(p for p in PLAYERS if p["name"] == name)
                team_players.append(player)
            
            success = save_team({
                "teamName": team_name,
                "players": team_players,
                "totalPrice": total_price,
                "savedAt": datetime.now().isoformat()
            })
            
            if success:
                st.balloons()
                st.rerun()
        else:
            st.error("Need name + exactly 6 players!")

with col2:
    if st.button("🔍 SHOW FILE"):
        teams = load_teams()
        st.json(teams)

with col3:
    st.download_button("💾 DOWNLOAD", json.dumps(load_teams(), indent=2), "teams.json")

# DEBUG INFO
st.sidebar.subheader("Debug")
st.sidebar.write(f"File exists: {os.path.exists(TEAMS_FILE)}")
st.sidebar.write(f"Working dir: {os.getcwd()}")
