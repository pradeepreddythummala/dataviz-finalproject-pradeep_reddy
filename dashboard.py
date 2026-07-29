import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="FIFA World Cup Dashboard",
    layout="wide"
)

# ----------------------------
# Title
# ----------------------------
st.title("⚽ FIFA World Cup Match Analysis Dashboard")

st.markdown("""
This interactive dashboard analyzes FIFA World Cup matches from 1970–2022.
Use the filters on the left to explore team performance, tournaments,
stages, and match statistics.
""")

# ----------------------------
# Load Dataset
# ----------------------------
df = pd.read_csv("fifa_wc_mens_match_dataset_1970_2022.csv")

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filters")

# Team Filter
teams = ["All Teams"] + sorted(df["team_name"].dropna().unique().tolist())
selected_team = st.sidebar.selectbox("Select Team", teams)

# Tournament Filter
tournaments = ["All Tournaments"] + sorted(df["tournament_name"].dropna().unique().tolist())
selected_tournament = st.sidebar.selectbox("Select Tournament", tournaments)

# Stage Filter
stages = ["All Stages"] + sorted(df["stage_name"].dropna().unique().tolist())
selected_stage = st.sidebar.selectbox("Select Stage", stages)

# Apply Filters
filtered_df = df.copy()

if selected_team != "All Teams":
    filtered_df = filtered_df[
        filtered_df["team_name"] == selected_team
    ]

if selected_tournament != "All Tournaments":
    filtered_df = filtered_df[
        filtered_df["tournament_name"] == selected_tournament
    ]

if selected_stage != "All Stages":
    filtered_df = filtered_df[
        filtered_df["stage_name"] == selected_stage
    ]

# ----------------------------
# Dataset Preview
# ----------------------------
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head())

# ----------------------------
# Download Button
# ----------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_fifa_data.csv",
    mime="text/csv"
)

# ----------------------------
# KPI Cards
# ----------------------------
st.subheader("Project Summary")

c1, c2, c3 = st.columns(3)

c1.metric("Total Matches", len(filtered_df))
c2.metric("Teams", filtered_df["team_name"].nunique())
c3.metric("Tournaments", filtered_df["tournament_name"].nunique())

# ============================================================
# # ============================================================
# Question 1
# Top Teams by Win Percentage
# ============================================================

st.header("Question 1: Top Teams by Win Percentage")

wins = (
    filtered_df.groupby("team_name")
    .apply(lambda x: (x["result"] == "win").sum()/len(x)*100)
    .reset_index(name="Win Percentage")
)

matches = (
    filtered_df.groupby("team_name")
    .size()
    .reset_index(name="Matches")
)

wins = wins.merge(matches, on="team_name")
wins = wins[wins["Matches"] >= 10]

top10 = wins.sort_values(
    "Win Percentage",
    ascending=False
).head(10)

fig1 = px.bar(
    top10,
    x="Win Percentage",
    y="team_name",
    orientation="h",
    color="Win Percentage",
    color_continuous_scale="Viridis",
    title="Top Teams by Win Percentage"
)

st.plotly_chart(fig1, use_container_width=True)

# ============================================================
# Question 2
# Average Goals per Tournament
# ============================================================

st.header("Question 2: Average Goals by Tournament")

filtered_df["Total Goals"] = (
    filtered_df["goals_for"] +
    filtered_df["goals_against"]
)

goal_avg = (
    filtered_df.groupby("tournament_name")["Total Goals"]
    .mean()
    .reset_index()
)

fig2 = px.line(
    goal_avg,
    x="tournament_name",
    y="Total Goals",
    markers=True,
    title="Average Goals by Tournament"
)

st.plotly_chart(fig2, use_container_width=True)

# ============================================================
# Question 3
# Possession vs Goals
# ============================================================

st.header("Question 3: Possession vs Goals Scored")

possession_df = filtered_df.dropna(subset=["possession"])

fig3 = px.scatter(
    possession_df,
    x="possession",
    y="goals_for",
    color="result",
    hover_data=["team_name", "opponent_name"],
    title="Possession vs Goals Scored"
)

st.plotly_chart(fig3, use_container_width=True)

# ============================================================
# Question 4
# Goals by Stage
# ============================================================

st.header("Question 4: Goals Distribution by Stage")

fig4 = px.box(
    filtered_df,
    x="stage_name",
    y="Total Goals",
    color="stage_name",
    title="Goals Distribution by Stage"
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.header("Question 5: Top Teams by Average Shots on Target")

q5 = filtered_df.groupby("team_name", as_index=False)["shots_on_target"].mean()
q5 = q5.sort_values("shots_on_target", ascending=False).head(10)

fig5 = px.bar(q5, x="team_name", y="shots_on_target", color="shots_on_target")
st.plotly_chart(fig5, use_container_width=True)


st.markdown("---")
st.header("Question 6: Top Teams by Average Yellow Cards")

q6 = filtered_df.groupby("team_name", as_index=False)["yellow_cards"].mean()
q6 = q6.sort_values("yellow_cards", ascending=False).head(10)

fig6 = px.bar(q6, x="team_name", y="yellow_cards", color="yellow_cards")
st.plotly_chart(fig6, use_container_width=True)


st.markdown("---")
st.header("Question 7: Highest Scoring Stadiums")

q7 = filtered_df.groupby("stadium_name", as_index=False)["Total Goals"].mean()
q7 = q7.sort_values("Total Goals", ascending=False).head(10)

fig7 = px.bar(q7, x="stadium_name", y="Total Goals", color="Total Goals")
st.plotly_chart(fig7, use_container_width=True)


st.markdown("---")
st.header("Question 8: Corners vs Goals")

fig8 = px.scatter(
    filtered_df,
    x="corners",
    y="goals_for",
    color="result"
)

st.plotly_chart(fig8, use_container_width=True)


st.markdown("---")
st.header("Question 9: Average Possession by Team")

q9 = filtered_df.groupby("team_name", as_index=False)["possession"].mean()
q9 = q9.sort_values("possession", ascending=False).head(10)

fig9 = px.bar(q9, x="team_name", y="possession", color="possession")
st.plotly_chart(fig9, use_container_width=True)


st.markdown("---")
st.header("Question 10: Correlation Heatmap")

cols = [
    "goals_for",
    "goals_against",
    "possession",
    "shots",
    "shots_on_target",
    "passes_completed",
    "passes_attempted",
    "corners",
    "fouls",
    "yellow_cards",
]

corr = filtered_df[cols].corr()

fig10 = px.imshow(corr, text_auto=True)

st.plotly_chart(fig10, use_container_width=True)
