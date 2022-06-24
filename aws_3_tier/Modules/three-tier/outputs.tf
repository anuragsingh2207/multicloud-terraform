output "nginxip" {
  value = aws_instance.nginx.public_ip
}

output "tomcat1ip" {
  value = aws_instance.tomcat1.public_ip
}


output "tomcat2ip" {
  value = aws_instance.tomcat2.public_ip
}

output "dbendpoint" {
  value = aws_db_instance.db1.endpoint

}