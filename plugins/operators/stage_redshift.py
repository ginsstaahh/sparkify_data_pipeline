from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    """A custom operator designed to transfer data from S3 and stage in Redshift.
    
    Args:
        BaseOperator - Abstract base class for all operators
    """
    
    ui_color = '#358140'
    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        FORMAT AS JSON '{}'
    """

    @apply_defaults
    def __init__(self, redshift_conn_id="", aws_credentials_id="", 
                 table="", s3_bucket="", s3_key="", json_format="auto", *args, **kwargs):
        """Constructor used to set default values for StageToRedshiftOperator instances.
        
        Args:
            redshift_conn_id {string} - id used to connect to redshift
            aws_credentials_id {string} - security credentials id to verify permission access
            table {string} - table to stage values into
            s3_bucket {string} - directory for where objects are stored in S3
            s3_key {string} - distinctive identifier for an object stored in S3
            json_format {string} - option to define JSON scheme
        """
        
        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.json_format = json_format

    def execute(self, context):
        """Procedures that are executed when Operator task runs
        
        Args:
            context {dict} - information about the running DAG and its Airflow environment
        Returns:
            {None}
        """
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Clearing data from destination Redshift table")
        redshift.run("DELETE FROM {}".format(self.table))

        self.log.info("Copying data from S3 to Redshift")
        rendered_key = self.s3_key.format(**context)
        s3_path = "s3://{}/{}".format(self.s3_bucket, rendered_key)
        formatted_sql = StageToRedshiftOperator.copy_sql.format(
            self.table,
            s3_path,
            credentials.access_key,
            credentials.secret_key,
            self.json_format
        )
        redshift.run(formatted_sql)