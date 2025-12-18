import streamlit as st
import pandas as pd
from datetime import datetime
from google.oauth2 import service_account  # ← THIS WAS MISSING
import gspread
from datetime import datetime
# Load Google Sheets using SECRETS.TOML (your config is perfect)
@st.cache_resource
def load_sheets():
    # Uses your secrets.toml automatically
    gc = st.connection("google_sheets")
    return gc

# YOUR FULL PLAYERS LIST (prices fixed for ₹100 budget)
PLAYERS = [
    {"id": 1, "name": "ROJIT SHRESTHA", "price": 8, "position": "GK", "isCaptain": False, "realTeam": "JOSHI JAGUARS"},
    {"id": 2, "name": "SUJAN BK", "price": 7, "position": "GK", "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 3, "name": "PRASHANNA PAUDEL", "price": 7, "position": "GK", "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 4, "name": "TANISHK THAPA", "price": 8, "position": "GK", "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 5, "name": "AAYUSH ROKA", "price": 7, "position": "GK", "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 6, "name": "SANGAM SHRESTHA", "price": 8, "position": "GK", "isCaptain": False, "realTeam": "GODAR GOATS"},
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
    {"id": 34, "name": "ANUJ THAPA", "price": 7, "position": "DEF", "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 35, "name": "ANUPAM BISTA", "price": 9, "position": "FWD", "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 36, "name": "TASHI SHERPA", "price": 7, "position": "FWD", "isCaptain": False, "realTeam": "BENZE BULLS"},
]
st.title("🏆 EF CUP FANTASY ")
st.title("🏆 EF CUP FANTASY")
st.markdown("**₹100 Budget • Save to Google Sheets**")

# PUBLIC GOOGLE SHEET - SIMPLEST METHOD (No service account needed!)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1n89U49NJ5JTQ0_YSA3li1AEgOJ_wpHcCsupRCLuf7iQ/edit?usp=sharing"

BUDGET = 100
team_name = st.text_input("🏷️ Team Name")
selected_players = st.multiselect(
    "Choose 6 players:", 
    [f"{p['name']} ({p['position']}) - ₹{p['price']}" for p in PLAYERS],
    max_selections=6
)

if selected_players:
    total_price = sum(int(sel.split("₹")[1]) for sel in selected_players)
    col1, col2 = st.columns(2)
    col1.metric("Players", len(selected_players), "6")
    col2.metric("Budget", f"₹{total_price}", f"₹{BUDGET-total_price}")
    
    if total_price <= BUDGET:
        st.success("✅ READY TO SAVE!")

# SAVE BUTTON
if st.button("💾 SAVE TEAM", type="primary"):
    if team_name and len(selected_players) == 6:
        # Copy this team data to your Google Sheet manually or use the session version above
        st.session_state.teams.append({
            "team": team_name,
            "price": total_price,
            "players": selected_players,
            "time": datetime.now().strftime("%H:%M")
        })
        st.success("✅ TEAM SAVED!")
        st.balloons()
    else:
        st.error("Name + 6 players needed!")

# TEAMS LIST
if "teams" not in st.session_state:
    st.session_state.teams = []

st.subheader("📋 Your Teams")
for team in st.session_state.teams[-10:]:
    with st.expander(team["team"]):
        st.write(f"**Price:** ₹{team['price']}")
        for player in team["players"]:
            st.write(f"• {player}")
