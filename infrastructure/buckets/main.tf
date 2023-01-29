terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.9.0"
    }
  }

  backend "s3" {
    bucket  = "bucket-pizza-planet"
    key     = "bucket-state/terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "s3-bucket" {
  bucket = "bucket-pizza-planet"
}

resource "aws_s3_bucket_acl" "s3-bucket-acl" {
  bucket = aws_s3_bucket.s3-bucket.id
  acl    = "private"
}

resource "aws_s3_bucket" "s3-bucket-sqlite" {
  bucket = "bucket-pizza-planet-sqlite"
}

resource "aws_s3_bucket_acl" "s3-bucket-acl-database" {
  bucket = aws_s3_bucket.s3-bucket-sqlite.id
  acl    = "private"
}

resource "aws_s3_bucket" "s3-bucket-frontend" {
  bucket = "bucket-pizza-planet-frontend"
}

resource "aws_s3_bucket_website_configuration" "s3_website_config" {
  bucket = aws_s3_bucket.s3-bucket-frontend.id
  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "index.html"
  }
}
