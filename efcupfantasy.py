import streamlit as st
import gspread
from google.oauth2 import service_account
import pandas as pd
from datetime import datetime
import hashlib

# Google Sheets setup
@st.cache_resource
def get_sheet():
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["connections"]["google_sheets"],
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )
    client = gspread.authorize(creds)
    
    try:
        sheet = client.open("efcupfantasy")
        try:
            worksheet = sheet.worksheet("Teams")
        except gspread.exceptions.WorksheetNotFound:
            # AUTO-CREATE Teams tab if missing
            worksheet = sheet.add_worksheet("Teams", 1000, 7)
            worksheet.append_row([
                "Team", "Owner", "Players", "Captain", "Time", "Points", "Owner_Email"
            ])
            st.success("✅ Created 'Teams' worksheet automatically!")
        return worksheet
    except gspread.exceptions.SpreadsheetNotFound:
        # CREATE entire spreadsheet if missing
        sheet = client.create("efcupfantasy")
        worksheet = sheet.add_worksheet("Teams", 1000, 7)
        worksheet.append_row([
            "Team", "Owner", "Players", "Captain", "Time", "Points", "Owner_Email"
        ])
        st.success("✅ Created 'efcupfantasy' spreadsheet + Teams tab!")
        return worksheet

@st.cache_resource
def get_scores_sheet():
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["connections"]["google_sheets"],
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    client = gspread.authorize(creds)
    
    try:
        sheet = client.open("efcupfantasy")
        try:
            worksheet = sheet.worksheet("Scores")
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sheet.add_worksheet("Scores", 1000, 3)
            worksheet.append_row(["Player Name", "Points", "Notes"])
            st.success("✅ Created 'Scores' worksheet!")
        return worksheet
    except:
        return None
# SIMPLE TEAM LOGIN SYSTEM
def hash_team_name(team_name):
    return hashlib.md5(team_name.encode()).hexdigest()

# Main app
st.set_page_config(page_title="EF Cup Fantasy", layout="wide")

# Initialize session state
if 'logged_in_team' not in st.session_state:
    st.session_state.logged_in_team = None
if 'teams_data' not in st.session_state:
    st.session_state.teams_data = []


BUDGET = 60

# TABS
tab1, tab2, tab3, tab4 = st.tabs(["🔐 Login", "📝 Build Team", "👑 My Team", "⚽ Admin Scores"])

