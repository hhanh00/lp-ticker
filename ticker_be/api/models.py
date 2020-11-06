from django.db import models

class PriceItem(models.Model):
  time = models.DateTimeField(unique=True)
  value = models.DecimalField(max_digits=12, decimal_places=4)
