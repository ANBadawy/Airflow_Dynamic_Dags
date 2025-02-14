from django.db import models

# Create your models here.

class Simulator(models.Model):
    start_date = models.DateTimeField()
    interval = models.CharField(
        max_length=50,
        choices=[('@hourly', '@hourly'), ('@daily', '@daily')],
    )  
    kpi_id = models.IntegerField() 

    def __str__(self):
        return f"Simulator {self.id} - KPI {self.kpi_id}"


class SimulatorResult(models.Model):
    simulator = models.ForeignKey(Simulator, on_delete=models.CASCADE)
    asset_id = models.CharField(max_length=50)
    attribute_id = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    value = models.FloatField()

    def __str__(self):
        return f"Result for Simulator {self.simulator.id} - Value: {self.value}"
