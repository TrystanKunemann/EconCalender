import os
import pandas as pd
import streamlit as st
from streamlit_calendar import calendar

# Load dataset
file_path = os.path.join(os.path.dirname(__file__), "EconomicCalendar.csv")
df = pd.read_csv(file_path)
df["Date"] = pd.to_datetime(df["Date"])

st.set_page_config(page_title="Economic Calendar", layout="wide")

st.title("📅 Interactive Economic Calendar")

# Currencies in desired order
currencies_order = ['USD', 'EUR', 'GBP', 'JPY', 'CHF', 'AUD', 'NZD', 'CAD',
                    'SEK', 'PLN', 'HUF', 'DKK', 'CZK', 'NOK', 'ZAR', 'BRL']

currencies = [c for c in currencies_order if c in df["Currency"].unique()]

# Assign colors to currencies
currency_colors = {
    'USD': 'blue', 'EUR': 'green', 'GBP': 'red', 'JPY': 'orange', 'CHF': 'purple',
    'AUD': 'teal', 'NZD': 'brown', 'CAD': 'pink', 'SEK': 'cyan', 'PLN': 'gold',
    'HUF': 'lime', 'DKK': 'magenta', 'CZK': 'indigo', 'NOK': 'olive',
    'ZAR': 'coral', 'BRL': 'slateblue'
}

# Multi-select currencies
selected_currencies = st.multiselect(
    "Select Currencies", options=currencies, default=[currencies[0]]
)

st.subheader(f"Showing events for: {', '.join(selected_currencies)}")

# Prepare calendar events with currency prefix and color coding
filtered_df = df[df["Currency"].isin(selected_currencies)]

calendar_events = [
    {
        "title": f"{row['Currency']}: {row['Event']}",
        "start": row["Date"].strftime("%Y-%m-%d"),
        "allDay": True,
        "color": currency_colors.get(row["Currency"], 'gray')
    }
    for _, row in filtered_df.iterrows()
]

# Calendar Options for Month View
calendar_options = {
    "initialView": "dayGridMonth",
    "editable": False,
    "height": 900,
    "contentHeight": "auto",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": ""  # Removed view tabs
    },
    "dayMaxEventRows": 5,
    "fixedWeekCount": False
}

# Render Calendar (Month View always)
calendar(events=calendar_events, options=calendar_options)
