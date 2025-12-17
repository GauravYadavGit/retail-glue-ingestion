resource "aws_s3_bucket" "retail_bucket" {
  bucket = var.bucket_name

  tags = {
    Project = "retail-glue-ingestion"
    Owner   = "data-platform"
  }
}

resource "aws_s3_bucket_versioning" "retail_bucket_versioning" {
  bucket = aws_s3_bucket.retail_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "retail_bucket_block" {
  bucket = aws_s3_bucket.retail_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# --------------------------------------------------
# S3 → Lambda notification (raw/orders/)
# --------------------------------------------------
resource "aws_s3_bucket_notification" "raw_orders_trigger_lambda" {
  bucket = aws_s3_bucket.retail_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.trigger_glue.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "raw/orders/"
  }

  depends_on = [
    aws_lambda_permission.allow_s3_invoke
  ]
}

