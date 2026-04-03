import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import os
from dotenv import load_dotenv

# ---------------- LOAD ENV ----------------
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
}

TABLES = {
    "📦 Material": "material_data",
    "👷 Labour": "labours_data",
    "🚜 Machines": "machines_data",
    "🛠 Maintenance": "machines_maintenance",
    "📈 Progress": "progress_data",
    "🏗 Sites": "site_data"
}

st.set_page_config(page_title="Elite Dashboard", layout="wide")

# ---------------- DB ----------------
@st.cache_data
def load_data(table):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ DB Error: {e}")
        return pd.DataFrame()

data = {name: load_data(tbl) for name, tbl in TABLES.items()}

# ---------------- HEADER ----------------
st.title("🚀 Elite Construction Dashboard")

# ---------------- FILTERS ----------------
col1, col2 = st.columns(2)

all_sites = []
for df in data.values():
    if "working_site" in df.columns:
        all_sites.extend(df["working_site"].dropna().unique())

all_sites = list(set(all_sites))

with col1:
    selected_site = st.selectbox("🏗 Select Site", ["All"] + all_sites)

with col2:
    selected_date = st.selectbox("📅 Date Filter", ["All", "Today"])

def apply_filters(df):
    if df.empty:
        return df

    if selected_site != "All" and "working_site" in df.columns:
        df = df[df["working_site"] == selected_site]

    if selected_date == "Today" and "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
        df = df[df["date"] == pd.Timestamp.today().date()]

    return df

for key in data:
    data[key] = apply_filters(data[key])

# ---------------- OVERVIEW ----------------
total_labours = len(data["👷 Labour"])
total_machines = len(data["🚜 Machines"])

total_cost = 0
for k in ["📦 Material", "👷 Labour", "🛠 Maintenance"]:
    if "total_cost" in data[k].columns:
        total_cost += data[k]["total_cost"].sum()

c1, c2, c3 = st.columns(3)
c1.metric("👷 Total Labour", total_labours)
c2.metric("🚜 Total Machines", total_machines)
c3.metric("💰 Total Cost", f"{int(total_cost):,}")

st.divider()

# ---------------- TABS ----------------
tabs = st.tabs(list(TABLES.keys()))

for i, tab_name in enumerate(TABLES.keys()):
    with tabs[i]:
        df = data[tab_name]

        st.subheader(tab_name)

        if df.empty:
            st.warning("No data available")
            continue

        c1, c2, c3 = st.columns(3)

        # ---------------- METRICS ----------------
        if tab_name == "📦 Material":
            c1.metric("Materials", df["material"].nunique())
            c2.metric("Total Cost", f"{df['total_cost'].sum():,.0f}")
            c3.metric("Total Tons", f"{df['tons'].sum():,.1f}")

        elif tab_name == "👷 Labour":
            c1.metric("Labours", df["labour_id"].nunique())
            c2.metric("Total Cost", f"{df['total_cost'].sum():,.0f}")
            c3.metric("Working Days", df["working_days"].sum())

        elif tab_name == "🚜 Machines":
            c1.metric("Machines", df["machine_id"].nunique())
            c2.metric("Working Time", df["working_time"].sum())
            c3.metric("Idle Time", df["idle_time"].sum())

        elif tab_name == "🛠 Maintenance":
            c1.metric("Machines", df["machine_id"].nunique())
            c2.metric("Total Cost", f"{df['total_cost'].sum():,.0f}")
            c3.metric("Repairs", df["machine_fault"].count())

        elif tab_name == "📈 Progress":
            c1.metric("Entries", len(df))
            c2.metric("Avg Progress", f"{df['progress_percentage'].mean():.1f}%")
            c3.metric("Max Progress", f"{df['progress_percentage'].max()}%")

        st.divider()

        # ---------------- TOP DATA ----------------
        st.subheader("🏆 Top Data")

        if tab_name == "📦 Material":
            top = df.groupby("material")["tons"].sum().nlargest(10).reset_index()
            st.dataframe(top)

        elif tab_name == "👷 Labour":
            top = df.sort_values("labour_rating", ascending=False).head(10)
            st.dataframe(top[["labour_name", "labour_rating", "labour_number"]])

        elif tab_name == "🚜 Machines":
            top = df.sort_values("working_time", ascending=False).head(10)
            st.dataframe(top[["machine_id", "working_time"]])

        elif tab_name == "🛠 Maintenance":
            top = df.groupby("machine_id")["total_cost"].sum().nlargest(10).reset_index()
            st.dataframe(top)

        st.divider()

        # ---------------- CHARTS ----------------
        st.subheader("📊 Charts")

        numeric_cols = df.select_dtypes(include="number").columns

        for col in numeric_cols[:2]:
            fig = px.bar(df, y=col, title=col)
            st.plotly_chart(fig, use_container_width=True)

        # ---------------- ADVANCED INSIGHTS ----------------
        st.subheader("🧠 Detailed Insights")

        try:
            insights = []

            if tab_name == "📦 Material":
                total_tons = df["tons"].sum()
                total_cost_mat = df["total_cost"].sum()

                top_mat = df.groupby("material")["tons"].sum().idxmax()
                bottom_mat = df.groupby("material")["tons"].sum().idxmin()

                insights.append(f"🔝 Top material: {top_mat}")
                insights.append(f"📉 Lowest usage material: {bottom_mat}")
                insights.append(f"💰 Total cost: {total_cost_mat:,.0f}")
                insights.append(f"⚖️ Cost per ton: {(total_cost_mat/(total_tons+1)):.2f}")

            elif tab_name == "👷 Labour":
                best = df.sort_values("labour_rating", ascending=False).iloc[0]
                worst = df.sort_values("labour_rating").iloc[0]

                insights.append(f"⭐ Best worker: {best['labour_name']}")
                insights.append(f"⚠️ Lowest performer: {worst['labour_name']}")
                insights.append(f"💰 Total labour cost: {df['total_cost'].sum():,.0f}")

            elif tab_name == "🚜 Machines":
                most_used = df.sort_values("working_time", ascending=False).iloc[0]
                least_used = df.sort_values("working_time").iloc[0]

                idle_ratio = df["idle_time"].sum()/(df["working_time"].sum()+1)

                insights.append(f"🚜 Most used machine: {most_used['machine_id']}")
                insights.append(f"📉 Least used machine: {least_used['machine_id']}")
                insights.append(f"📊 Idle ratio: {idle_ratio:.2%}")

            elif tab_name == "🛠 Maintenance":
                most_expensive = df.groupby("machine_id")["total_cost"].sum().idxmax()

                insights.append(f"💸 Most expensive machine: {most_expensive}")
                insights.append(f"💰 Total maintenance cost: {df['total_cost'].sum():,.0f}")

            elif tab_name == "📈 Progress":
                avg = df["progress_percentage"].mean()

                insights.append(f"📊 Average progress: {avg:.1f}%")

                if avg < 50:
                    insights.append("⚠️ Project behind schedule")
                else:
                    insights.append("✅ Project progressing well")

            for ins in insights:
                st.write(f"• {ins}")

        except Exception as e:
            st.warning(f"Insight error: {e}")

        # ---------------- RAW ----------------
        st.subheader("📄 Raw Data")
        st.dataframe(df, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("""
**Created by Hussain-Ali**  
📧 ha780383@gmail.com  
📞 03357897412 | 03318782469  
""")