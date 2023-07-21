# Intro
This project contains an Apache Airflow data pipeline used for transferring data from S3 buckets to a Redshift data warehouse.  The intent of this project is to demonstrate the superb ability to control the process of data transfer by using a data pipeline with Airflow being sufficient for backfilling (transferring data from earlier date times) and monitoring.  The data pipeline consists of a DAG (directed acyclic graph) which puts tasks in sequence so that work is performed smoothly and synchronously.  This project is part of Udacity's Data Engineering Nanodegree where Udacity's sparkify music streaming app stores user data in a data warehouse for analytics.

## Folders and Files
Dags:
	udac_example_dag.py - Airflow DAG consisting of all pipeline tasks and task dependencies
Plugins:
	Helpers:
    	sql_queries.py - Helper file for inserting values into Redshift SQL tables
    Operators:
    - Folder contains Operator classes that instantiate unique tasks
    	data_quality.py - Custom operator to perform quality checks on fact and dimension tables
    	load_dimension.py - Custom operator that loads dimension tables with values
       	load_fact.py - Custom operator that loads fact tables with values
        stage_redshift.py - Operator Copies S3 data to Redshift
create_tables.sql - SQL code for creating tables in Redshift

## Set Up Procedures
Before running the DAG in the Airflow UI, tables need to be created in Redshift.  Create a Redshift instance and run the create_tables.sql code in Redshift's query editor first before running the DAG.

## Using Airflow UI
Airflow can be run locally on a webserver if using a local Airflow installation.  Type into the terminal the command:
airflow webserver
Copy into your web browser of choice the localhost and port used by Airflow to access the webserver
In the webserver, the airflow DAG can be turned on and then triggered to start running tasks.  Monitoring and debugging can be performed when zooming into a specific DAG.

### Prerequisites
If you are on linux, you probably already have python installed
Check to see if your UNIX system has already has python by using the command in your terminal:
python --version

Otherwise, python can be installed for ubuntu or debian linux using the command:
sudo apt-get install python

Airflow can also be installed locally using pip:
https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html