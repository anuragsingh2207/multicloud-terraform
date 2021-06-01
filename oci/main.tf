provider "oci" {

  config_file_profile = "DEFAULT"
  
}

resource "oci_objectstorage_bucket" "test_bucket" {
    
    compartment_id = "ocid1.compartment.oc1..aaaaaaaax2onuepuj6qp2wjlpsmrjefzhy7e5f5krmhsgflzzl7panz5zv6a"
    name = "mytestbucketviaterraform"
    namespace = "bmxhvfhdlsai"

}