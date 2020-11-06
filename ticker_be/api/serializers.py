from rest_framework import serializers
from .models import PriceItem

class TimestampField(serializers.Field):
  def to_representation(self, value):
    return value.timestamp()

class PriceItemSerializer(serializers.ModelSerializer):
  time = TimestampField()
  class Meta:
    model = PriceItem
    fields = ['time', 'value']
