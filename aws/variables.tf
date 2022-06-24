# Region

variable "region" {

  default = "ap-south-1"
}

# AMI Id
variable "imageid" {

  default = "ami-0bfea82e3463aabec"

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

  default = ["DevOpsSG"]

}


# Public Key
variable "pub_key" {

  default = ""

}