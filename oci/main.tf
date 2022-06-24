provider "oci" {

  config_file_profile = "DEFAULT"

}

// Object Storage Bucket
resource "oci_objectstorage_bucket" "test_bucket" {
  compartment_id = var.comp_id
  name           = "mytestbucketviatf"
  namespace      = var.ns
}


resource "oci_core_volume" "test_volume" {
  compartment_id      = var.comp_id
  availability_domain = "rMlR:AP-MUMBAI-1-AD-1"
  size_in_gbs         = "50"
  display_name        = "mytestblockvolviatf"
}

// Compute Instance
resource "oci_core_instance" "test_instance" {
  availability_domain = var.ad
  compartment_id      = var.comp_id
  shape               = var.shape

  create_vnic_details {
    assign_public_ip = "true"
    display_name     = "ds1"
    hostname_label   = "ds1"
    subnet_id        = var.sub
  }

  source_details {
    source_id               = var.img_id
    source_type             = "image"
    boot_volume_size_in_gbs = "50"
  }


  metadata = {
    ssh_authorized_keys = "${file(var.ssh_public_key_file)}"
  }

}


// VCN
resource "oci_core_vcn" "test_vcn" {
  compartment_id = var.comp_id
  cidr_block     = "10.1.0.0/16"
  display_name   = "test_vcn"

}


output "compute_id" {
  value = oci_core_instance.test_instance.id
}

output "compute_public_ip" {
  value = oci_core_instance.test_instance.public_ip
}

output "vcn_id" {
  value = oci_core_vcn.test_vcn.id
}