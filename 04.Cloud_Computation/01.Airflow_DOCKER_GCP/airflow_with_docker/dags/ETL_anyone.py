from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from  load_dag import main_load_dag
from  transform_dag import main_transform_dag
from  plots_dag import main_plots_dag

TAGS = ['PythonDataFlow']
DAG_ID = "ETL_anyone"
DAG_DESCRIPTION = """ETL"""
DAG_SCHEDULE = "0 9 * * *"
default_args = {
"start_date": datetime(2024, 8, 6),
}
retries = 4
retry_delay = timedelta(minutes=60)

def execute_taks():
    print("Hola Mundo")

dag = DAG(
dag_id=DAG_ID,
description=DAG_DESCRIPTION,
catchup=False,
schedule_interval=DAG_SCHEDULE,
max_active_runs=1,
dagrun_timeout=200000,
default_args=default_args,
tags=TAGS
)

def chao():
    print("################################### TU PRIMER ETL EN AIRFLOW *** -----------------------------")

with dag as dag:
    load_task = PythonOperator(
        task_id="carga",
        python_callable=main_load_dag,
    )

    transform_task = PythonOperator(
        task_id="transformacion",
        python_callable=main_transform_dag,
    )

    plot_task = PythonOperator(
        task_id="plots",
        python_callable=main_plots_dag,
    )


    end_task = PythonOperator(
        task_id="finaliza_proceso",
        python_callable=chao,
    )

load_task >> transform_task >> [plot_task , end_task]