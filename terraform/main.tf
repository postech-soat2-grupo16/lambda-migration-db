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

# ## Resource para instalar as deps
# resource "null_resource" "pip_install" {
#   triggers = {
#     shell_hash = "${sha256(file("../src/code/requirements.txt"))}"
#   }

#   provisioner "local-exec" {
#     command = "python -m pip install -r ../src/code/requirements.txt -t ../src/code"
#   }
# }

# ## Cria o .zip da layer
# data "archive_file" "layer" {
#   type        = "zip"
#   source_dir  = "../src/layer"
#   output_path = "../src/layer/layer.zip"
#   depends_on  = [null_resource.pip_install]
# }

# ## Config Layer
# resource "aws_lambda_layer_version" "layer" {
#   layer_name          = "test-layer"
#   filename            = data.archive_file.layer.output_path
#   source_code_hash    = data.archive_file.layer.output_base64sha256
#   compatible_runtimes = ["python3.9", "python3.8", "python3.7", "python3.6"]
# }

## .zip do código
data "archive_file" "code" {
  type        = "zip"
  source_dir  = "../src/code"
  output_path = "../src/code/code.zip"
}

## Infra lambda
resource "aws_lambda_function" "lambda" {
  function_name    = "lambda-migration-db"
  handler          = "lambda.main"
  runtime          = "python3.8"
  filename         = data.archive_file.code.output_path
  source_code_hash = data.archive_file.code.output_base64sha256
  role             = var.lambda_execution_role
  timeout          = 120
  #layers           = [aws_lambda_layer_version.layer.arn]
  description = "Lamda para executar scripts DB"

  vpc_config {
    subnet_ids         = [var.subnet_a, var.subnet_b]
    security_group_ids = [var.security_group_lambda]
  }

  environment {
    variables = {
      "RDS_ENDPOINT" = var.rds_endpoint
      "DB_NAME"      = var.rds_db_name
      "BUCKET_NAME"  = var.bucket_name
      "SECRET_NAME"  = var.secret_name
    }
  }
}
