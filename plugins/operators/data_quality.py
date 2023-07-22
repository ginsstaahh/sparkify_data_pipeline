from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    """A custom operator designed to check data integrity and insertion 
    for fact and dimension tables in Redshift.
    
    Args:
        BaseOperator - Abstract base class for all operators
    """
    
    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self, redshift_conn_id="", tables="", *args, **kwargs):
        """Constructor used to set default values for DataQualityOperator instances.
        
        Args:
            redshift_conn_id {string} - id used to connect to redshift
            tables {list} - tables to be quality checked
        """
        
        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables

    def execute(self, context):
        """Procedures that are executed when Operator task runs
        
        Args:
            context {} - 
        Returns:
            {None}
        """
        redshift_hook = PostgresHook(self.redshift_conn_id)
        self.log.info(f'context type: {type(context)}')
       
        self.log.info('Checking number of records in tables')
        for table in self.tables:
            records = redshift_hook.get_records(f"SELECT COUNT(*) FROM {table}")
            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError(f"Data quality check failed. {table} returned no results")
            num_records = records[0][0]
            if num_records < 1:
                raise ValueError(f"Data quality check failed. {table} contained 0 rows")
            self.log.info(f"Data quality on table {table} check passed with {records[0][0]} records")