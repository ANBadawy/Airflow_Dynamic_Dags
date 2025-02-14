import os
import django
import random
import requests
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import sys
from croniter import croniter

# Setup Django environment
sys.path.append('/mnt/e/Assignments/Airflow/airflow/airflow_django')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airflow_project.settings')
django.setup()

# Import Simulator and SimulatorResult models from the new project
from sim_app.models import Simulator, SimulatorResult

def validate_schedule_interval(interval):
    """
    Validate the schedule_interval.
    """
    try:
        if isinstance(interval, str) and croniter.is_valid(interval):
            return interval
        elif isinstance(interval, timedelta):
            return interval
        elif interval in ["@once", "@hourly", "@daily", "@weekly", "@monthly"]:
            return interval
        else:
            raise ValueError(f"Invalid schedule interval: {interval}")
    except Exception as e:
        raise ValueError(f"Invalid schedule interval: {interval} - {e}")

def send_to_api(simulator_id, **kwargs):

    simulator = Simulator.objects.get(id=simulator_id)
    random_value = random.uniform(10, 200)
    payload = {
        "asset_id": simulator.kpi_id,
        "attribute_id": "1",
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ[UTC]"),
        "value": random_value,
    }

    # Send data to the previous project API
    url = "http://127.0.0.1:8000/api/input/ingester/"
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        response_data = response.json()

        # Save the response to the database
        SimulatorResult.objects.create(
            simulator=simulator,
            asset_id=response_data.get("asset_id"),
            attribute_id=response_data.get("attribute_id"),
            timestamp=datetime.strptime(response_data.get("timestamp"), "%Y-%m-%dT%H:%M:%SZ[UTC]"),
            value=response_data.get("value"),
        )
        print(f"Response saved for Simulator {simulator_id}: {response_data}")

    except requests.exceptions.RequestException as e:
        print(f"Error processing Simulator {simulator_id}: {e}")

def create_dynamic_dag(simulator):
    """Dynamically create a DAG for each Simulator instance."""
    dag_id = f"simulator_{simulator.id}_dag"
    default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    }

    # Validate the simulator.interval value
    try:
        schedule_interval = validate_schedule_interval(simulator.interval)
    except ValueError as e:
        print(f"Skipping Simulator {simulator.id} due to invalid interval: {e}")
        return None

    dag = DAG(
        dag_id,
        default_args=default_args,
        description=f"DAG for Simulator {simulator.id}",
        schedule_interval=schedule_interval,
        start_date=simulator.start_date,
        catchup=False,
    )

    with dag:
        task = PythonOperator(
            task_id=f"send_to_api_{simulator.id}",
            python_callable=send_to_api,
            op_kwargs={'simulator_id': simulator.id},
        )

    return dag

# Dynamically create a DAG for each Simulator instance
simulators = Simulator.objects.all()
for simulator in simulators:
    dag = create_dynamic_dag(simulator)
    if dag:  # Only add the DAG if it was successfully created
        globals()[dag.dag_id] = dag
