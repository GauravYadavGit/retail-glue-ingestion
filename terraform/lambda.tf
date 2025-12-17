resource "aws_lambda_function" "trigger_glue" {
  function_name = "trigger-glue-orders-ingestion"
  role          = aws_iam_role.lambda_role.arn
  handler       = "handler.lambda_handler"
  runtime       = "python3.10"
  timeout       = 30

  filename         = "${path.module}/lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda.zip")

  environment {
    variables = {
      GLUE_JOB_NAME = aws_glue_job.orders_ingestion.name
    }
  }
}

resource "aws_lambda_permission" "allow_s3_invoke" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.trigger_glue.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::my-retail-glue-demo-ap-south-1"
}

