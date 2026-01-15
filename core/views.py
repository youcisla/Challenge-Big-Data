from django.shortcuts import render
from django.db.models import Count, Sum
from .models import OlympicStats
import plotly.express as px
import pandas as pd

def home(request):
    # 1. Calculate KPIs
    total_games = OlympicStats.objects.values('slug_game').distinct().count()
    total_countries = OlympicStats.objects.values('country_3_letter_code').distinct().count()
    kpi_athletes = OlympicStats.objects.aggregate(total=Sum('total_athletes'))['total']
    kpi_medals = OlympicStats.objects.aggregate(total=Sum('total_medals'))['total']

    # 2. Charts (Global Map)
    country_medals = (
        OlympicStats.objects
        .values('country_3_letter_code')
        .annotate(total_medals=Sum('total_medals'))
        .order_by('-total_medals')
    )
    
    df_map = pd.DataFrame(list(country_medals))
    
    if not df_map.empty:
        # data type fix - use float to avoid binary packing issues
        df_map['total_medals'] = df_map['total_medals'].fillna(0).astype(float)

        # Create Choropleth
        map_fig = px.choropleth(
            df_map,
            locations="country_3_letter_code",
            locationmode="ISO-3",
            color="total_medals",
            hover_name="country_3_letter_code",
            color_continuous_scale="Viridis",
            title="Répartition Mondiale des Médailles (1896-2022)",
            labels={'total_medals': 'Médailles'}
        )
        
        map_fig.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular',
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", color="#f8fafc"),
            margin={"r":0,"t":40,"l":0,"b":0},
            coloraxis_colorbar=dict(
                title=dict(text="Médailles", font=dict(color="#f8fafc")),
                tickfont=dict(color="#f8fafc")
            )
        )
        
        chart_json = safe_json_dump(map_fig)
    else:
        chart_json = "null"

    context = {
        'total_games': total_games,
        'total_countries': total_countries,
        'total_athletes': kpi_athletes if kpi_athletes else 0,
        'total_medals': kpi_medals if kpi_medals else 0,
        'chart_json': chart_json
    }
    return render(request, 'core/home.html', context)

def explorer(request):
    # 1. France Specific Data 🇫🇷
    france_qs = OlympicStats.objects.filter(country_3_letter_code='FRA')
    
    # Medal Distribution (Pie Chart)
    # Sum gold, silver, bronze separately
    fra_medals = france_qs.aggregate(
        Or=Sum('gold_medals'),
        Argent=Sum('silver_medals'),
        Bronze=Sum('bronze_medals')
    )
    
    # Transform for Plotly
    # Use float to ensure JSON serialization creates numbers, not binary
    vals = [float(v) if v else 0.0 for v in fra_medals.values()]
    
    fra_pie_fig = px.pie(
        names=list(fra_medals.keys()),
        values=vals,
        title="Répartition des Médailles (France)",
        color_discrete_sequence=['#FFD700', '#C0C0C0', '#CD7F32'] # Gold, Silver, Bronze colors
    )
    fra_pie_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_family="Inter", font_color="#f8fafc")
    fra_pie_json = safe_json_dump(fra_pie_fig)

    # Performance Over Time (Line Chart)
    fra_timeline = list(france_qs.values('year', 'season', 'total_medals').order_by('year'))
    fra_line_fig = px.line(
        fra_timeline, 
        x='year', 
        y='total_medals', 
        color='season',
        title="Évolution du Nombre de Médailles (France)",
        markers=True,
        labels={'year': 'Année', 'total_medals': 'Médailles', 'season': 'Saison'}
    )
    fra_line_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family="Inter", font_color="#f8fafc")
    fra_line_json = safe_json_dump(fra_line_fig)

    # 2. General Trends 🌍
    top_hosts = (
        OlympicStats.objects
        .filter(is_host=1)
        .values('country_3_letter_code')
        .annotate(host_count=Count('year'))
        .order_by('-host_count')[:10]
    )
    
    hosts_bar_fig = px.bar(
        list(top_hosts),
        x='country_3_letter_code',
        y='host_count',
        title="Pays ayant accueilli le plus de Jeux",
        labels={'country_3_letter_code': 'Pays', 'host_count': 'Jeux Accueillis'},
        color='host_count'
    )
    hosts_bar_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family="Inter", font_color="#f8fafc", coloraxis_colorbar=dict(tickfont=dict(color="#f8fafc")))
    hosts_bar_json = safe_json_dump(hosts_bar_fig)

    context = {
        'fra_pie_json': fra_pie_json,
        'fra_line_json': fra_line_json,
        'hosts_bar_json': hosts_bar_json
    }
    return render(request, 'core/explorer.html', context)

def myths(request):
    # Data for the 11 Myths (Sample subset for prototype)
    myths_list = [
        {
            "id": 1,
            "question": "Les femmes ont-elles participé aux JO de Paris 1900 ?",
            "verdict": "VRAI",
            "verdict_color": "text-success",
            "insight": "Oui, 22 femmes ont concouru en Tennis et Golf, marquant la première participation féminine.",
            "icon": "bi-gender-female"
        },
        {
            "id": 2,
            "question": "La France a-t-elle accueilli les Jeux 5 fois ?",
            "verdict": "VRAI",
            "verdict_color": "text-success",
            "insight": "La France a accueilli : Paris 1900, Chamonix 1924, Paris 1924, Grenoble 1968, Albertville 1992.",
            "icon": "bi-flag-fill"
        },
        {
            "id": 3,
            "question": "Les USA sont-ils les leaders de tous les temps ?",
            "verdict": "VRAI",
            "verdict_color": "text-success",
            "insight": "Les USA détiennent le record avec plus de 2 600 médailles, loin devant toute autre nation.",
            "icon": "bi-trophy-fill"
        },
        {
            "id": 4,
            "question": "Les Jeux de St. Louis 1904 avaient-ils peu d'athlètes internationaux ?",
            "verdict": "VRAI",
            "verdict_color": "text-success",
            "insight": "En raison des difficultés de voyage, très peu d'athlètes non-américains ont participé.",
            "icon": "bi-airplane-engines"
        }
    ]
    
    context = {
        'myths': myths_list
    }
    context = {
        'myths': myths_list
    }
    return render(request, 'core/myths.html', context)

