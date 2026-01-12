import plotly.express as px
import pandas as pd
from src.database import run_query

def get_medals_by_country_data():
    """
    Query the database for medal counts by country.
    """
    query = """
    SELECT country_name, medal_type, COUNT(*) as count
    FROM medals
    GROUP BY country_name, medal_type
    ORDER BY count DESC
    LIMIT 50; -- Top 50 entries for clarity
    """
    result = run_query(query)
    if result:
        return pd.DataFrame(result)
    return pd.DataFrame(columns=["country_name", "medal_type", "count"])

def plot_medals_by_country():
    df = get_medals_by_country_data()
    if df.empty:
        return None
    
    fig = px.bar(
        df, 
        x="country_name", 
        y="count", 
        color="medal_type", 
        title="Top Countries by Medal Count",
        barmode='stack',
        color_discrete_map={
            'GOLD': '#FFD700',
            'SILVER': '#C0C0C0',
            'BRONZE': '#CD7F32'
        }
    )
    return fig

def get_participation_trends_data():
    """
    Query how many athletes participated over the years.
    """
    # Note: We counting entries in results as a proxy for participation if we don't have exact distinct counts easily
    # Or we can join hosts.
    query = """
    SELECT h.game_year, h.game_season, COUNT(DISTINCT r.athlete_url) as athlete_count
    FROM results r
    JOIN hosts h ON r.game_slug = h.game_slug
    GROUP BY h.game_year, h.game_season
    ORDER BY h.game_year;
    """
    result = run_query(query)
    if result:
        return pd.DataFrame(result)
    return pd.DataFrame(columns=["game_year", "game_season", "athlete_count"])

def plot_participation_trends():
    df = get_participation_trends_data()
    if df.empty:
        return None
        
    fig = px.line(
        df, 
        x="game_year", 
        y="athlete_count", 
        color="game_season",
        title="Athlete Participation Over Time",
        markers=True
    )
    return fig

