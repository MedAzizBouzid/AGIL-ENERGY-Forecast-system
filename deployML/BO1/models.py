from django.db import models

class ClientHistory(models.Model):
    ANCSCP=models.IntegerField()
    DATLIV=models.DateTimeField()
    LIBGVR=models.CharField(max_length=255)
    LIBLOC=models.CharField(max_length=255)
    LIBPRD=models.CharField(max_length=255)
    QTEPRD=models.FloatField()
    prixHT=models.FloatField()
    lag1_previous_order=models.FloatField()
    lag3_previous_order=models.FloatField()
    lag6_previous_order=models.FloatField()
    lag9_previous_order=models.FloatField()

class PredictClient(models.Model):
    ANCSCP=models.IntegerField()
    DATLIV=models.DateTimeField()
    LIBGVR=models.CharField(max_length=255)
    LIBLOC=models.CharField(max_length=255)
    LIBPRD=models.CharField(max_length=255)
    prixHT=models.FloatField()
    lag1_previous_order=models.FloatField()
    lag3_previous_order=models.FloatField()
    lag6_previous_order=models.FloatField()
    lag9_previous_order=models.FloatField()
    prediction=models.FloatField()

# Create your models here.
