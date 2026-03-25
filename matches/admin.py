from django.contrib import admin
from .models import Match

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['found_item', 'lost_item', 'score', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['found_item__title', 'lost_item__title']
