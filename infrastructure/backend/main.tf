terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.9.0"
    }
  }

  backend "s3" {
    bucket  = "bucket-pizza-planet"
    key     = "backend-state/terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}

provider "aws" {
  region = "us-east-1"
}

data "external" "sops_secrets" {
  program = ["sops", "-d", "../../credentials.json"]
}

resource "aws_api_gateway_resource" "lambda_api_gateway" {
  rest_api_id = aws_api_gateway_rest_api.api-gateway-rest-api.id
  parent_id   = aws_api_gateway_rest_api.api-gateway-rest-api.root_resource_id
  path_part   = "{proxy+}"
}


resource "aws_api_gateway_rest_api" "api-gateway-rest-api" {
  name = "pizza-planet-backend"
}

resource "aws_api_gateway_method" "api-gateway-method" {
  rest_api_id   = aws_api_gateway_rest_api.api-gateway-rest-api.id
  resource_id   = aws_api_gateway_resource.lambda_api_gateway.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "api-gateway-integration" {
  rest_api_id             = aws_api_gateway_rest_api.api-gateway-rest-api.id
  resource_id             = aws_api_gateway_resource.lambda_api_gateway.id
  http_method             = aws_api_gateway_method.api-gateway-method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.aws-lambda.invoke_arn
}

resource "aws_api_gateway_deployment" "api-gateway-deployment" {
  depends_on = [
    aws_api_gateway_integration.api-gateway-integration
  ]
  rest_api_id = aws_api_gateway_rest_api.api-gateway-rest-api.id
  stage_name  = "v1"
}

resource "aws_lambda_function" "aws-lambda" {
  function_name = "pizza-planet"
  role          = aws_iam_role.iam_for_lambda.arn
  timeout       = 15
  image_uri     = var.pizza-planet-image
  package_type  = "Image"
  environment {
    variables = {
      "database" = data.external.sops_secrets.result["database_uri"],
    }
  }
}

resource "aws_lambda_permission" "lambda_permision" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.aws-lambda.arn
  principal     = "apigateway.amazonaws.com"
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
POLICY
  inline_policy {
    name = "perms"
    policy = jsonencode(
      {
        "Version" : "2012-10-17",
        "Statement" : concat(
          [
            {
              "Effect" : "Allow",
              "Action" : [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
              ],
              "Resource" : "*"
            }
          ]
        )
      }
    )
  }
}

resource "aws_api_gateway_account" "api-gateway-account" {
  cloudwatch_role_arn = aws_iam_role.cloudwatch.arn
}

resource "aws_iam_role" "cloudwatch" {
  name = "api_gateway_cloudwatch_global"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "apigateway.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "cloudwatch" {
  name = "default"
  role = aws_iam_role.cloudwatch.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams",
                "logs:PutLogEvents",
                "logs:GetLogEvents",
                "logs:FilterLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_subnet" "aws-subnet" {
  vpc_id                  = "vpc-057e0edae3c95cb91"
  cidr_block              = "172.31.100.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"

  tags = {
    Name = "pizza-planet"
  }
}

resource "aws_subnet" "aws-subnet-2" {
  vpc_id                  = "vpc-057e0edae3c95cb91"
  cidr_block              = "172.31.102.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1b"

  tags = {
    Name = "pizza-planet"
  }
}

resource "aws_db_subnet_group" "aws-subnet-group" {
  name       = "pizza-planet"
  subnet_ids = [aws_subnet.aws-subnet.id, aws_subnet.aws-subnet-2.id]

  tags = {
    Name = "pizza-planet"
  }
}

resource "aws_security_group" "rds" {
  name   = "security group rds"
  vpc_id = "vpc-057e0edae3c95cb91"

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "pizzaplanet"
  }
}

resource "aws_db_parameter_group" "aws-parameter-group" {
  name   = "pizzaplanet"
  family = "postgres14"

  parameter {
    name  = "log_connections"
    value = "1"
  }
}

resource "aws_internet_gateway" "aws-igw" {
  vpc_id = "vpc-057e0edae3c95cb91"

  tags = {
    Name = "pizzaplanet"
  }
}
resource "aws_route" "aws-route" {
  route_table_id         = "rtb-069fb6d2c168508f8"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.aws-igw.id
}

resource "aws_db_instance" "db-instance-rds" {
  identifier             = "pizzaplanet"
  allocated_storage      = 5
  db_name                = data.external.sops_secrets.result["db_name"]
  engine                 = "postgres"
  engine_version         = "14.3"
  instance_class         = "db.t4g.micro"
  username               = data.external.sops_secrets.result["username"]
  password               = data.external.sops_secrets.result["password"]
  skip_final_snapshot    = true
  db_subnet_group_name   = aws_db_subnet_group.aws-subnet-group.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  parameter_group_name   = aws_db_parameter_group.aws-parameter-group.name
  publicly_accessible    = true
}
