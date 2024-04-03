from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import json
import pandas as pd
from sqlalchemy import create_engine

city_name = ''
OpenWeather_API_key = ''
end_point_link = f'/data/2.5/weather?q={city_name}&appid={OpenWeather_API_key}'
kelvin_to_celcius = lambda k: round(k - 273.15,2)

def transform_load_data(task_instance):
    
    data = task_instance.xcom_pull(task_ids='extract_weather_data')
    city = data['name']
    weather_description = data['weather'][0]['description']
    temperature = kelvin_to_celcius(data['main']['temp'])
    feels_like = kelvin_to_celcius(data['main']['feels_like'])
    min_temperature = kelvin_to_celcius(data['main']['temp_min'])
    max_temperature = kelvin_to_celcius(data['main']['temp_max'])
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    cloudiness = data['clouds']['all']
    time_of_record = datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
    sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%Y-%m-%d %H:%M:%S')
    sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%Y-%m-%d %H:%M:%S')

    transformed_data = {
        'City': city,
        'Weather Description': weather_description,
        'Temperature': temperature,
        'Feels Like': feels_like,
        'Min Temperature': min_temperature,
        'Max Temperature': max_temperature,
        'Pressure': pressure,
        'Humidity': humidity,
        'Wind Speed': wind_speed,
        'Cloudiness': cloudiness,
        'Time of Record': time_of_record,
        'Sunrise (Local Time)': sunrise,
        'Sunset (Local Time)': sunset
    }

    transformed_data_list = [transformed_data]
    global df_data 
    df_data = pd.DataFrame(transformed_data_list)
    aws_credentials = {"key": "", "secret": "AsSKGf3RJ7d+", "token":""}
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dt_string = f"Current_Weather_{city_name} {now}"
    df_data.to_csv(f's3://myairflow-weather-s3-bucket/{dt_string}.csv', index=False, storage_options=aws_credentials)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 2),
    'email' : ['itisqaisar@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG('weather_dag',
    default_args=default_args,
    description='A simple weather DAG',
    schedule_interval= timedelta(minutes=1),
    catchup=False
    ) as dag:
    
    is_weather_api_ready = HttpSensor(
    task_id='is_weather_api_ready',
    http_conn_id='weathermap_api',
    endpoint= end_point_link,
    )
    
    extract_weather_data = SimpleHttpOperator(
    task_id = 'extract_weather_data',
    http_conn_id = 'weathermap_api',
    endpoint = end_point_link,
    method = 'GET',
    response_filter = lambda r: json.loads(r.text),
    log_response = True  
    )
    
    transform_load_weather_data = PythonOperator(
    task_id='transform_load_weather_data',
    python_callable= transform_load_data
)

    is_weather_api_ready >> extract_weather_data >> transform_load_weather_data
