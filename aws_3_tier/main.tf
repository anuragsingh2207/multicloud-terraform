module "three-tier" {
  
  source = ".//Modules//three-tier"
  private_key_path = "${var.my_key_path}"
  
  
}

module "security-group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "4.2.0"

  name        = "web-server"
  description = "Allow HTTP/HTTPS traffic"
  vpc_id      = "${var.my_vpc}"

  
  ingress_cidr_blocks = ["0.0.0.0/0"]
}