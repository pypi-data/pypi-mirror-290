from datetime import datetime, timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflowgp.operators.greenplum_operator import GreenplumOperator

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'example_greenplum_dag',
    default_args=default_args,
    description='A simple DAG to run SQL commands on Greenplum',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    catchup=False,
)

# Task to run a SQL query
run_sql_task = GreenplumOperator(
    task_id='run_sql',
    sql="""SELECT * FROM pg_catalog.pg_tables LIMIT 10;""",
    gp_conn_id='gp_conn_id',  # Ensure this connection ID is configured in Airflow
    autocommit=True,
    dag=dag,
)

# Define the task sequence
run_sql_task