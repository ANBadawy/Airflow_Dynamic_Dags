from django.db import models

class KPI(models.Model):
    name = models.CharField(max_length=100)
    expression = models.TextField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Asset(models.Model):
    asset_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.asset_id

class Attribute(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='attributes')
    attribute_id = models.CharField(max_length=50)
    # kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, related_name='attributes')
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.asset.asset_id} - {self.attribute_id}"
