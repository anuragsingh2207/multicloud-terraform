provider "aws" {

  region  = var.aws_region
  profile = "default"

}


resource "aws_instance" "nginx" {
  ami             = var.imageid // ubuntu 18 image id taken from varaiables file
  instance_type   = var.instancetype
  key_name        = var.key
  security_groups = ["${var.sg}"]

  tags = {
    Name = "nginx_server"
  }

  connection {
    user        = "ubuntu"
    host        = self.public_ip
    type        = "ssh"
    port        = "22"
    timeout     = "5m"
    private_key = file(var.private_key_path) # Variable
  }

  provisioner "remote-exec" {

    inline = [
      "sudo apt update",
      "sudo apt install -y nginx",
      "sudo systemctl start nginx",
      "exit 0"
    ]
  }

} // End of Nginx 


resource "aws_instance" "tomcat1" {
  ami             = var.imageid // // ubuntu 18 image id taken from varaiables file
  instance_type   = var.instancetype
  key_name        = var.key
  security_groups = ["${var.sg}"]

  tags = {
    Name = "tomcat1"
  }

  connection {
    user        = "ubuntu"
    host        = self.public_ip
    type        = "ssh"
    port        = "22"
    timeout     = "5m"
    private_key = file(var.private_key_path) # Variable
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt update",
      "sudo apt install -y tomcat8",
      "systemctl start tomcat8",
      "exit 0"
    ]
  }


} // End of Tomcat 


resource "aws_instance" "tomcat2" {
  ami             = var.imageid // ubuntu 18 image id taken from varaiables file
  instance_type   = var.instancetype
  key_name        = var.key
  security_groups = ["${var.sg}"]

  tags = {
    Name = "tomcat2"
  }

  connection {
    user        = "ubuntu"
    host        = self.public_ip
    type        = "ssh"
    port        = "22"
    timeout     = "5m"
    private_key = file(var.private_key_path) # here we need to pass path of private key 
    # file turns path to contents
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt update",
      "sudo apt install -y tomcat8",
      "systemctl start tomcat8",
      "exit 0"
    ]
  }


} // End of Tomcat 


resource "aws_db_instance" "db1" {

  allocated_storage    = 10
  engine               = "mysql"
  engine_version       = "8.0.20"
  instance_class       = "db.t2.micro"
  name                 = "mydb1"
  username             = "admin"
  password             = "admin123"
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true
} // End of RDS 