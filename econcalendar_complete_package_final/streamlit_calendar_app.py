import os
import pandas as pd
import streamlit as st
from streamlit_calendar import calendar

# Load data
file_path = os.path.join(os.path.dirname(__file__), "EconomicCalendar.csv")
df = pd.read_csv(file_path)
df["Date"] = pd.to_datetime(df["Date"])

st.set_page_config(page_title="Economic Calendar", layout="wide")

st.title("📅 Interactive Economic Calendar")

# --- Currency Buttons ---
custom_order = ['USD', 'EUR', 'GBP', 'JPY', 'CHF', 'AUD', 'NZD', 'CAD', 
                'SEK', 'PLN', 'HUF', 'DKK', 'CZK', 'NOK', 'ZAR', 'BRL']

currencies = [c for c in custom_order if c in df["Currency"].unique()]

currency_container = st.container()
with currency_container:
    cols = st.columns(len(currencies))
    selected_currency = None
    for i, currency in enumerate(currencies):
        if cols[i].button(currency):
            selected_currency = currency

if "selected_currency" not in st.session_state:
    st.session_state.selected_currency = currencies[0]

if selected_currency:
    st.session_state.selected_currency = selected_currency

# --- View Toggle ---
view_mode = st.radio("Select View Mode:", ["Monthly", "Year Grid View"], horizontal=True)

# --- Filter Data ---
filtered_df = df[df["Currency"] == st.session_state.selected_currency]

# --- Main View ---
if view_mode != "Year Grid View":
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
            "right": ""  # Remove month/week tabs
        }
    }

    calendar(events=calendar_events, options=calendar_options)

else:
    st.subheader(f"Year Grid View: {st.session_state.selected_currency}")

    # Layout: 3x4 grid for 12 months
    cols = st.columns(3)
    month_names = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]

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
            "height": 350,  # Increased to show full month without scroll
            "headerToolbar": False,  # Remove header toolbar
            "titleFormat": {"year": "numeric", "month": "short"},
            "fixedWeekCount": False
        }

        with cols[idx % 3]:
            st.markdown(f"##### {month_names[month-1]}")
            calendar(events=calendar_events, options=calendar_options)