# TAB 1: COMPLETE FIXED LOGIN (No NameError!)
with tab1:
    st.markdown("### 🔐 **SELECT YOUR REGISTERED TEAM**")
    
    # Get teams data ONCE at top
    try:
        teams_worksheet = get_sheet()
        all_teams_data = teams_worksheet.get_all_records()
        registered_teams = [team.get('Team', '').strip() for team in all_teams_data if team.get('Team')]
    except:
        registered_teams = []
        all_teams_data = []
    
    if st.session_state.get('logged_in_team'):
        # SHOW LOGGED IN TEAM (user_team defined HERE)
        current_team = st.session_state.logged_in_team
        st.success(f"✅ **Logged in: {current_team}**")
        
        # Find team data SAFELY
        user_team = None
        for team in all_teams_data:
            if team.get('Team', '').strip() == current_team:
                user_team = team
                break
        
        if user_team:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**👤 Owner:** {user_team.get('Owner', 'N/A')}")
                st.markdown(f"**⏰ Created:** {user_team.get('Time', 'N/A')}")
                st.markdown(f"**🏆 Points:** {user_team.get('Points', '0')}")
            
            with col2:
                st.markdown("**📋 YOUR PLAYERS:**")
                players_str = user_team.get('Players', '')
                if players_str:
                    players = [p.strip() for p in players_str.split(',')]
                    for player in players:
                        st.write(f"• **{player}**")
                else:
                    st.write("No players yet")
            
            if st.button("🚪 **LOGOUT**", type="secondary"):
                st.session_state.logged_in_team = None
                st.rerun()
        else:
            st.error("❌ Team data missing!")
            
    else:
        # LOGIN FORM - No user_team here
        if registered_teams:
            selected_team = st.selectbox(
                "Choose your team:",
                options=registered_teams,
                index=None,
                placeholder="Select team..."
            )
            
            if selected_team and st.button("✅ **LOGIN**", type="primary"):
                st.session_state.logged_in_team = selected_team
                st.success(f"✅ **Welcome {selected_team}!**")
                st.rerun()
                
            # Preview selected team
            if selected_team:
                preview_team = next((t for t in all_teams_data if t.get('Team', '') == selected_team), None)
                if preview_team:
                    st.info(f"👤 Owner: {preview_team.get('Owner', 'N/A')} | 📊 {len(preview_team.get('Players', '').split(','))} players")
        else:
            st.info("**No teams yet! Create one in Build Team tab.**")



            # COMPLETE 36 PLAYERS LIST
            PLAYERS = [
    {"id": 1, "name": "ROJIT SHRESTHA", "price": 13, "position": "GK", "realTeam": "JOSHI JAGUARS",},
    {"id": 2, "name": "SUJAN BK", "price": 15, "position": "GK", "realTeam": "SOTI SOLDIERS"},
    {"id": 3, "name": "PRASHANNA PAUDEL", "price": 15, "position": "GK", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 4, "name": "TANISHK THAPA", "price": 11, "position": "GK", "realTeam": "ZENITH ZEBRAS"},
    {"id": 5, "name": "AAYUSH ROKA", "price": 14, "position": "GK", "realTeam": "BENZE BULLS"},
    {"id": 6, "name": "SANGAM SHRESTHA", "price": 10, "position": "GK", "realTeam": "GODAR GOATS"},
    {"id": 7, "name": "SABIN DAHAL", "price": 5, "position": "FWD", "realTeam": "BENZE BULLS"},
    {"id": 8, "name": "SACHIN SEN", "price": 17, "position": "FWD", "realTeam": "ZENITH ZEBRAS"},
    {"id": 9, "name": "SAKAR SUBEDI", "price": 7, "position": "FWD", "realTeam": "BENZE BULLS"},
    {"id": 10, "name": "SANDIL KATUWAL", "price": 4, "position": "FWD", "realTeam": "GODAR GOATS"},
    {"id": 11, "name": "SANJAYA ADHIKARI", "price": 4, "position": "FWD", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 12, "name": "SANKALPA SHARMA", "price": 11, "position": "FWD", "realTeam": "JOSHI JAGUARS"},
    {"id": 13, "name": "SHRIJAN BHUSAL", "price": 15, "position": "FWD", "realTeam": "ZENITH ZEBRAS"},
    {"id": 14, "name": "SHUBHAM SINGH", "price": 12, "position": "FWD", "realTeam": "GODAR GOATS"},
    {"id": 15, "name": "SHUSHANT ADHIKARI", "price": 11, "position": "FWD", "realTeam": "JOSHI JAGUARS"},
    {"id": 16, "name": "SHYAM MAHATO", "price": 8, "position": "FWD", "realTeam": "GODAR GOATS"},
    {"id": 17, "name": "SUDIP BARAL", "price": 18, "position": "FWD", "realTeam": "BENZE BULLS"},
    {"id": 18, "name": "SUJIT GURUNG", "price": 10, "position": "FWD", "realTeam": "ZENITH ZEBRAS"},
    {"id": 19, "name": "SUMAN CHHETRI", "price": 15, "position": "FWD", "realTeam": "SOTI SOLDIERS"},
    {"id": 20, "name": "UNIQUE REGMI", "price": 6, "position": "FWD", "realTeam": "SOTI SOLDIERS"},
    {"id": 21, "name": "SUMAN SHARMA", "price": 5, "position": "FWD", "realTeam": "SOTI SOLDIERS"},
    {"id": 22, "name": "UDHAY THAKUR", "price": 9, "position": "FWD", "realTeam": "GODAR GOATS"},
    {"id": 23, "name": "SAJAN ROKAYA", "price": 4, "position": "DEF", "realTeam": "ZENITH ZEBRAS"},
    {"id": 24, "name": "SAMEER ACHARYA", "price": 18, "position": "DEF", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 25, "name": "SAMIR GODAR", "price": 18, "position": "DEF", "realTeam": "GODAR GOATS"},
    {"id": 26, "name": "SANTOSH JOSHI", "price": 18, "position": "DEF", "realTeam": "JOSHI JAGUARS"},
    {"id": 27, "name": "SUJAL PARAJULI", "price": 17, "position": "DEF", "realTeam": "JOSHI JAGUARS"},
    {"id": 28, "name": "SUJAL SOTI", "price": 18, "position": "DEF", "realTeam": "SOTI SOLDIERS"},
    {"id": 29, "name": "SUJAN BHAATTA", "price": 10, "position": "DEF", "realTeam": "SOTI SOLDIERS"},
    {"id": 30, "name": "SUSHAN PANDEY", "price": 7, "position": "DEF", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 31, "name": "SWORNIM TIMILSINA", "price": 13, "position": "DEF", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 32, "name": "VIVEK GAUTAM", "price": 12, "position": "DEF", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 33, "name": "ZENITH SARU", "price": 18, "position": "DEF", "realTeam": "ZENITH ZEBRAS"},
    {"id": 34, "name": "ANUJ THAPA", "price": 15, "position": "DEF", "realTeam": "BENZE BULLS"},
    {"id": 35, "name": "ANUPAM BISTA", "price": 7, "position": "FWD", "realTeam": "BENZE BULLS"},
    {"id": 36, "name": "TASHI SHERPA", "price": 10, "position": "FWD", "realTeam": "BENZE BULLS"},
            ]
            # TAB 2: BUILD TEAM (Only if not logged in or for new teams)
