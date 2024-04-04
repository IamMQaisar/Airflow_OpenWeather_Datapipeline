## Airflow OpenWeather Data Pipeline

<img width="930" alt="image" src="https://github.com/IamMQaisar/Airflow_OpenWeather_Datapipeline/assets/130001453/fa974ee3-d152-4d98-84eb-901cce404049">

<img width="935" alt="image" src="https://github.com/IamMQaisar/Airflow_OpenWeather_Datapipeline/assets/130001453/aaa1fc4a-1139-4dba-b2fa-e5039522ce1d">

This repository contains a simple Apache Airflow DAG for fetching weather data from the OpenWeather API and storing it in AWS S3.

### Setup Instructions

1. **Enable Windows Subsystem for Linux (WSL)** and **Virtualization**:
   - Go to `Control Panel/Program and Feature` and enable these features.

2. **Install Ubuntu from Microsoft Store**:
   - Set a username and password during installation.

3. **Set Up Ubuntu**:
   - Open Ubuntu using `wsl` command or directly from the start menu.
   - Run the following commands:
     ```bash
     sudo apt update
     sudo apt install python3-pip
     sudo apt install python3.10-venv
     python3 -m venv airflow-venv
     ```
   - Activate the virtual environment:
     - For Linux:
       ```bash
       source airflow-venv/bin/activate
       ```
     - For Windows:
       ```bash
       .\airflow-venv\Scripts\activate
       ```
   - Install required Python packages:
     ```bash
     pip install pandas s3fs apache-airflow
     ```

4. **Start Airflow**:
   ```bash
   airflow standalone
   ```
   - Open a new tab and go to `Public IPv4 DNS:8080`.
   - Navigate to Admin > Connections and add a new connection with the following details:
     - `http_conn_id`
     - `HTTP`
     - Your OpenWeather API endpoint

5. **Configure Airflow**:
   - Create a `dags` directory in Airflow.
   - Create or import the `weather_dag.py` file provided in this repository.
   - Edit `airflow.cfg` to set the DAG directory.

6. **AWS Setup**:
   - Install AWS CLI:
     ```bash
     sudo apt install awscli
     ```
   - Set up security credentials:
     ```bash
     aws configure
     ```
     Follow the prompts and enter your AWS access key ID, secret access key, and region.
   - Run the following command to get a session token:
     ```bash
     aws sts get-session-token
     ```

### DAG Code

The DAG code `weather_dag.py` included in this repository fetches weather data from the OpenWeather API, transforms it, and loads it into AWS S3.

### Contact Information

For any questions or concerns, please contact [itisqaisar@gmail.com](mailto:itisqaisar@gmail.com).
