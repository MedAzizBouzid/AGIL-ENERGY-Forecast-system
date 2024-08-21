from django.db import models

class NextCallDelivery(models.Model):
    ANCSCP=models.IntegerField()
    DATLIV=models.DateTimeField()
    LIBGVR=models.CharField(max_length=255)
    LIBLOC=models.CharField(max_length=255)
    LIBPRD=models.CharField(max_length=255)
    prixHT=models.FloatField()
    last_quantity_delivered=models.FloatField()
    next_call=models.FloatField()
# Create your models here.
