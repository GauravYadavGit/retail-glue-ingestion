import boto3
import os

glue = boto3.client("glue")


def lambda_handler(event, context):
    # S3 event structure
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    glue.start_job_run(
        JobName=os.environ["GLUE_JOB_NAME"],
        Arguments={"--SOURCE_BUCKET": bucket, "--SOURCE_KEY": key},
    )

    return {"status": "glue_started", "bucket": bucket, "key": key}
