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

# Desired currency order
currency_order = ["USD", "EUR", "GBP", "JPY", "CHF", "AUD", "NZD", "CAD",
                  "SEK", "PLN", "HUF", "DKK", "CZK", "NOK", "ZAR", "BRL"]

# Filter to only currencies present in dataset
available_currencies = [c for c in currency_order if c in df["Currency"].dropna().unique()]

# Reduce button spacing with custom CSS
st.markdown("""
    <style>
    .css-1aumxhk, .stButton button {
        margin: 2px !important;
        padding: 4px 8px !important;
    }
    .stButton button {
        font-size: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Create buttons for each currency
cols = st.columns(len(available_currencies))
selected_currency = None

for i, currency in enumerate(available_currencies):
    if cols[i].button(currency):
        selected_currency = currency

# Set default on first run
if "selected_currency" not in st.session_state:
    st.session_state.selected_currency = available_currencies[0]

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
        "right": "dayGridMonth,timeGridWeek"
    }
}

calendar(events=calendar_events, options=calendar_options)

