import streamlit as st
from src.database import get_db_connection
from src.visualization import plot_medals_by_country, plot_participation_trends

# Set page config
st.set_page_config(page_title="Olympic Games Analytics", page_icon="🏅", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data Exploration", "Predictions", "Clustering"])

if page == "Home":
    st.title("🏅 Olympic Games Data Analytics")
    st.markdown("""
    Welcome to the 120 years of Olympic history analysis dashboard.
    
    This application allows you to:
    - **Explore** historical data from Athens 1896 to Beijing 2022.
    - **Visualize** trends and country performances.
    - **Predict** future outcomes using Machine Learning.
    - **Cluster** countries based on performance metrics.
    """)
    
    st.info("Please configure your Supabase connection in the `.env` file to get started.")

elif page == "Data Exploration":
    st.title("📊 Data Exploration")
    
    st.subheader("Medal Distribution per Country")
    fig_medals = plot_medals_by_country()
    if fig_medals:
        st.plotly_chart(fig_medals, use_container_width=True)
    else:
        st.warning("No data available for Medals. Database might be empty.")

    st.subheader("Participation Over Time")
    fig_trends = plot_participation_trends()
    if fig_trends:
        st.plotly_chart(fig_trends, use_container_width=True)
    else:
        st.warning("No data available for Trends.")

elif page == "Predictions":
    st.title("🔮 Predictions (Paris 2024)")
    st.write("Model integration coming soon.")

elif page == "Clustering":
    st.title("🗺️ Country Clustering")
    st.write("Clustering analysis coming soon.")