# TAB 2: BUILD TEAM WITH PRICE FILTERS
with tab2:
    st.markdown("### 🏗️ **BUILD TEAM**")
    if st.session_state.logged_in_team:
        st.info("✅ Logged in! Use 'My Team' tab.")
    else:
        team_name = st.text_input("Team Name:")
        owner_name = st.text_input("Owner Name:")
        
        if team_name and owner_name:
            # PRICE FILTERS
            col1, col2 = st.columns(2)
            with col1:
                max_price = st.slider("Max Price per player:", 8, 15, 15)
            with col2:
                remaining_budget = st.slider("Remaining Budget:", 0, BUDGET, BUDGET)
            
            # FILTER PLAYERS BY PRICE
            filtered_players = [p for p in PLAYERS if int(p['price'][1:]) <= max_price]
            
            col1, col2, col3 = st.columns(3)
            selected_gk = []
            selected_def_fwd = []
            
            with col1:
                st.write(f"**🧤 GK (≤₹{max_price})**")
                for p in [x for x in filtered_players if x["position"] == "GK"]:
                    if st.checkbox(f"{p['name']} {p['price']}", key=f"gk_{p['name']}"):
                        selected_gk.append(f"{p['name']} {p['price']}")
            
            with col2:
                st.write(f"**🛡️ DEF (≤₹{max_price})**")
                for p in [x for x in filtered_players if x["position"] == "DEF"]:
                    if st.checkbox(f"{p['name']} {p['price']}", key=f"def_{p['name']}"):
                        selected_def_fwd.append(f"{p['name']} {p['price']}")
            
            with col3:
                st.write(f"**⚽ FWD (≤₹{max_price})**")
                for p in [x for x in filtered_players if x["position"] == "FWD"]:
                    if st.checkbox(f"{p['name']} {p['price']}", key=f"fwd_{p['name']}"):
                        selected_def_fwd.append(f"{p['name']} {p['price']}")
            
            # REAL-TIME BUDGET CHECK
            all_selected = selected_gk + selected_def_fwd
            total_price = sum(int(p.split("₹")[1]) for p in all_selected if "₹" in p)
            budget_left = BUDGET - total_price
            
            col4, col5 = st.columns(2)
            col5.metric("💰 Budget Used", f"₹{total_price}", f"₹{budget_left}")
            
            # GREEN/RED BUDGET STATUS
            budget_color = "normal" if budget_left >= 0 else "inverse"
            st.markdown(f"**Budget Left: ₹{budget_left}**")
            
            # PERFECT VALIDATION
            is_valid = (len(selected_gk) == 1 and 
                       len(selected_def_fwd) == 5 and 
                       total_price <= BUDGET)
            
            if total_price > BUDGET:
                st.error(f"❌ **OVER BUDGET!** ₹{total_price} > ₹{BUDGET}")
            elif len(selected_gk) != 1:
                st.error("❌ **Select exactly 1 GK**")
            elif len(selected_def_fwd) != 5:
                st.warning(f"❌ **Select exactly 5 DEF/FWD** (have {len(selected_def_fwd)})")
            else:
                st.success("✅ **VALID TEAM! Ready to save!**")
            
            if st.button("💾 **SAVE TEAM**", type="primary", disabled=not is_valid):
                worksheet = get_sheet()
                players_str = ", ".join(all_selected)
                worksheet.append_row([team_name, owner_name, players_str, "", 
                                    datetime.now().strftime("%Y-%m-%d %H:%M"), 0, ""])
                st.success(f"✅ **{team_name} SAVED!** Budget: ₹{total_price}")
                st.rerun()


