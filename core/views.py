from django.shortcuts import render
from django.db.models import Count, Sum
from .models import OlympicStats
import plotly.express as px

def home(request):
    # 1. Calculate KPIs (Aggregated from creating a queryset)
    # Note: Because our data is Country-Per-Game, distinct counts need strict handling
    
    # Total Games: Count distinct (game_slug)
    total_games = OlympicStats.objects.values('slug_game').distinct().count()
    
    # Total Countries: Count distinct (country_3_letter_code)
    total_countries = OlympicStats.objects.values('country_3_letter_code').distinct().count()
    
    # Total Athletes: Sum of 'total_athletes' field
    # But note: total_athletes in CSV is per country-year. Adding them up gives total participations.
    # To get unique humans we need athlete names, which we don't have.
    # So we sum "Total Participations"
    kpi_athletes = OlympicStats.objects.aggregate(total=Sum('total_athletes'))['total']
    
    # Total Medals
    kpi_medals = OlympicStats.objects.aggregate(total=Sum('total_medals'))['total']

    # 2. Charts (Top 10 Countries)
    # Group by Country -> Sum Medals -> Order Desc -> Limit 10
    top_countries = (
        OlympicStats.objects
        .values('country_3_letter_code')
        .annotate(medals=Sum('total_medals'))
        .order_by('-medals')[:10]
    )
    
    # Convert to list for Plotly
    data = list(top_countries)
    
    # Create Plotly Figure
    if data:
        fig = px.bar(
            data, 
            x='country_3_letter_code', 
            y='medals',
            title='Top 10 Countries by All-Time Medals',
            labels={'country_3_letter_code': 'Country', 'medals': 'Total Medals'},
            color='medals',
            color_continuous_scale='Viridis' # Professional gradient
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        chart_html = fig.to_html(full_html=False, include_plotlyjs=False)
    else:
        chart_html = "<p class='text-center p-4'>No data available for charts.</p>"

    context = {
        'total_games': total_games,
        'total_countries': total_countries,
        'total_athletes': f"{kpi_athletes:,}" if kpi_athletes else 0,
        'total_medals': f"{kpi_medals:,}" if kpi_medals else 0,
        'chart_html': chart_html
    }
    return render(request, 'core/home.html', context)
