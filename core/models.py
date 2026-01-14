from django.db import models

class OlympicStats(models.Model):
    year = models.IntegerField(blank=True, null=True)
    slug_game = models.CharField(max_length=255, blank=True, null=True)
    country_3_letter_code = models.CharField(max_length=10, blank=True, null=True)
    bronze_medals = models.IntegerField(blank=True, null=True)
    gold_medals = models.IntegerField(blank=True, null=True)
    silver_medals = models.IntegerField(blank=True, null=True)
    total_medals = models.IntegerField(blank=True, null=True)
    total_athletes = models.IntegerField(blank=True, null=True)
    avg_age_athletes = models.FloatField(blank=True, null=True)
    medals_in_current_year = models.IntegerField(blank=True, null=True)
    game_slug = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    season = models.CharField(max_length=50, blank=True, null=True)
    game_name = models.CharField(max_length=255, blank=True, null=True)
    cumulative_medals = models.FloatField(blank=True, null=True)
    is_host = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'olympic_stats'

    def __str__(self):
        return f"{self.slug_game} - {self.country_3_letter_code}"
