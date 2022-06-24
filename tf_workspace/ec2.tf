provider "aws" {

  region     = "ap-south-1"
  access_key = "ABC"
  secret_key = "XYZ"

}

resource "aws_instance" "myec2" {

  ami           = "ami-123abcdef"
  instance_type = lookup(var.instance_type, terraform.workspace)


}

# Creating map variable for instnace shape for different workspaces
variable "instance_type" {
  type = map(any)

  default = {

    default = "t2.micro"
    dev     = "t2.medium"
    latge   = "t2.large"
  }

}