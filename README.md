# Intro
This project contains an Apache Airflow data pipeline used for transferring data from S3 buckets to a Redshift data warehouse.  The intent of this project is to demonstrate the ability to control the process of data transfer by using a data pipeline with Airflow.  Airflow is also used for backfilling (transferring data from earlier date times) and monitoring.  The data pipeline consists of a DAG (directed acyclic graph) which puts tasks in sequence so that work is performed smoothly and synchronously.  This project is part of Udacity's Data Engineering Nanodegree where Udacity's sparkify music streaming app stores user data in a data warehouse for analytics.

## Folders and Files
* Dags:
	* udac_example_dag.py - Airflow DAG consisting of all pipeline tasks and task dependencies
* Plugins:
	* Helpers:
 		* sql_queries.py - Helper file for inserting values into Redshift SQL tables
    * Operators:
    * i. Folder contains Operator classes that instantiate unique tasks
    	* data_quality.py - Custom operator to perform quality checks on fact and dimension tables
    	* load_dimension.py - Custom operator that loads dimension tables with values
       	* load_fact.py - Custom operator that loads fact tables with values
        * stage_redshift.py - Operator Copies S3 data to Redshift
* create_tables.sql - SQL code for creating tables in Redshift

## Set Up Procedures
This project uses a shell script in Udacity's project workspace and to access the Airflow UI.  To use a local installation, Airflow can be installed using pip (https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html)

Before running the DAG in the Airflow UI, tables need to be created in Redshift.  Create a Redshift instance and run the create_tables.sql code in Redshift's query editor first before running the DAG:
![alt text](screenshots/aws_query.png?raw=true)

## Using Airflow UI
In the webserver, connections need to be set up under Admin to access Redshift.  This is done by creating connections for Amazon Web Services and Postgres with the following information:
![alt text](screenshots/connection-aws-credentials.png?raw=true)
![alt text](screenshots/connection-redshift.png?raw=true)
The airflow DAG can be turned on and then triggered to start running tasks.  Monitoring and debugging can be performed when zooming into a specific DAG's tree or graph view:
![alt text](screenshots/airflow_tree_view.png?raw=true)
