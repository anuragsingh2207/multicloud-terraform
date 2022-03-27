
provider google {
 
 credentials = "${file("key.json")}"
 project = "mytestproject082021"
 region = "us-central1"
 zone   = "us-central1-c"
}


resource "google_sql_database_instance" "instance" {
  name   = "my-database-instance-new-test-2"
  database_version = "POSTGRES_11"
  
  settings {
    tier = "db-f1-micro"
    disk_size = "20"
    disk_type = "PD_HDD"
    availability_type = "ZONAL"

    ip_configuration{
    ipv4_enabled = "true"
    }

    backup_configuration{
    enabled = "true"
    start_time = "03:00"
    point_in_time_recovery_enabled = "true"
    location = "us-central1"
   }

   maintenance_window {
   day = 6
   hour = 2
   update_track = "stable"
   }

  }
  
}



resource "google_sql_database" "database2" {
  name     = "my-database-1"
  instance = google_sql_database_instance.instance.name
    provisioner "local-exec" {
       command = <<-EOT
       echo  ${google_sql_database_instance.instance.first_ip_address}
       ./run.sh ${google_sql_database_instance.instance.first_ip_address}
       EOT
	
  }

}

resource "google_sql_user" "user1" {
  name     = "myuser1"
  instance = google_sql_database_instance.instance.name
  password = "changeme"
}