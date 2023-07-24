from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):
    """A custom operator designed to load dimension tables in Redshift.
    
    Args:
        BaseOperator - Abstract base class for all operators
    """
    
    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self, destination_table="", redshift_conn_id="", 
                 sql="", truncate=False, *args, **kwargs):
        """Constructor used to set default values for LoadDimensionOperator instances.
        
        Args:
            destination_table {string} - table to insert values into
            redshift_conn_id {string} - id used to connect to redshift
            sql {string} - SQL code to execute insertion
            truncate {bool} - option to truncate existing data before insertion
        """
        
        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.destination_table = destination_table
        self.redshift_conn_id = redshift_conn_id
        self.sql = sql
        self.truncate = truncate

    def execute(self, context):
        """Procedures that are executed when Operator task runs
        
        Args:
            context {dict} - information about the running DAG and its Airflow environment
        Returns:
            {None}
        """
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        if self.truncate:
            self.log.info(f"truncating existing data in {self.destination_table}")
            redshift.run(f"""
                DELETE FROM {self.destination_table};
            """)
        
        self.log.info(f"Loading {self.destination_table} dimension table")
        formatted_sql = f"""
            INSERT INTO {self.destination_table}
            ({self.sql});
        """
        redshift.run(formatted_sql)
        pass
