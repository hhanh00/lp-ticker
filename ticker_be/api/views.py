from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework import status
from .models import PriceItem
from .serializers import PriceItemSerializer

@api_view(['GET', 'POST'])
def get_data(request):
  if request.method == 'POST':
    data = request.data
    PriceItem.objects.create(time=data['time'], value=data['value'])
    return Response(status=status.HTTP_201_CREATED)
  else:
    start_date = timezone.make_aware(datetime.strptime(request.GET['start_date'], '%Y-%m-%d'))
    end_date = timezone.make_aware(datetime.strptime(request.GET['end_date'], '%Y-%m-%d')) + timedelta(days=1)
    items = PriceItem.objects.filter(time__gte=start_date, time__lte=end_date)
    ser = PriceItemSerializer(items, many=True)
    return Response(ser.data)
