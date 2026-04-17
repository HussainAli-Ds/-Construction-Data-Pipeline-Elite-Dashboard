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

st.set_page_config(layout="wide")

# ---------------- FORMAT FUNCTION ----------------
def format_numbers(df):
    num_cols = df.select_dtypes(include="number").columns
    return df.style.format({col: "{:,.0f}" for col in num_cols})

# ---------------- DB ----------------
@st.cache_data
def load_data(table):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"DB Error: {e}")
        return pd.DataFrame()

data = {name: load_data(tbl) for name, tbl in TABLES.items()}

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>🚀 Elite Executive Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>مین ڈیش بورڈ</h3>", unsafe_allow_html=True)

# ---------------- MAIN KPIs ----------------
lab = data["👷 Labour"]
mac = data["🚜 Machines"]
mat = data["📦 Material"]
mnt = data["🛠 Maintenance"]

total_lab = lab["labour_id"].nunique() if not lab.empty else 0
total_mac = mac["machine_id"].nunique() if not mac.empty else 0

total_cost = sum([
    df["total_cost"].sum() for df in [lab, mat, mnt] if "total_cost" in df.columns
])

c1, c2 = st.columns(2)
c1.metric("👷 Total Labours (کل مزدور)", total_lab)
c2.metric("🚜 Total Machines (کل مشینیں)", total_mac)

st.metric("💰 Total Cost PKR (کل لاگت)", f"{int(total_cost):,}")

st.divider()

# ---------------- QUICK SUMMARY ----------------
summary_main = pd.DataFrame({
    "Field": ["Labour","Machine","Maintenance","Material"],
    "Total Records": [len(lab), len(mac), len(mnt), len(mat)],
    "Total Cost": [
        lab.get("total_cost", pd.Series()).sum(),
        0,
        mnt.get("total_cost", pd.Series()).sum(),
        mat.get("total_cost", pd.Series()).sum()
    ]
})

st.subheader("📊 Quick Summary (فوری خلاصہ)")
st.dataframe(format_numbers(summary_main), use_container_width=True)

fig_main = px.bar(summary_main, x="Field", y="Total Cost")
st.plotly_chart(fig_main, use_container_width=True, key="main_chart")

st.divider()

# ---------------- TABS ----------------
tabs = st.tabs(list(TABLES.keys()))

