import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql.functions import udf
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from transformers import pipeline

# Initialize Glue context