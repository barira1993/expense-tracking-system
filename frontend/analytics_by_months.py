import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import altair as alt

API_URL = "http://localhost:8000"

def analytics_months_tab():
    years = range(2022, datetime.now().year + 1)
    available_years = []

    for year in years:
        response = requests.get(f"{API_URL}/analytics/by_months/{year}")

        if response.status_code == 200 and response.json():
            available_years.append(year)

    selected_year = st.selectbox(
        "Select Year",
        available_years
    )

    response = requests.get(
        f"{API_URL}/analytics/by_months/{selected_year}"
    )

    if response.status_code == 200:
        data = response.json()

        st.subheader(f"Expense Breakdown By Months - {selected_year}")

        if not data:
            st.info(f"No expenses found for {selected_year}.")
        else:
            df = pd.DataFrame(data)
            df["month_label"] = (
                df["month"] + " " + df["year"].astype(str)
            )

            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(
                    "month_label:N",
                    title="Month",
                    sort=alt.SortField(
                        field="month_number",
                        order="ascending"
                    ),
                    axis=alt.Axis(
                        labelAngle=0
                    )
                ),
                y=alt.Y(
                    "total:Q",
                    title="Total"
                )
            ).properties(
                height=400
            )

            st.altair_chart(
                chart,
                use_container_width=True
            )

            
            df_display = df[["month", "total"]].copy()
            df_display["total"] = df_display["total"].map("{:.2f}".format)
            df_display.columns = ["Month", "Total"]
  
            st.table(df_display)

    else:
        st.error("Failed to retrieve monthly expenses.")
