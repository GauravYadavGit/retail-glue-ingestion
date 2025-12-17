resource "aws_glue_job" "orders_ingestion" {
  name     = "glue-orders-ingestion"
  role_arn = aws_iam_role.glue_job_role.arn

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://my-retail-glue-demo-ap-south-1/scripts/orders_ingestion_job.py"
  }

  glue_version = "4.0"

  worker_type       = "G.1X"
  number_of_workers = 2

  default_arguments = {
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-metrics"                   = "true"
  }


  execution_property {
    max_concurrent_runs = 1
  }
}
