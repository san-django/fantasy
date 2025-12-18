import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit as st
from google.oauth2 import service_account
import gspread

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

st.title("🏆 EF CUP FANTASY - GOOGLE SHEETS ✅")
st.markdown("**Teams SAVED PERMANENTLY to Google Sheets!**")

# Load credentials from secrets.toml
@st.cache_resource
def load_sheets():
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["google_sheets"],
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )
    client = gspread.authorize(creds)
    
    # Open or create sheet
    try:
        sheet = client.open("EF Cup Fantasy Teams")
    except:
        sheet = client.create("EF Cup Fantasy Teams")
    
    # Get or create "Teams" worksheet
    try:
        worksheet = sheet.worksheet("Teams")
    except:
        worksheet = sheet.add_worksheet(title="Teams", rows=1000, cols=10)
        # Add headers
        worksheet.append_row(["Team Name", "Total Price", "Players", "Positions", "Real Teams", "Saved At"])
    
    return worksheet

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
    
    if budget_left >= 0:
        st.success(f"✅ Budget OK! ({len(selected_players)}/6 players)")
        st.subheader("📋 Your Team")
        for player_str in selected_players:
            st.write(f"• {player_str}")

# SAVE BUTTON - FIXED SYNTAX
if st.button("💾 SAVE TO GOOGLE SHEETS", type="primary", use_container_width=True):
    if not team_name.strip():
        st.error("❌ Enter team name!")
    elif len(selected_players) != 6:
        st.error(f"❌ Need exactly 6 players!")
    else:
        total_price = sum(int(sel.split(" - ₹")[1]) for sel in selected_players)
        if total_price > BUDGET:
            st.error(f"❌ Over budget ₹{total_price}!")
        else:
            try:
                worksheet = load_sheets()
                
                # Get player details
                team_players = []
                for sel in selected_players:
                    name = sel.split(" - ₹")[0].split(" (")[0]
                    player = next(p for p in PLAYERS if p["name"] == name)
                    team_players.append(player)
                
                # ✅ CORRECT SYNTAX - append_row()
                worksheet.append_row([
                    team_name.strip(),
                    total_price,
                    ", ".join([p['name'] for p in team_players]),
                    ", ".join([p['position'] for p in team_players]),
                    ", ".join([p['realTeam'] for p in team_players]),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ])
                
                st.success(f"🎉 '{team_name}' SAVED TO GOOGLE SHEETS!")
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"❌ ERROR: {str(e)}")
                st.info("Check: 1) secrets.toml 2) Sheet shared with service account")

# SHOW TEAMS FROM SHEETS
st.subheader("📊 Live Teams from Google Sheets")
try:
    worksheet = load_sheets()
    records = worksheet.get_all_records()
    if records:
        df = pd.DataFrame(records)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("👆 Save first team!")
except Exception as e:
    st.error(f"❌ Read error: {str(e)}")
