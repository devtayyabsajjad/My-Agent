# home.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_dashboard():
    st.markdown('<div class="header">Smart Farming Assistant 🚜</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Professional Dashboard Overview</div>', unsafe_allow_html=True)
    
    if st.session_state.get("summarized_data"):
        data = st.session_state["summarized_data"]
        user_data = data.get("user", {})
        api_data = data.get("api", {})
    else:
        st.info("No data available. Please go to the Best Crop Recommendation page and provide your farm details.")
        return

    economic_data = api_data.get("economic", {})
    environmental_data = api_data.get("environmental", {})

    # Display key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Avg Income", f"${economic_data.get('average_income', 0):,.2f}")
    with col2:
        st.metric("Temp", f"{environmental_data.get('temperature', 0):.1f} °C")
    with col3:
        st.metric("Rainfall", f"{environmental_data.get('rainfall', 0):.1f} mm")
    with col4:
        st.metric("Humidity", f"{environmental_data.get('humidity', 0):.1f} %")
    with col5:
        try:
            budget = float(user_data.get("budget", "0"))
        except:
            budget = 0
        st.metric("Budget", f"${budget:,.2f}")

    st.markdown('<div class="section-title">Crop Prices Overview</div>', unsafe_allow_html=True)
    crop_prices = economic_data.get("crop_prices", {})
    if crop_prices:
        df_prices = pd.DataFrame.from_dict(crop_prices, orient='index', columns=['Price']).sort_values("Price")
        st.bar_chart(df_prices)
        # Pie chart using matplotlib
        fig, ax = plt.subplots()
        ax.pie(df_prices['Price'], labels=df_prices.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.info("No crop price data available.")

    st.markdown('<div class="section-title">Monthly Temperature Variation</div>', unsafe_allow_html=True)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    # Here you could integrate a real-time temperature trend; for now, we simulate a trend based on the current temperature.
    base_temp = environmental_data.get("temperature", 25)
    temp_values = [base_temp - 5 + i*0.5 for i in range(12)]
    df_temp = pd.DataFrame({"Month": months, "Avg Temp (°C)": temp_values}).set_index("Month")
    st.line_chart(df_temp)
    
    st.markdown('<div class="section-title">User Information</div>', unsafe_allow_html=True)
    df_user = pd.DataFrame.from_dict(user_data, orient='index', columns=["Value"])
    st.table(df_user)
    
    st.markdown('<div class="description">Use the sidebar to navigate to different sections of the application.</div>', unsafe_allow_html=True)
