variable "aws_region" {
  default = "ap-south-1"
}

# AMI Id
variable "imageid" {
  default = "ami-04bde106886a53080"
}


# Instance Type
variable "instancetype" {
  default = "t2.micro"
}

# Key
variable "key" {
  default = "MUMKEY"
}

#Security Group
variable "sg" {
  type    = string
  default = "DevOpsSG"

}


# Empty Private  Key Path variable ; the value will be passed while running from CLI

variable "private_key_path" {}

variable "vpcid" {

  default = "vpc-ac4ca1c7 " // to be changed default vpc id

}