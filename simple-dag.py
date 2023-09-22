from airflow import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import json
from datetime import datetime
from pandas import json_normalize

# Define the Bash command to import data from the CSV file into the SQLite database
bash_command = (
    'echo -e ".separator \",\"\n.import /tmp/processed_user.csv" | '
    'sqlite3 airflow.db'
    )

    # Use the BashOperator to execute the Bash command


def _process_user(ti):
        user = ti.xcom_pull(task_ids="extract_user")
        user = user['results'][0]
        processed_user = json_normalize({
            'firstname': user['name']['first'],
            'lastname': user['name']['last'],
            'country': user['location']['country'],
            'username': user['login']['username'],
            'password': user['login']['password'],
            'email': user['email']
        })
        processed_user.to_csv('/tmp/processed_user.csv', index=None, header=False)
# Define the DAG
with DAG('user_processing', start_date=datetime(2022, 1, 1),
         schedule_interval='@daily', catchup=False) as dag:

    # Task to create a table in SQLite
    create_table = SqliteOperator(
        task_id='create_table',
        sql='''
            CREATE TABLE IF NOT EXISTS users (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL PRIMARY KEY
            );
        ''',
        sqlite_conn_id='sqlite_conn'  # Specify your SQLite connection ID here
    )

    # Task to check if the API is available
    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='user_api',
        endpoint='https://randomuser.me/api/'
    )

    # Task to extract user data from the API
    extract_user = SimpleHttpOperator(
        task_id='extract_user',
        http_conn_id='user_api',
        endpoint='https://randomuser.me/api/',
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    # Task to process user data

    process_user = PythonOperator(
        task_id='process_user',
        python_callable=_process_user
    )

    # Task to store processed user data in SQLite
    bash_operator = BashOperator(
        task_id='store_user',
        bash_command=bash_command,
    )

    # Define the task dependencies
    create_table >> is_api_available >> extract_user >> process_user >> bash_operator
