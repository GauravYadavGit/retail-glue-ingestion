variable "bucket_name" {
  type        = string
  description = "S3 bucket for retail Glue ingestion"
  default     = "my-retail-glue-demo-ap-south-1"
}


variable "glue_script_path" {
  type        = string
  description = "S3 path to Glue job script"
  default     = "scripts/orders_ingestion_job.py"
}
