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

# Currency buttons
cols = st.columns(len(currencies))
selected_currency = None

for i, currency in enumerate(currencies):
    if cols[i].button(currency):
        selected_currency = currency

# Maintain selected currency
if "selected_currency" not in st.session_state:
    st.session_state.selected_currency = currencies[0]

if selected_currency:
    st.session_state.selected_currency = selected_currency

st.subheader(f"Showing events for: {st.session_state.selected_currency}")

# View mode toggle
view_mode = st.radio("View Mode", ["Month View", "Day View", "Year Grid View"], horizontal=True)

# Year selector for Year Grid View
if view_mode == "Year Grid View":
    selected_year = st.selectbox("Select Year", [2025, 2026, 2027], index=0)
else:
    selected_year = pd.Timestamp.today().year

# Filter events for selected currency and year
filtered_df = df[(df["Currency"] == st.session_state.selected_currency) & 
                 (df["Date"].dt.year == selected_year)]

# Prepare calendar events
calendar_events = [
    {
        "title": row["Event"],
        "start": row["Date"].strftime("%Y-%m-%d"),
        "allDay": True
    }
    for _, row in filtered_df.iterrows()
]

# Month & Day View Options
calendar_options_standard = {
    "initialView": "dayGridMonth" if view_mode == "Month View" else "timeGridDay",
    "editable": False,
    "height": 700,
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": ""  # Remove week/month buttons
    }
}

# Render Calendar based on view mode
if view_mode in ["Month View", "Day View"]:
    calendar(events=calendar_events, options=calendar_options_standard)

# Year Grid View
if view_mode == "Year Grid View":
    st.subheader(f"Year Overview: {selected_year}")

    # Arrange mini calendars in grid
    cols_per_row = 4
    for row_idx in range(0, 12, cols_per_row):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            month_idx = row_idx + col_idx + 1
            if month_idx > 12:
                continue

            month_events = [
                event for event in calendar_events
                if pd.to_datetime(event["start"]).month == month_idx
            ]

            with cols[col_idx]:
                st.markdown(f"### {pd.Timestamp(selected_year, month_idx, 1).strftime('%B %Y')}")
                
                mini_calendar_options = {
                    "initialView": "dayGridMonth",
                    "initialDate": f"{selected_year}-{month_idx:02d}-01",
                    "editable": False,
                    "height": 400,  # Taller to show all days without scroll
                    "headerToolbar": False,
                    "titleFormat": {"year": "numeric", "month": "short"},
                    "fixedWeekCount": False
                }

                calendar(events=month_events, options=mini_calendar_options)
