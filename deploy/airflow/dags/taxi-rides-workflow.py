from datetime import datetime, timedelta

# TODO
# Add a schedule
# Trigger whenever a new file gets available using the pattern

from airflow.sdk import DAG
from airflow.providers.cncf.kubernetes.operators.job import (
    KubernetesJobOperator
)
from airflow.operators.python import ShortCircuitOperator
import os


def should_run_for_today():
    today = datetime.now().strftime("%Y-%m-%d")
    data_file = f"/opt/airflow/data-dir/{today}.taxi-rides.parquet"
    metadata_file = f"/opt/airflow/data-dir/{today}.taxi-rides.run-metadata.json"

    print(f"Checking for {data_file}and {metadata_file}")    
    if os.path.exists(data_file) and not os.path.exists(metadata_file):
        print(f"Outlier detection for {data_file} will be run.")
        return True

    print(f"Outlier detection for {data_file} will be skipped.")
    return False
    return False

with DAG(
    "taxi-rides-outlier-detection",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function, # or list of functions
        # 'on_success_callback': some_other_function, # or list of functions
        # 'on_retry_callback': another_function, # or list of functions
        # 'sla_miss_callback': yet_another_function, # or list of functions
        # 'on_skipped_callback': another_function, #or list of functions
        # 'trigger_rule': 'all_success'
    },
    description="Taxi rides outlier detection workflow",
    #schedule=timedelta(days=1),
    #start_date=datetime(2021, 1, 1),
    #catchup=False
) as dag:

    outlier_detection = KubernetesJobOperator(
        task_id="outlier-detection",
        #image="taxi-rides-outlier-detection",
        #cmds=["detect-taxi-ride-outliers", "/data"],
        #name="detect-taxi-ride-outliers",
        job_template_file="/opt/airflow/dags/k8s-jobs/taxi-rides-outlier-detection-job.yaml",
        wait_until_job_complete=True,
        retries=0
    )

    data_drift_detection = KubernetesJobOperator(
        task_id="data_drift_dectection",
        #image="taxi-rides-outlier-detection",
        #cmds=["detect-taxi-ride-outliers", "/data"],
        #name="detect-taxi-ride-outliers",
        job_template_file="/opt/airflow/dags/k8s-jobs/taxi-rides-data-drift-detection-job.yaml",
        wait_until_job_complete=True,
        retries=0
    )

    outlier_detection >> data_drift_detection

    should_run_for_today = ShortCircuitOperator(
        task_id='should_run_for_today',
        python_callable=should_run_for_today,
        retries=0
    )

    should_run_for_today >> outlier_detection



