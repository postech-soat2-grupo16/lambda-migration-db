variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "s3_name" {
  description = "S3 Name"
  type = string
  default = "terraform-state-soat"
}

variable "lambda_execution_role" {
  description = "Execution Role Lambda"
  type = string
  sensitive = true
}