# TAB 3: MY TEAM & SCORE (Logged in only)
with tab3:
    st.markdown("### 👑 **YOUR TEAM & LIVE SCORE**")
    
    if st.session_state.logged_in_team:
        teams_worksheet = get_sheet()
        scores_worksheet = get_scores_sheet()
        
        # Get user's team data
        user_team = None
        for team in teams_worksheet.get_all_records():
            if team.get('Team', '') == st.session_state.logged_in_team:
                user_team = team
                break
        
        if user_team:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📋 YOUR PLAYERS**")
                players = user_team.get('Players', '').split(', ')
                for player in players:
                    st.write(f"• {player.strip()}")
                
                captain = user_team.get('Captain', 'None')
                st.markdown(f"**👑 Captain:** {captain}")
            
            with col2:
                # LIVE SCORE CALCULATION
                scores_data = scores_worksheet.get_all_records()
                points_dict = {s['Player Name']: int(s['Points']) for s in scores_data}
                
                team_total = 0
                players = user_team.get('Players', '').split(', ')
                captain = user_team.get('Captain', '').strip()
                
                st.markdown("**⚽ LIVE POINTS**")
                for player in players:
                    player_name = player.strip()
                    pts = points_dict.get(player_name, 0)
                    multiplier = " **(2x)**" if player_name == captain else ""
                    st.write(f"• {player_name}: **{pts}{multiplier}** pts")
                    if player_name == captain:
                        team_total += pts * 2
                    else:
                        team_total += pts
                
                st.markdown("---")
                st.metric("🏆 **TOTAL POINTS**", f"{team_total}", delta=None)
                
                # Update sheet with live score
                if st.button("🔄 Update My Score", type="secondary"):
                    row_num = teams_worksheet.findall(st.session_state.logged_in_team)[0].row
                    teams_worksheet.update_cell(row_num, 6, team_total)  # Points column
                    st.success("✅ Score updated!")
        else:
            st.warning("No team found!")
    else:
        st.info("🔐 Login to view your team!")

# TAB 4: ADMIN SCORES (Separate admin access)
with tab4:
    st.markdown("### ⚽ **ADMIN: ENTER MATCH SCORES**")
    admin_code = st.text_input("Admin Code:", type="password")
    
    if admin_code == "efcup2025":  # Change this password
        player_names = [p['name'] for p in PLAYERS]
        selected_player = st.selectbox("Select Player:", player_names)
        
        col1, col2 = st.columns(2)
        points = col1.number_input("Points:", min_value=-5, max_value=50, value=0)
        notes = col2.text_input("Notes:")
        
        if st.button("➕ ADD SCORE", type="primary"):
            scores_worksheet = get_scores_sheet()
            scores_worksheet.append_row([selected_player, points, notes])
            st.success(f"✅ {selected_player}: {points}pts ADDED!")
            st.rerun()
        
        # View all scores
        if st.button("📊 View All Scores"):
            scores_data = scores_worksheet.get_all_records()
            st.dataframe(pd.DataFrame(scores_data))
