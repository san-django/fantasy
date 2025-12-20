import streamlit as st
from datetime import datetime
import pandas as pd
import gspread
from google.oauth2 import service_account

# COMPLETE 36 PLAYERS - FIXED PRICES FOR ₹100 BUDGET
PLAYERS = [
    # GOALKEEPERS
    {"id": 1, "name": "ROJIT SHRESTHA", "price": 8, "position": "GK", "realTeam": "JOSHI JAGUARS"},
    {"id": 2, "name": "SUJAN BK", "price": 7, "position": "GK", "realTeam": "SOTI SOLDIERS"},
    {"id": 3, "name": "PRASHANNA PAUDEL", "price": 7, "position": "GK", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 4, "name": "TANISHK THAPA", "price": 8, "position": "GK", "realTeam": "ZENITH ZEBRAS"},
    {"id": 5, "name": "AAYUSH ROKA", "price": 7, "position": "GK", "realTeam": "BENZE BULLS"},
    {"id": 6, "name": "SANGAM SHRESTHA", "price": 8, "position": "GK", "realTeam": "GODAR GOATS"},
    
    # FORWARDS
    {"id": 7, "name": "SABIN DAHAL", "price": 9, "position": "FWD", "realTeam": "BENZE BULLS"},
    {"id": 8, "name": "SACHIN SEN", "price": 8, "position": "FWD", "realTeam": "ZENITH ZEBRAS"},
    {"id": 9, "name": "SAKAR SUBEDI", "price": 7, "position": "FWD", "realTeam": "BENZE BULLS"},
    {"id": 10, "name": "SANDIL KATUWAL", "price": 8, "position": "FWD", "realTeam": "GODAR GOATS"},
    {"id": 11, "name": "SANJAYA ADHIKARI", "price": 7, "position": "FWD", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 12, "name": "SANKALPA SHARMA", "price": 9, "position": "FWD", "realTeam": "JOSHI JAGUARS"},
    {"id": 13, "name": "SHRIJAN BHUSAL", "price": 9, "position": "FWD", "realTeam": "ZENITH ZEBRAS"},
    {"id": 14, "name": "SHUBHAM SINGH", "price": 8, "position": "FWD", "realTeam": "GODAR GOATS"},
    {"id": 15, "name": "SHUSHANT ADHIKARI", "price": 7, "position": "FWD", "realTeam": "JOSHI JAGUARS"},
    {"id": 16, "name": "SHYAM MAHATO", "price": 8, "position": "FWD", "realTeam": "GODAR GOATS"},
    {"id": 17, "name": "SUDIP BARAL", "price": 8, "position": "FWD", "realTeam": "BENZE BULLS"},
    {"id": 18, "name": "SUJIT GURUNG", "price": 9, "position": "FWD", "realTeam": "ZENITH ZEBRAS"},
    {"id": 19, "name": "SUMAN CHHETRI", "price": 8, "position": "FWD", "realTeam": "SOTI SOLDIERS"},
    {"id": 20, "name": "UNIQUE REGMI", "price": 9, "position": "FWD", "realTeam": "SOTI SOLDIERS"},
    {"id": 21, "name": "SUMAN SHARMA", "price": 9, "position": "FWD", "realTeam": "SOTI SOLDIERS"},
    {"id": 22, "name": "UDHAY THAKUR", "price": 8, "position": "FWD", "realTeam": "GODAR GOATS"},
    
    # DEFENDERS (CHEAPEST)
    {"id": 23, "name": "SAJAN ROKAYA", "price": 6, "position": "DEF", "realTeam": "ZENITH ZEBRAS"},
    {"id": 24, "name": "SAMEER ACHARYA", "price": 7, "position": "DEF", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 25, "name": "SAMIR GODAR", "price": 6, "position": "DEF", "realTeam": "GODAR GOATS"},
    {"id": 26, "name": "SANTOSH JOSHI", "price": 7, "position": "DEF", "realTeam": "JOSHI JAGUARS"},
    {"id": 27, "name": "SUJAL PARAJULI", "price": 6, "position": "DEF", "realTeam": "JOSHI JAGUARS"},
    {"id": 28, "name": "SUJAL SOTI", "price": 7, "position": "DEF", "realTeam": "SOTI SOLDIERS"},
    {"id": 29, "name": "SUJAN BHAATTA", "price": 6, "position": "DEF", "realTeam": "SOTI SOLDIERS"},
    {"id": 30, "name": "SUSHAN PANDEY", "price": 7, "position": "DEF", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 31, "name": "SWORNIM TIMILSINA", "price": 7, "position": "DEF", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 32, "name": "VIVEK GAUTAM", "price": 6, "position": "DEF", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 33, "name": "ZENITH SARU", "price": 7, "position": "DEF", "realTeam": "ZENITH ZEBRAS"},
    
    # FOREIGN PLAYERS
    {"id": 34, "name": "ANUJ THAPA", "price": 7, "position": "DEF", "realTeam": "BENZE BULLS"},
    {"id": 35, "name": "ANUPAM BISTA", "price": 9, "position": "FWD", "realTeam": "BENZE BULLS"},
    {"id": 36, "name": "TASHI SHERPA", "price": 7, "position": "FWD", "realTeam": "BENZE BULLS"},
]

