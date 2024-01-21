variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "lambda_execution_role" {
  description = "Execution Role Lambda"
  type = string
  sensitive = true
}

variable "vpc_id" {
  type    = string
  default = "vpc-02704242632eb2597"
}

variable "subnet_a" {
  type = string
  default = "subnet-0c485509fe2864438"
}

variable "subnet_b" {
  type = string
  default = "subnet-000064d84790b3f77"
}

variable "bucket_name" {
  type = string
  default = "migrations-script"
}