for i, name in enumerate(TABLES.keys()):
    with tabs[i]:
        df = data[name]

        if df.empty:
            st.warning("No Data")
            continue

        st.subheader(name)

        # ---------- FILTER ----------
        col1, col2, col3 = st.columns(3)

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

            start = col1.date_input("Start Date", df["date"].min(), key=f"start_{name}")
            end = col2.date_input("End Date", df["date"].max(), key=f"end_{name}")

            df = df[(df["date"] >= pd.to_datetime(start)) & (df["date"] <= pd.to_datetime(end))]

        if name == "📦 Material":
            val = col3.multiselect("Material", df["material"].unique(), key=f"mat_{name}")
            if val:
                df = df[df["material"].isin(val)]

        elif name == "👷 Labour":
            val = col3.multiselect("Labour", df["labour_name"].unique(), key=f"lab_{name}")
            if val:
                df = df[df["labour_name"].isin(val)]

        elif name == "🚜 Machines":
            val = col3.multiselect("Machine", df["machine_id"].unique(), key=f"mac_{name}")
            if val:
                df = df[df["machine_id"].isin(val)]

        elif name == "🛠 Maintenance":
            val = col3.multiselect("Machine", df["machine_id"].unique(), key=f"mnt_{name}")
            if val:
                df = df[df["machine_id"].isin(val)]

        st.divider()

        # ---------- METRICS ----------
        c1, c2, c3 = st.columns(3)

        if name == "📦 Material":
            c1.metric("Materials", df["material"].nunique())
            c2.metric("Total Cost", f"{df['total_cost'].sum():,.0f}")
            c3.metric("Total Tons", f"{df['tons'].sum():,.1f}")

            summary = df.groupby("material").agg({"tons":"sum","total_cost":"sum"}).reset_index()

        elif name == "👷 Labour":
            c1.metric("Labours", df["labour_id"].nunique())
            c2.metric("Total Cost", f"{df['total_cost'].sum():,.0f}")
            c3.metric("Working Days", df["working_days"].sum())

            summary = df.groupby("labour_name").agg({
                "working_days":"sum",
                "labour_rating":"mean",
                "total_cost":"sum",
                "labour_number":"first"
            }).reset_index()

        elif name == "🚜 Machines":
            c1.metric("Machines", df["machine_id"].nunique())
            c2.metric("Working Time", df["working_time"].sum())
            c3.metric("Idle Time", df["idle_time"].sum())

            summary = df.groupby(["machine_id","machine_name"]).agg({
                "working_time":"sum",
                "idle_time":"sum",
                "fuel_cost":"sum"
            }).reset_index()

        elif name == "🛠 Maintenance":
            c1.metric("Machines", df["machine_id"].nunique())
            c2.metric("Total Cost", f"{df['total_cost'].sum():,.0f}")
            c3.metric("Repairs", df["machine_fault"].count())

            summary = df.groupby("machine_id").agg({
                "total_cost":"sum",
                "repair_cost":"sum",
                "maintenance_cost":"sum"
            }).reset_index()

        summary = summary.sort_values(summary.columns[-1], ascending=False)
        summary["rank"] = range(1, len(summary)+1)

        st.subheader("📊 Summary")
        st.dataframe(format_numbers(summary), use_container_width=True)

        # ---------- TREND ----------
        if "date" in df.columns and "total_cost" in df.columns:
            daily = df.groupby("date")["total_cost"].sum().reset_index()
            daily["Moving Avg"] = daily["total_cost"].rolling(3).mean()

            fig = px.line(daily, x="date", y=["total_cost","Moving Avg"])
            st.plotly_chart(fig, use_container_width=True, key=f"trend_{name}")

        # ---------- TOP / BOTTOM ----------
        st.subheader("🏆 Top vs Bottom")

        mid = len(summary)//2
        col1, col2 = st.columns(2)
        col1.dataframe(format_numbers(summary.head(mid)), use_container_width=True)
        col2.dataframe(format_numbers(summary.tail(mid)), use_container_width=True)

        # ---------- BAR ----------
        st.subheader("📊 Comparison")

        num_col = summary.select_dtypes(include="number").columns[-1]
        fig = px.bar(summary.head(10), x=summary.columns[1], y=num_col)
        st.plotly_chart(fig, use_container_width=True, key=f"bar_{name}")

        # ---------- ALERTS ----------
        st.subheader("🚨 Smart Alerts & Insights")

        try:
            if "idle_time" in df.columns:
                idle = df["idle_time"].sum()
                working = df["working_time"].sum() + 1
                ratio = idle / working

                if ratio > 0.5:
                    st.error(f"""
                            🚨 **High Machine Idle Time Detected**

                            - Idle Time is **{ratio:.2%}** of working time  
                            - Machines are staying unused for long periods  

                            👉 **Problem:** Wasted resources & reduced efficiency  
                            👉 **Solution:** Improve scheduling or reallocate machines  
                            """)
                else:
                    st.success("✅ Machines are being used efficiently")

            if "labour_rating" in df.columns:
                avg = df["labour_rating"].mean()

                if avg < 3:
                    st.error(f"""
                            🚨 **Low Labour Performance**

                                - Average Rating: {avg:.2f}/5  

                                👉 **Problem:** Workers performance is below expected  
                                👉 **Solution:** Provide training or review workforce  
                                """)
                else:
                    st.success("✅ Labour performance is good")

        except:
            pass

        # ---------- RAW ----------
        st.subheader("📄 Raw Data")
        st.dataframe(format_numbers(df), use_container_width=True)

# ---------------- GUIDE ----------------
st.markdown("---")
st.markdown("## 📘 Complete Dashboard Guide (مکمل رہنمائی)")

st.markdown("""
### 🔹 English (Detailed Guide)

This dashboard helps you monitor your construction project:

**1. Main Dashboard**
- Shows total labour, machines, and cost
- Gives quick overall business health

**2. Tabs**
- Each tab represents a dataset:
  - Material → what you used
  - Labour → workforce performance
  - Machines → usage efficiency
  - Maintenance → repair costs

**3. Filters**
- Select date range to analyze specific time
- Use dropdowns to focus on specific items

**4. Charts**
- Line chart → shows trends over time
- Bar chart → compares top performers

**5. Alerts**
- Red alert = problem detected  
- Green alert = everything is fine  
- Alerts explain:
  - What is wrong  
  - Why it matters  
  - How to fix it  

---

### 🔹 اردو (تفصیلی رہنمائی)

یہ ڈیش بورڈ آپ کے پروجیکٹ کو مانیٹر کرنے میں مدد دیتا ہے:

**1. مین ڈیش بورڈ**
- کل مزدور، مشینیں اور لاگت دکھاتا ہے

**2. ٹیبز**
- ہر ٹیب ایک ڈیٹا سیٹ ہے:
  - مواد
  - مزدور
  - مشینیں
  - مرمت

**3. فلٹرز**
- تاریخ منتخب کریں
- مخصوص چیزیں دیکھیں

**4. چارٹس**
- لائن چارٹ → وقت کے ساتھ تبدیلی
- بار چارٹ → موازنہ

**5. الرٹس**
- سرخ = مسئلہ  
- سبز = سب ٹھیک  
- ہر الرٹ بتاتا ہے:
  - مسئلہ کیا ہے  
  - کیوں اہم ہے  
  - کیسے حل کریں  
""")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("""
**Created by Hussain-Ali**  
📧 ha780383@gmail.com  
📞 03357897412 | 03318782469  
""")