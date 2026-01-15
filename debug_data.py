import os
import django
from django.db.models import Sum

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import OlympicStats

def check_data():
    print("Checking OlympicStats data...")
    count = OlympicStats.objects.count()
    print(f"Total rows: {count}")
    
    if count > 0:
        first = OlympicStats.objects.first()
        print(f"Sample row: {first.__dict__}")
        
        sums = OlympicStats.objects.aggregate(
            total_medals=Sum('total_medals'),
            total_athletes=Sum('total_athletes')
        )
        print(f"Aggregates: {sums}")
        
        # Check for nulls
        null_medals = OlympicStats.objects.filter(total_medals__isnull=True).count()
        print(f"Rows with null total_medals: {null_medals}")

if __name__ == "__main__":
    check_data()
