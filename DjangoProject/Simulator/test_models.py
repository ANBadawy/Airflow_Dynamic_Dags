import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airflow_project.settings')
django.setup()

from sim_app.models import Simulator, SimulatorResult

simulator = Simulator.objects.get(id=1)  # Replace with an actual simulator ID
SimulatorResult.objects.create(
    simulator=simulator,
    asset_id="1",
    attribute_id="1",
    timestamp=datetime.now(),
    value=123
)
print("Simulator result saved successfully.")
