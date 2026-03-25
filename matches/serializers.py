from rest_framework import serializers
from .models import Match
from items.serializers import ItemListSerializer


class MatchSerializer(serializers.ModelSerializer):
    found_item = ItemListSerializer(read_only=True)
    lost_item = ItemListSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Match
        fields = ['id', 'found_item', 'lost_item', 'score', 'reason',
                  'status', 'status_display', 'created_at']
