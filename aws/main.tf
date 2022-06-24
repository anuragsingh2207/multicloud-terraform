provider "aws" {

  region  = var.region
  profile = "default"

}

# Creating EC2 instances
resource "aws_instance" "web_server1" {
  ami             = var.imageid
  instance_type   = var.instancetype
  key_name        = var.key
  security_groups = var.sg

  tags = {
    Name = "web_server1"
  }

}

resource "aws_instance" "web_server2" {
  ami             = var.imageid
  instance_type   = var.instancetype
  key_name        = var.key
  security_groups = var.sg

  tags = {
    Name = "web_server2"
  }

}

# Creating a new key pair in AWS using terraform
resource "aws_key_pair" "key1" {
  key_name   = "MUMKEY"
  public_key = var.pub_key
}


#  Creating Security Group (This resource has dependency on vpc vpc1)
resource "aws_security_group" "sg1" {
  name        = "sg1"
  description = "Allow TLS inbound traffic"
  vpc_id      = aws_vpc.vpc1.id

  ingress {
    description = "TLS from VPC"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["${aws_vpc.vpc1.cidr_block}"] # using vpc1 cidr_block output
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_tls"
  }
}


# Creating VPC (This VPC gets created first and then above security group sg1 gets created)
resource "aws_vpc" "vpc1" {
  cidr_block = "10.0.0.0/16"
}


# Creating S3 Bucket with lifecycle rules
resource "aws_s3_bucket" "bucket1" {
  bucket = "my-tf-test-bucket"
  acl    = "private"

  versioning {
    enabled = true
  }

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }

  lifecycle_rule {
    id      = "log"
    enabled = true

    prefix = "log/"

    tags = {
      "rule"      = "log"
      "autoclean" = "true"
    }

    transition {
      days          = 30
      storage_class = "STANDARD_IA" # or "ONEZONE_IA"
    }

    transition {
      days          = 60
      storage_class = "GLACIER"
    }

    expiration {
      days = 90
    }

  }

}

# Creating one more EC2 instance 

resource "aws_instance" "web_server3" {
  ami             = var.imageid
  instance_type   = var.instancetype
  key_name        = var.key
  security_groups = ["${aws_security_group.sg1.name}"] #Resource outputs

  tags = {
    Name = "web_server2"
  }

  connection {
    user        = "ec2-user"
    private_key = file(var.private_key_path) # Variable

  }

}