from .ml_service import MLService


def predictions(request):
    ml_service = MLService()
    results = ml_service.predict_paris_2024()
    
    # Separate France for "Golden Card"
    fra_prediction = next((item for item in results if item['country'] == 'FRA'), None)
    
    # Top 3 for Podium
    top_3 = results[:3] if len(results) >= 3 else results
    
    # Full Leaderboard
    leaderboard = results
    
    # Mock "Starts to Watch" (Athletes)
    stars = [
        {'name': 'Léon Marchand', 'country': 'FRA', 'sport': 'Natation', 'event': '400m 4 Nages', 'prob': 98, 'img': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/L%C3%A9on_Marchand_2023.jpg/640px-L%C3%A9on_Marchand_2023.jpg'},
        {'name': 'Simone Biles', 'country': 'USA', 'sport': 'Gymnastique', 'event': 'Concours Général', 'prob': 95, 'img': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Simone_Biles_at_the_2016_Olympics_all-around_gold_medal_podium_%2828902897262%29_%28cropped%29.jpg/480px-Simone_Biles_at_the_2016_Olympics_all-around_gold_medal_podium_%2828902897262%29_%28cropped%29.jpg'},
        {'name': 'Teddy Riner', 'country': 'FRA', 'sport': 'Judo', 'event': '+100kg', 'prob': 85, 'img': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Teddy_Riner_Rio_2016.jpg/480px-Teddy_Riner_Rio_2016.jpg'},
        {'name': 'Armand Duplantis', 'country': 'SWE', 'sport': 'Athlétisme', 'event': 'Saut à la perche', 'prob': 99, 'img': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Armand_Duplantis_2020.jpg/480px-Armand_Duplantis_2020.jpg'},
        {'name': 'Noah Lyles', 'country': 'USA', 'sport': 'Athlétisme', 'event': '100m', 'prob': 75, 'img': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Noah_Lyles_Doha_2019.jpg/480px-Noah_Lyles_Doha_2019.jpg'},
    ]
    
    context = {
        'fra_prediction': fra_prediction,
        'top_3': top_3,
        'leaderboard': leaderboard,
        'stars': stars,
    }
    return render(request, 'core/predictions.html', context)

def comparison(request):
    """
    Compares AI predictions with 'Official' (Mocked) results.
    """
    ml_service = MLService()
    preds = ml_service.predict_paris_2024()
    
    # Mock Official Results (Simulated for Demo)
    import random
    random.seed(42) # Fixed seed for consistency
    
    comp_data = []
    
    for p in preds:
        predicted = p['predicted_medals']
        # Simulate 'Actual' results with some variance
        variance = random.randint(-5, 5)
        real = max(0, predicted + variance)
        
        diff = real - predicted
        
        status = 'perfect' if diff == 0 else ('under' if diff > 0 else 'over')
        
        comp_data.append({
            'country': p['country'],
            'predicted': predicted,
            'real': real,
            'diff': diff,
            'status': status,
            'abs_diff': abs(diff)
        })
        
    # Sort by 'Real' medals count
    comp_data.sort(key=lambda x: x['real'], reverse=True)
    
    context = {
        'comparison': comp_data
    }
    return render(request, 'core/comparison.html', context)

# UTILITY
import json
import numpy as np
import base64

def deep_decode_bdata(obj):
    """
    Recursively decode Plotly's 'bdata' (binary encoded arrays) back to standard lists.
    """
    if isinstance(obj, dict):
        if 'bdata' in obj and 'dtype' in obj:
            # Decode bdata
            bdata = obj['bdata']
            dtype_str = obj['dtype']
            try:
                decoded_bytes = base64.b64decode(bdata)
                # Map plotly dtype strings to numpy dtypes
                # 'f8' = float64, 'f4' = float32, 'i8' = int64, etc.
                np_dtype = np.dtype(dtype_str)
                array = np.frombuffer(decoded_bytes, dtype=np_dtype)
                return array.tolist()
            except Exception as e:
                # Fallback if decoding fails
                print(f"Bdata decode failed: {e}")
                return obj
        else:
            return {k: deep_decode_bdata(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [deep_decode_bdata(item) for item in obj]
    return obj

def safe_json_dump(fig):
    """
    Serializes a Plotly figure to a JSON string, ensuring NO binary packing.
    """
    # 1. Get dictionary (which might contain bdata)
    fig_dict = fig.to_dict()
    
    # 2. Recursively convert bdata back to lists
    clean_dict = deep_decode_bdata(fig_dict)
    
    # 3. Dump to JSON (numpy types are now lists, but handle any stragglers)
    def default_serializer(obj):
        if hasattr(obj, 'tolist'):
            return obj.tolist()
        if isinstance(obj, (np.int64, np.int32, np.int16)):
             return int(obj)
        if isinstance(obj, (np.float64, np.float32)):
             return float(obj)
        raise TypeError(f"Type {type(obj)} is not serializable")

    return json.dumps(clean_dict, default=default_serializer)
