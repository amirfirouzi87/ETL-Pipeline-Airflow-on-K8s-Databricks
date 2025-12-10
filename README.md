After successfully deploying Apache Airflow on Kubernetes,here you can find the complete guideline(https://medium.com/@amirfiroozi87/deploying-apache-airflow-on-kubernetes-a-step-by-step-guide-c49339584518), I decided to create an ETL pipeline using that infrastructure.
Here is what happens step-by-step :
1. Metadata of video's of a Youtube channel is extracted and saved into a JSON file.
2. The JSON file is uploaded to AWS S3.
3. In Databricks, JSON file in AWS S3 is read and saved in delta format in a managed database.
4. Loaded data is cleaned, transformed and written as stream.
5. Apache Airflow is scheduled to be run hourly so that videos new metadata is added to the previous data and number of Views for example can be monitored. 

# YouTube Analytics ETL: Airflow on Kubernetes & Databricks

This is a complete project that grabs data from a YouTube channel, saves it to AWS S3, and then uses Databricks to clean and process it.

The cool part is that **Apache Airflow (running on Kubernetes)** manages the whole schedule, but **Databricks** does the heavy work.

> **Read the Guide:** If you want to know how I set up the infrastructure, check out my article: [Deploying Apache Airflow on Kubernetes: A Step-by-Step Guide](https://medium.com/@amirfiroozi87/deploying-apache-airflow-on-kubernetes-a-step-by-step-guide-c49339584518).

---

## How it Works



I separated the "manager" (Airflow) from the "worker" (Databricks) to make the system better:

1.  **Get Data (Airflow):** A Python script uses the YouTube API to get video details like views, likes, and duration.
2.  **Save Data (AWS S3):** It saves the raw data as a JSON file in an S3 bucket.
3.  **Load Data (Databricks - Bronze):** Spark reads the JSON file from S3 and adds it to a raw table.
4.  **Clean Data (Databricks - Silver):** A Streaming job cleans the data, fixes the time format, and saves it to a final table.

---

## The Pipeline Steps

### 1. Airflow Manager (`yt_etl_dag.py`)
The pipeline runs every hour (`@hourly`). Here is what the tasks do:
* `get_playlist_id`: Finds the "Uploads" playlist for the channel.
* `get_video_metadata`: Goes through the playlist to find all Video IDs.
* `extract_video_data`: Gets the full details for the videos in batches of 50.
* `save_to_json_upload_s3`: Saves the data to a local file and uploads it to S3 (`youtubeetl852147`).
* `run_databricks_job`: Tells Databricks to start the Spark job and tells it which file to process (`p_file_name`).

### 2. Loading Data: S3 to Delta (`1.Read_File_from_S3.ipynb`)
* **Security:** I use Databricks Secrets (`awscredentials`) so I don't have to write passwords in the code.
* **Raw Table:** It adds the data to the `yt_vids_data.raw` table.

### 3. Cleaning & Logic (`2.Transform_ingested_data.ipynb`)
* **Fixing Types:** It changes things like `view_count` to numbers and `published_at` to timestamps.
* **Fixing Time:** YouTube uses a weird time format (like `PT15M33S`). I used Regex code to turn that into normal hours, minutes, and seconds (`HH:MM:SS`).
* **Smart Streaming:** I use Spark Structured Streaming with `.trigger(availableNow=True)`.
    * *Why?* This processes all the new data at once and then turns off. It saves money because the cluster doesn't stay on all the time.

---

## Tools I Used

* **Manager:** Apache Airflow 3.x (on Kubernetes)
* **Processing:** Databricks (Spark / Delta Lake)
* **Storage:** AWS S3
* **Data Source:** YouTube Data API v3
* **Coding:** Python 3, PySpark

---

## How to Set Up

### 1. Airflow Settings
Go to the Airflow UI and add these:
* **Variable** `API_KEY`: Your YouTube API Key.
* **Connection** `s3_conn`: Select "Amazon Web Services".
* **Connection** `databricks_conn`: Put in your Databricks Host url and Token.

### 2. Databricks Secrets
Run these commands in the Databricks CLI to handle your AWS keys safely:
```bash
databricks secrets create-scope --scope awscredentials
databricks secrets put --scope awscredentials --key awskey
databricks secrets put --scope awscredentials --key awssecret
```

### 3. S3 Bucket Policy
Ensure your S3 bucket (youtubeetl852147) allows access from the IAM user configured in Databricks.