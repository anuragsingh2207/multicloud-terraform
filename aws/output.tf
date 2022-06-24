# Using outputs to display the IP of EC2 instance named one
output "public_ip" {

  value = aws_instance.web_server1.public_ip
}

output "private_ip" {

  value = aws_instance.web_server1.private_ip
}
