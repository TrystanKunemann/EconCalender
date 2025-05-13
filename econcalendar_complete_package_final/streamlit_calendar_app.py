import os
import pandas as pd
import streamlit as st
from streamlit_calendar import calendar

# Load data
file_path = os.path.join(os.path.dirname(__file__), "EconomicCalendar.csv")
df = pd.read_csv(file_path)
df["Date"] = pd.to_datetime(df["Date"])

st.set_page_config(page_title="Yearly Economic Calendar", layout="wide")

st.title("📅 Yearly Economic Calendar (Grid View)")

# Currency filter
currencies = sorted(df["Currency"].dropna().unique())
currency = st.selectbox("Select Currency", currencies)

# Filter data
filtered_df = df[df["Currency"] == currency]

# Layout: 3 columns per row (4 rows for 12 months)
cols = st.columns(3)

month_names = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

for idx, month in enumerate(range(1, 13)):
    month_df = filtered_df[filtered_df["Date"].dt.month == month]

    calendar_events = [
        {
            "title": row["Event"],
            "start": row["Date"].strftime("%Y-%m-%d"),
            "allDay": True
        }
        for _, row in month_df.iterrows()
    ]

    calendar_options = {
        "initialView": "dayGridMonth",
        "editable": False,
        "height": 300,
        "headerToolbar": False,
        "titleFormat": {"year": "numeric", "month": "long"},
        "fixedWeekCount": False
    }

    with cols[idx % 3]:
        st.markdown(f"#### {month_names[month-1]}")
        calendar(events=calendar_events, options=calendar_options)
