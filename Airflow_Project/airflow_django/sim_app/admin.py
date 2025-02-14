from django.contrib import admin
from .models import Simulator, SimulatorResult

# Register your models here.

@admin.register(Simulator)
class SimulatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date', 'interval', 'kpi_id')

@admin.register(SimulatorResult)
class SimulatorResultAdmin(admin.ModelAdmin):
    list_display = ('simulator', 'asset_id', 'attribute_id', 'timestamp', 'value')
