provider "aws" {
  region = var.aws_region
}

#Configuração do Terraform State
terraform {
  backend "s3" {
    bucket = "terraform-state-soat"
    key    = "infra-lambda-migration/terraform.tfstate"
    region = "us-east-1"

    dynamodb_table = "terraform-state-soat-locking"
    encrypt        = true
  }
}

## .zip do código
data "archive_file" "code" {
  type        = "zip"
  source_dir  = "../src/code"
  output_path = "../src/code/code.zip"
}

#Security Group Lambda Migration
resource "aws_security_group" "security_group_migration_lambda" {
  name_prefix = "security_group_migration_lambda"
  description = "SG for migration Lambda"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    infra   = "lambda"
    service = "migration"
    Name    = "security_group_migration_lambda"
  }
}

## Infra lambda
resource "aws_lambda_function" "migration_lambda" {
  function_name    = "lambda-migration-db"
  handler          = "lambda.main"
  runtime          = "python3.8"
  filename         = data.archive_file.code.output_path
  source_code_hash = data.archive_file.code.output_base64sha256
  role             = var.lambda_execution_role
  timeout          = 120
  description      = "Lambda para executar scripts DB"

  vpc_config {
    subnet_ids         = [var.subnet_a, var.subnet_b]
    security_group_ids = [aws_security_group.security_group_migration_lambda.id]
  }

  environment {
    variables = {
      "BUCKET_NAME"  = var.bucket_name
    }
  }
}
