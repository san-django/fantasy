import streamlit as st
from datetime import datetime
import json

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

# SESSION STATE - WORKS 100% ON STREAMLIT CLOUD
if "teams" not in st.session_state:
    st.session_state.teams = []

st.title("🏆 EF CUP FANTASY")
st.markdown("**₹100 Budget • 6 Players • Save & Download**")

BUDGET = 100

# Team name input
team_name = st.text_input("🏷️ **Team Name**", placeholder="Enter your team name")

# Player selection by position
st.subheader("Select Players")
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

# Combine selections
selected_players = selected_gk + selected_fwd + selected_def

# Budget calculator
if selected_players:
    total_price = sum(int(p.split("₹")[1]) for p in selected_players)
    budget_left = BUDGET - total_price
    
    col1, col2, col3 = st.columns([1,2,1])
    col1.metric("👥 Players", len(selected_players), "6")
    col2.metric("💰 Budget", f"₹{total_price}", f"₹{budget_left}")
    col3.metric("✅ Status", "OK" if budget_left >= 0 else "OVER", "Budget")
    
    if budget_left >= 0:
        st.success(f"✅ **Budget OK!** ({len(selected_players)}/6 players)")
        st.markdown("### 📋 **Your Team**")
        for player in selected_players:
            st.write(f"• {player}")
    else:
        st.error(f"❌ **Over budget by ₹{-budget_left}!**")

# SAVE TEAM
if st.button("💾 **SAVE TEAM**", type="primary", use_container_width=True):
    if not team_name.strip():
        st.error("❌ **Enter team name first!**")
    elif len(selected_players) != 6:
        st.error(f"❌ **Need exactly 6 players!** (You have {len(selected_players)})")
    else:
        total_price = sum(int(p.split("₹")[1]) for p in selected_players)
        if total_price > BUDGET:
            st.error(f"❌ **Over budget: ₹{total_price}!**")
        else:
            # Get full player data
            team_players = []
            for sel in selected_players:
                name = sel.split(" ")[0]
                player = next((p for p in PLAYERS if p["name"] == name), None)
                if player:
                    team_players.append(player)
            
            # Save to session
            st.session_state.teams.append({
                "name": team_name.strip(),
                "players": team_players,
                "total_price": total_price,
                "saved": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            st.success(f"🎉 **'{team_name}' SAVED!** ₹{total_price}/100")
            st.balloons()
            st.rerun()

# DOWNLOAD BUTTON
if st.session_state.teams:
    st.markdown("---")
    json_data = json.dumps(st.session_state.teams, indent=2, ensure_ascii=False)
    st.download_button(
        label="💾 **DOWNLOAD ALL TEAMS** (JSON)",
        data=json_data,
        file_name=f"efcup_teams_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json",
        type="secondary",
        use_container_width=True
    )

# DISPLAY SAVED TEAMS
tab1, tab2 = st.tabs(["📱 **Recent Teams**", "📋 **All Teams**"])

with tab1:
    if not st.session_state.teams:
        st.info("👆 **Save your first team above!**")
    else:
        st.markdown(f"**Total teams saved: {len(st.session_state.teams)}**")
        for team in st.session_state.teams[-5:][::-1]:
            st.markdown(f"**{team['name']}** • ₹{team['total_price']} • {team['saved']}")

with tab2:
    if not st.session_state.teams:
        st.info("**No teams saved yet!**")
    else:
        for i, team in enumerate(st.session_state.teams):
            with st.expander(f"#{i+1} {team['name']} - ₹{team['total_price']}"):
                st.caption(f"**Saved:** {team['saved']}")
                cols = st.columns(3)
                for j, player in enumerate(team['players']):
                    with cols[j%3]:
                        st.markdown(f"""
                        **{player['name']}**  
                        _{player['position']}_ • {player['realTeam']}
                        """)

st.markdown("---")
st.caption("🎮 **EF Cup Fantasy** - Powered by Streamlit")
