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

variable "rds_endpoint" {
  description = "rds endpoint"
  type = string
  sensitive = true
}

variable "rds_db_name" {
  description = "rds db name"
  type = string
  sensitive = true
}

variable "subnet_a" {
  type = string
  default = "value"
}

variable "subnet_b" {
  type = string
  default = "value"
}

variable "security_group_lambda" {
  type = string
  default = "value"
}

variable "bucket_name" {
  type = string
  default = "terraform-state-soat"
}

variable "secret_name" {
  type = string
  sensitive = true
}