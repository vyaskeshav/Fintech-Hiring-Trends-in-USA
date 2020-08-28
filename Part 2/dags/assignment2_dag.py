from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# Following are defaults which can be overridden later on
default_args = {
    'owner': 'keshav.vyas',
    'depends_on_past': False,
    'start_date': datetime(2019, 2, 26),
    'email': ['keshav,vyas14@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('assignment2_dag', default_args=default_args,schedule_interval= None)

# t1, t2, t3 and t4- 2 more tasks to be added S3 downloads and csv merging

t2 = BashOperator(
    task_id='part1',
    bash_command='python3 /root/airflow/dags/data_mapping.py',
    dag=dag)


t3 = BashOperator(
    task_id='part2',
    bash_command='ipython /root/airflow/dags/actionable_insights.py',
    dag=dag)

	
t2 >> t3
