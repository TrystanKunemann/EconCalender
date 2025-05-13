import os
import pandas as pd
import streamlit as st
from streamlit_calendar import calendar

# Load CSV
file_path = os.path.join(os.path.dirname(__file__), "EconomicCalendar.csv")
df = pd.read_csv(file_path)
df["Date"] = pd.to_datetime(df["Date"])

st.set_page_config(page_title="Economic Calendar", layout="wide")
st.title("📅 Interactive Economic Calendar")

# Currencies & Colors
currencies_order = ['USD', 'EUR', 'GBP', 'JPY', 'CHF', 'AUD', 'NZD', 'CAD',
                    'SEK', 'PLN', 'HUF', 'DKK', 'CZK', 'NOK', 'ZAR', 'BRL']

currency_colors = {
    'USD': 'blue', 'EUR': 'green', 'GBP': 'red', 'JPY': 'orange', 'CHF': 'purple',
    'AUD': 'teal', 'NZD': 'brown', 'CAD': 'pink', 'SEK': 'cyan', 'PLN': 'gold',
    'HUF': 'lime', 'DKK': 'magenta', 'CZK': 'indigo', 'NOK': 'olive',
    'ZAR': 'coral', 'BRL': 'slateblue'
}

currencies = [c for c in currencies_order if c in df["Currency"].unique()]

# Multi-select currencies
selected_currencies = st.multiselect(
    "Select Currencies", options=currencies, default=[currencies[0]]
)

st.subheader(f"Events for: {', '.join(selected_currencies)}")

# View toggle
view_mode = st.radio("View Mode", ["Month View", "Day View", "Year Grid View"], horizontal=True)

# Year selection (for Year Grid View)
if view_mode == "Year Grid View":
    selected_year = st.selectbox("Year", [2025, 2026, 2027], index=0)
else:
    selected_year = pd.Timestamp.today().year

# Filtered Events
filtered_df = df[df["Currency"].isin(selected_currencies) & (df["Date"].dt.year == selected_year)]

calendar_events = [
    {
        "title": f"{row['Currency']}: {row['Event']}",
        "start": row["Date"].strftime("%Y-%m-%d"),
        "allDay": True,
        "color": currency_colors.get(row["Currency"], 'gray')
    }
    for _, row in filtered_df.iterrows()
]

# FullCalendar options
calendar_height = 1300 if view_mode != "Year Grid View" else 650

calendar_options = {
    "initialView": "dayGridMonth" if view_mode == "Month View" else "timeGridDay",
    "editable": False,
    "height": calendar_height,
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": ""  # Do not use False
    },
    "eventContent": """
        function(arg) {
            return { html: '<div title="'+arg.event.title+'" style="overflow:hidden;text-overflow:ellipsis;">'+arg.event.title+'</div>' };
        }
    """,
    "dayMaxEventRows": 6,
    "fixedWeekCount": True
}

# Main Calendar Render
if view_mode != "Year Grid View":
    calendar(
        events=calendar_events,
        options=calendar_options,
        key="main_calendar"
    )

# Year Grid View Render
if view_mode == "Year Grid View":
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
                if pd.to_datetime(event["start"]).month == month_idx
            ]

            with cols[col_idx]:
                st.markdown(f"### {pd.Timestamp(selected_year, month_idx, 1).strftime('%B %Y')}")

                mini_calendar_options = {
                    "initialView": "dayGridMonth",
                    "initialDate": f"{selected_year}-{month_idx:02d}-01",
                    "editable": False,
                    "height": 700,
                    "headerToolbar": None,
                    "eventContent": """
                        function(arg) {
                            return { html: '<div title="'+arg.event.title+'" style="overflow:hidden;text-overflow:ellipsis;font-size:10px;">'+arg.event.title+'</div>' };
                        }
                    """,
                    "dayMaxEventRows": 4,
                    "fixedWeekCount": True
                }

                calendar(
                    events=month_events,
                    options=mini_calendar_options,
                    key=f"year_view_{month_idx}"
                )