# YOUR SHEET ID HERE (replace with your actual ID)
SHEET_ID = "1n89U49NJ5JTQ0_YSA3li1AEgOJ_wpHcCsupRCLuf7iQ"  # ← PASTE YOUR SHEET ID

@st.cache_resource
def connect_sheets():
    # Simple public sheet access
    gc = gspread.service_account()
    sheet = gc.open_by_key(SHEET_ID)
    return sheet.sheet1

st.title("🏆 EF CUP FANTASY LEAGUE")
st.markdown("**Public League - Everyone's teams saved LIVE!**")

# MAIN APP (same beautiful interface)
BUDGET = 100
team_name = st.text_input("🏷️ **Team Name**")
owner_name = st.text_input("👤 **Your Name**")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 🧤 **Goalkeepers**")
    gk_options = [f"{p['name']} ₹{p['price']}" for p in PLAYERS if p['position'] == 'GK']
    selected_gk = st.multiselect("GK", gk_options, max_selections=1)

with col2:
    st.markdown("### ⚽ **Forwards**")
    fwd_options = [f"{p['name']} ₹{p['price']}" for p in PLAYERS if p['position'] == 'FWD']
    selected_fwd = st.multiselect("FWD", fwd_options, max_selections=3)

with col3:
    st.markdown("### 🛡️ **Defenders**")
    def_options = [f"{p['name']} ₹{p['price']}" for p in PLAYERS if p['position'] == 'DEF']
    selected_def = st.multiselect("DEF", def_options, max_selections=2)

selected_players = selected_gk + selected_fwd + selected_def

# Budget display
if selected_players:
    total_price = sum(int(p.split("₹")[1]) for p in selected_players)
    budget_left = BUDGET - total_price
    
    col1, col2, col3 = st.columns([1,2,1])
    col1.metric("👥 Players", len(selected_players), "6")
    col2.metric("💰 Budget", f"₹{total_price}", f"₹{budget_left}")
    col3.metric("✅ Status", "OK" if budget_left >= 0 else "OVER", "Budget")
    
    if budget_left >= 0:
        st.success(f"✅ **Budget OK!** ({len(selected_players)}/6)")
        st.markdown("### 📋 **Your Team**")
        for player in selected_players:
            st.write(f"• {player}")

# 🚀 SAVE TO PUBLIC GOOGLE SHEETS
if st.button("💾 **SAVE TO PUBLIC LEAGUE**", type="primary", use_container_width=True):
    if not team_name or not owner_name:
        st.error("❌ **Enter Team Name & Your Name!**")
    elif len(selected_players) != 6:
        st.error(f"❌ **Need exactly 6 players!**")
    else:
        total_price = sum(int(p.split("₹")[1]) for p in selected_players)
        if total_price > BUDGET:
            st.error(f"❌ **Over budget!**")
        else:
            try:
                worksheet = connect_sheets()
                
                # Get full player data
                team_players = []
                positions = []
                real_teams = []
                for sel in selected_players:
                    name = sel.split(" ")[0]
                    player = next(p for p in PLAYERS if p["name"] == name)
                    team_players.append(player['name'])
                    positions.append(player['position'])
                    real_teams.append(player['realTeam'])
                
                # SAVE TO PUBLIC SHEET
                worksheet.append_row([
                    team_name.strip(),
                    total_price,
                    ", ".join(team_players),
                    ", ".join(positions),
                    ", ".join(real_teams),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    owner_name.strip()
                ])
                
                st.success(f"🎉 **'{team_name}' ADDED TO PUBLIC LEAGUE!**")
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"❌ **Save failed:** {str(e)}")

# LIVE LEAGUE TABLE
st.markdown("---")
st.subheader("🏆 **LIVE LEAGUE - All City Teams**")

try:
    worksheet = connect_sheets()
    df = pd.DataFrame(worksheet.get_all_records())
    if not df.empty:
        st.dataframe(df.tail(50), use_container_width=True)  # Last 50 teams
    else:
        st.info("👆 **Be the first to save your team!**")
except:
    st.info("**Loading league...**")

st.markdown("---")
st.caption("🎮 **EF Cup Fantasy League** - Share app link with everyone!")
