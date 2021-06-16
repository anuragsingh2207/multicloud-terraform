provider "oci" {

  config_file_profile = "DEFAULT"
  
}


resource "oci_objectstorage_bucket" "test_bucket" {
    
    compartment_id = "${var.comp_id}"
    name = "mytestbucketviatf"
    namespace = "${var.ns}"

}


resource "oci_core_volume" "test_volume" {
    #Required
    compartment_id = "${var.comp_id}"
    #Required
    availability_domain = "${var.ad}"

    #Required
    id = var.volume_source_details_id
    type = var.volume_source_details_type
  
    # Volume details
    size_in_gbs = "20"
    display_name = "mytestblockvolviatf"


}