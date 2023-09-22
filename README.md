# User Data Processing Pipeline with Apache Airflow

![Airflow Logo](https://upload.wikimedia.org/wikipedia/commons/d/de/AirflowLogo.png)

## Overview

This project demonstrates the use of Apache Airflow to create a data processing pipeline that extracts user data from an external API, processes it, and stores it in a SQLite database. The pipeline includes tasks for data extraction, transformation, and loading (ETL), and it is designed to run on a daily schedule.

## Features

- Utilizes Apache Airflow, an open-source workflow automation platform, to create and manage the ETL pipeline.
- Extracts user data from the [Random User Generator API](https://randomuser.me/api/).
- Processes the retrieved JSON data, extracting relevant user information (first name, last name, country, username, password, and email) and normalizing it into a structured format.
- Creates an SQLite database table to store the processed user data.
- Executes the ETL pipeline on a daily basis with the option to disable catch-up to prevent backfilling.

## Installation

To get started with the User Data Processing Pipeline, follow these steps:

1. **Install Docker:** Ensure you have Docker installed on your system. If not, you can download and install it from the [official Docker website](https://www.docker.com/get-started).

2. **Create a Project Folder:** Create a folder named `materials` in your `Documents` directory. This folder will be used for project materials.

3. **Download Docker Compose File:** Download the `docker-compose.yml` file provided in this repository and place it in the `materials` folder.

4. **Create an Environment File:** In the `materials` folder, create a new file named `.env`. Add the following lines to the `.env` file:

   ```plaintext
   AIRFLOW_IMAGE_NAME=apache/airflow:2.4.2
   AIRFLOW_UID=50000
Save the file.

Start Apache Airflow: Open your terminal or command prompt, navigate to Documents/materials, and run the command:

`docker-compose up -d`

This command starts Apache Airflow using Docker.

Access Airflow Web UI: Open your web browser and go to `localhost:8080` to access the Apache Airflow web interface.

Congratulations! You've successfully installed and set up Apache Airflow for the User Data Processing Pipeline.

