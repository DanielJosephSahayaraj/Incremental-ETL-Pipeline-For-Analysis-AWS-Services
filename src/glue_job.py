import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Initialize Glue context
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read from S3
source_df = glueContext.create_dynamic_frame.from_catalog(
    database="spotify_db",
    table_name="playlists"
)

# Transform: Extract relevant fields
transformed_df = source_df.apply_mapping([
    ('playlist_id', 'string', 'playlist_id', 'string'),
    ('name', 'string', 'name', 'string'),
    ('description', 'string', 'description', 'string'),
    ('tracks', 'array', 'tracks', 'array'),
    ('artists', 'array', 'artists', 'array')
])

# Write to Redshift
glueContext.write_dynamic_frame.from_options(
    frame=transformed_df,
    connection_type="redshift",
    connection_options={
        "url": "jdbc:redshift://your-redshift-cluster:5439/spotify_db",
        "dbtable": "playlists",
        "user": "your-username",
        "password": "your-password",
        "redshiftTmpDir": "s3://your-bucket/temp/"
    }
)

job.commit()