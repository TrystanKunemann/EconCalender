import os
import pandas as pd
import streamlit as st
from streamlit_calendar import calendar

# Load dataset
file_path = os.path.join(os.path.dirname(__file__), "EconomicCalenderFinal.csv")
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

# Button to toggle Year Grid View
if "show_year_view" not in st.session_state:
    st.session_state.show_year_view = False

if st.button("Toggle Yearly Overview"):
    st.session_state.show_year_view = not st.session_state.show_year_view

# Year selector for Year Grid View (only when toggled)
if st.session_state.show_year_view:
    selected_year = st.selectbox("Select Year", [2025, 2026, 2027], index=0)
else:
    selected_year = pd.Timestamp.today().year

# Filter events for selected currencies (no year filtering for month view)
filtered_df = df[df["Currency"].isin(selected_currencies)]

# Prepare calendar events with currency prefix and color coding
calendar_events = [
    {
        "title": f"{row['Currency']}: {row['Event']}",
        "start": row["Date"].strftime("%Y-%m-%d"),
        "allDay": True,
        "color": currency_colors.get(row["Currency"], 'gray')
    }
    for _, row in filtered_df.iterrows()
]

# Month View Calendar Options
calendar_options_standard = {
    "initialView": "dayGridMonth",
    "editable": False,
    "height": 900,
    "contentHeight": "auto",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": ""
    },
    "dayMaxEventRows": 5,
    "fixedWeekCount": False
}

# Render Month View Calendar
calendar(events=calendar_events, options=calendar_options_standard)

# Year Grid View rendering (when toggled)
if st.session_state.show_year_view:
    st.subheader(f"Year Overview: {selected_year}")

    cols_per_row = 3
    for row_idx in range(0, 12, cols_per_row):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            month_idx = row_idx + col_idx + 1
            if month_idx > 12:
                continue

            month_events = [
                event for event in calendar_events
                if pd.to_datetime(event["start"]).month == month_idx and pd.to_datetime(event["start"]).year == selected_year
            ]

            with cols[col_idx]:
                st.markdown(f"### {pd.Timestamp(selected_year, month_idx, 1).strftime('%B %Y')}")

                mini_calendar_options = {
                    "initialView": "dayGridMonth",
                    "initialDate": f"{selected_year}-{month_idx:02d}-01",
                    "editable": False,
                    "height": 450,
                    "headerToolbar": False,
                    "titleFormat": {"year": "numeric", "month": "short"},
                    "fixedWeekCount": False,
                    "dayMaxEventRows": 3
                }

                calendar(events=month_events, options=mini_calendar_options)
