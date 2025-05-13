import os
import pandas as pd
import streamlit as st
from streamlit_calendar import calendar

# Correct relative path fix
file_path = os.path.join(os.path.dirname(__file__), "EconomicCalendar.csv")
df = pd.read_csv(file_path)
df["Date"] = pd.to_datetime(df["Date"])

st.set_page_config(page_title="Economic Calendar", layout="wide")

st.title("📅 Interactive Economic Calendar")

# Unique currencies sorted alphabetically
currencies = sorted(df["Currency"].dropna().unique())

# Create buttons for each currency in a single row of columns
cols = st.columns(len(currencies))
selected_currency = None

for i, currency in enumerate(currencies):
    if cols[i].button(currency):
        selected_currency = currency

# Set default on first run
if "selected_currency" not in st.session_state:
    st.session_state.selected_currency = currencies[0]

if selected_currency:
    st.session_state.selected_currency = selected_currency

# Filter based on selected currency
filtered_df = df[df["Currency"] == st.session_state.selected_currency]

st.subheader(f"Showing events for: {st.session_state.selected_currency}")

# Convert events to FullCalendar format
calendar_events = [
    {
        "title": row["Event"],
        "start": row["Date"].strftime("%Y-%m-%d"),
        "allDay": True
    }
    for _, row in filtered_df.iterrows()
]

calendar_options = {
    "initialView": "dayGridMonth",
    "editable": False,
    "height": 650,
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,listYear"
    },
    "views": {
        "listYear": {
            "type": "list",
            "duration": {"years": 1},
            "buttonText": "Year"
        }
    }
}

calendar(events=calendar_events, options=calendar_options)
