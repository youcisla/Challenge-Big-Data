from django.shortcuts import render
from django.db.models import Count, Sum
from .models import OlympicStats
import plotly.express as px
import pandas as pd
import os
from django.conf import settings

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
    fra_timeline_df = pd.DataFrame(fra_timeline)
    
    if not fra_timeline_df.empty:
        fra_line_fig = px.line(
            fra_timeline_df, 
            x='year', 
            y='total_medals', 
            color='season',
            title="Évolution du Nombre de Médailles (France)",
            markers=True,
            labels={'year': 'Année', 'total_medals': 'Médailles', 'season': 'Saison'}
        )
        fra_line_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family="Inter", font_color="#f8fafc")
    else:
        # Fallback empty chart
        fra_line_fig = px.line(title="Évolution du Nombre de Médailles (France)")
        fra_line_fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_family="Inter", 
            font_color="#f8fafc",
            annotations=[dict(text="Aucune donnée disponible", showarrow=False, font_size=16)]
        )
    fra_line_json = safe_json_dump(fra_line_fig)

    # 2. General Trends 🌍
    top_hosts = (
        OlympicStats.objects
        .filter(is_host=1)
        .values('country_3_letter_code')
        .annotate(host_count=Count('year'))
        .order_by('-host_count')[:10]
    )
    top_hosts_df = pd.DataFrame(list(top_hosts))
    
    if not top_hosts_df.empty:
        hosts_bar_fig = px.bar(
            top_hosts_df,
            x='country_3_letter_code',
            y='host_count',
            title="Pays ayant accueilli le plus de Jeux",
            labels={'country_3_letter_code': 'Pays', 'host_count': 'Jeux Accueillis'},
            color='host_count'
        )
        hosts_bar_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family="Inter", font_color="#f8fafc", coloraxis_colorbar=dict(tickfont=dict(color="#f8fafc")))
    else:
        # Fallback empty chart
        hosts_bar_fig = px.bar(title="Pays ayant accueilli le plus de Jeux")
        hosts_bar_fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_family="Inter", 
            font_color="#f8fafc",
            annotations=[dict(text="Aucune donnée disponible", showarrow=False, font_size=16)]
        )
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
    Compares AI predictions with OFFICIAL Paris 2024 results.
    """
    ml_service = MLService()
    preds = ml_service.predict_paris_2024()
    
    # OFFICIAL PARIS 2024 RESULTS (Source: User Provided)
    # Mapping Country Name -> (Gold, Silver, Bronze, Total)
    # We need to map these Names to our 3-Letter Codes.
    # Common IOC Code Mapping:
    name_to_code = {
        'United States': 'USA', 'China': 'CHN', 'Japan': 'JPN', 'Australia': 'AUS', 'France': 'FRA',
        'Netherlands': 'NED', 'Great Britain': 'GBR', 'South Korea': 'KOR', 'Italy': 'ITA', 'Germany': 'GER',
        'New Zealand': 'NZL', 'Canada': 'CAN', 'Uzbekistan': 'UZB', 'Hungary': 'HUN', 'Spain': 'ESP',
        'Sweden': 'SWE', 'Kenya': 'KEN', 'Norway': 'NOR', 'Ireland': 'IRL', 'Brazil': 'BRA',
        'Iran': 'IRI', 'Ukraine': 'UKR', 'Romania': 'ROU', 'Georgia': 'GEO', 'Belgium': 'BEL',
        'Bulgaria': 'BUL', 'Serbia': 'SRB', 'Czech Republic': 'CZE', 'Denmark': 'DEN', 'Azerbaijan': 'AZE',
        'Croatia': 'CRO', 'Cuba': 'CUB', 'Bahrain': 'BRN', 'Slovenia': 'SLO', 'Chinese Taipei': 'TPE',
        'Austria': 'AUT', 'Hong Kong': 'HKG', 'Philippines': 'PHI', 'Algeria': 'ALG', 'Indonesia': 'INA',
        'Israel': 'ISR', 'Poland': 'POL', 'Kazakhstan': 'KAZ', 'Jamaica': 'JAM', 'South Africa': 'RSA',
        'Thailand': 'THA', 'Ethiopia': 'ETH', 'Switzerland': 'SUI', 'Ecuador': 'ECU', 'Portugal': 'POR',
        'Greece': 'GRE', 'Argentina': 'ARG', 'Egypt': 'EGY', 'Tunisia': 'TUN', 'Botswana': 'BOT',
        'Chile': 'CHI', 'Saint Lucia': 'LCA', 'Uganda': 'UGA', 'Dominican Republic': 'DOM', 'Guatemala': 'GUA',
        'Morocco': 'MAR', 'Dominica': 'DMA', 'Pakistan': 'PAK', 'Turkey': 'TUR', 'Mexico': 'MEX',
        'Armenia': 'ARM', 'Colombia': 'COL', 'Kyrgyzstan': 'KGZ', 'North Korea': 'PRK', 'Lithuania': 'LTU',
        'India': 'IND', 'Moldova': 'MDA', 'Kosovo': 'KOS', 'Cyprus': 'CYP', 'Fiji': 'FIJ',
        'Jordan': 'JOR', 'Mongolia': 'MGL', 'Panama': 'PAN', 'Tajikistan': 'TJK', 'Albania': 'ALB',
        'Grenada': 'GRN', 'Malaysia': 'MAS', 'Puerto Rico': 'PUR', 'Cape Verde': 'CPV', 'Ivory Coast': 'CIV',
        'Peru': 'PER', 'Qatar': 'QAT', 'Refugee Olympic Team': 'EOR', 'Singapore': 'SGP', 'Slovakia': 'SVK',
        'Zambia': 'ZAM'
    }

    # Data: Total Medals - Load from CSV
    official_by_code = {}
    try:
        csv_path = os.path.join(settings.BASE_DIR, 'data', 'res2024.csv')
        # Use pandas for easy reading (assuming simple format: Rank,NOC,Gold,Silver,Bronze,Total)
        if os.path.exists(csv_path):
            df_res = pd.read_csv(csv_path)
            # Ensure columns exist
            if 'NOC' in df_res.columns and 'Total' in df_res.columns:
                for _, row in df_res.iterrows():
                    country_name = str(row['NOC']).strip()
                    total = int(row['Total'])
                    
                    # Map Name -> Code
                    # First try direct map
                    code = name_to_code.get(country_name)
                    
                    # If failed, try some manual overrides for common mismatches in Olympic data
                    if not code:
                        manual_map = {
                            "People's Republic of China": "CHN",
                            "Republic of Korea": "KOR",
                            "Chinese Taipei": "TPE", 
                            "Hong Kong, China": "HKG",
                            "Great Britain": "GBR",
                            "United States of America": "USA",
                            "Islamic Republic of Iran": "IRI",
                            "Democratic People's Republic of Korea": "PRK",
                            "Türkiye": "TUR",
                            "Czechia": "CZE",
                            "Republic of Moldova": "MDA"
                        }
                        code = manual_map.get(country_name)
                        if not code:
                           # Reverse lookup in name_to_code (risky but better than nothing)? 
                           # No, stick to safe maps.
                           pass

                    if code:
                        official_by_code[code] = total
        else:
            print(f"RES2024 CSV not found at {csv_path}")

        print(f"DEBUG: Official Data Loaded. Count: {len(official_by_code)}")
        if 'USA' in official_by_code:
            print(f"DEBUG: USA found -> {official_by_code['USA']}")
        else:
            print("DEBUG: USA NOT FOUND in official_by_code")

    except Exception as e:
        print(f"Error loading RES2024 CSV: {e}")
            
    comp_data = []
    
    for p in preds:
        code = p['country']
        predicted = p['predicted_medals']
        xgb_val = p.get('predicted_medals_xgb', 0)
        rf_val = p.get('predicted_medals_rf', 0)
        
        # Get real or default to 0 if not in list
        real = official_by_code.get(code, 0)
        
        # Only compare if we have real data (or if predicted > 0, we assume real is 0 if missing)
        # To avoid clutter, let's include if either predicted > 0 or real > 0
        if predicted == 0 and real == 0:
            continue
            
        diff = real - predicted
        
        if diff == 0:
            status = 'perfect'
        elif diff > 0:
            status = 'under' # Predicted under real -> Good surprise
        else:
            status = 'over' # Predicted over real -> Disappointment
            
        comp_data.append({
            'country': code,
            'predicted': predicted,
            'predicted_xgb': xgb_val,
            'predicted_rf': rf_val,
            'real': real,
            'diff': diff,
            'status': status,
            'abs_diff': abs(diff)
        })
        
    # Sort by 'Real' medals count
    comp_data.sort(key=lambda x: x['predicted'], reverse=True)
    
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
