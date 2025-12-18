import streamlit as st
from streamlit.connections import GSheetsConnection
from datetime import datetime

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
st.markdown("**Teams SAVED PERMANENTLY to Google Sheets!**")

# Connect to Google Sheets using YOUR secrets.toml
@st.cache_resource
def init_connection():
    return st.connection("google_sheets", type=GSheetsConnection)

# MAIN APP
BUDGET = 100
team_name = st.text_input("🏷️ Team Name", placeholder="Enter your team name")

player_options = [f"{p['name']} ({p['position']}) - ₹{p['price']}" for p in PLAYERS]
selected_players = st.multiselect("⚽ Choose 6 players:", player_options, max_selections=6)

# Budget calculation
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

# SAVE TO GOOGLE SHEETS
if st.button("💾 SAVE TO GOOGLE SHEETS", type="primary", use_container_width=True):
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
                
                # SAVE TO SHEETS
                conn = init_connection()
                row = {
                    "Team Name": team_name.strip(),
                    "Total Price": total_price,
                    "Players": ", ".join([p['name'] for p in team_players]),
                    "Positions": ", ".join([p['position'] for p in team_players]),
                    "Real Teams": ", ".join([p['realTeam'] for p in team_players]),
                    "Saved At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                conn.write(row, sheet="Teams")  # "Teams" = your sheet tab name
                
                st.success(f"🎉 Team '{team_name}' SAVED TO GOOGLE SHEETS!")
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Save failed: {str(e)}")

# SHOW TEAMS FROM GOOGLE SHEETS
st.subheader("📊 All Teams (Live from Google Sheets)")
try:
    conn = init_connection()
    df = conn.read(sheet="Teams")
    if df is not None and not df.empty:
        st.dataframe(df)
    else:
        st.info("👆 Save your first team to see it here!")
except Exception as e:
    st.error(f"❌ Cannot read sheets: {str(e)}")
    st.info("Check your secrets.toml and sheet sharing")
