import os
import django
from django.db.models import Sum, Count
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import OlympicStats

def debug_charts():
    print("--- Debugging France Data ---")
    france_qs = OlympicStats.objects.filter(country_3_letter_code='FRA')
    print(f"France rows count: {france_qs.count()}")
    
    if france_qs.count() == 0:
        print("No rows found for 'FRA'. Checking distinct codes close to 'F'...")
        codes = OlympicStats.objects.values_list('country_3_letter_code', flat=True).distinct()
        f_codes = [c for c in codes if c and 'F' in c]
        print(f"Codes containing 'F': {f_codes[:20]}")
    else:
        print("France data found. Aggregating...")
        aggs = france_qs.aggregate(
            Or=Sum('gold_medals'),
            Argent=Sum('silver_medals'),
            Bronze=Sum('bronze_medals')
        )
        print(f"France Aggregates: {aggs}")

    print("\n--- Debugging Map Data ---")
    country_medals = (
        OlympicStats.objects
        .values('country_3_letter_code')
        .annotate(total_medals=Sum('total_medals'))
        .order_by('-total_medals')
    )
    count = country_medals.count()
    print(f"Country Groups count: {count}")
    
    if count > 0:
        print(f"Top 5 Countries: {list(country_medals[:5])}")
        
    df_map = pd.DataFrame(list(country_medals))
    print(f"\nDataFrame Shape: {df_map.shape}")
    print(f"DataFrame Head:\n{df_map.head()}")
    
    if df_map.empty:
        print("DataFrame is empty!")

if __name__ == "__main__":
    debug_charts()
