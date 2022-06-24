provider "oci" {
  config_file_profile = "DEFAULT"
}

# this is the data source for Oracle Linux 7 images
data "oci_core_images" "ol7_latest" {
  compartment_id = "ocid1.compartment.oc1..aaaaaaaax2onuepuj6qp2wjlpsmrjefzhy7e5f5krmhsgflzzl7panz5zv6a"

  operating_system         = "Oracle Linux"
  operating_system_version = "7.9"
  shape                    = "VM.Standard.E2.1.Micro"
}

# now let's print the image OCID
output "latest_ol7_image" {
  value = data.oci_core_images.ol7_latest.images.0.id
}

resource "oci_core_instance" "some_instance" {
  # oci_ads is another data source looking up names of the ADs in my region
  availability_domain = data.oci_identity_availability_domains.oci_ads.availability_domains.1.name
  compartment_id      = "ocid1.compartment.oc1..aaaaaaaax2onuepuj6qp2wjlpsmrjefzhy7e5f5krmhsgflzzl7panz5zv6a"
  shape               = "VM.Standard.E2.1.Micro"

  source_details {
    source_id   = data.oci_core_images.ol7_latest.images.0.id
    source_type = "image"

  }

}

# now let's print the AD ID
output "some_instance" {
  value = data.oci_identity_availability_domains.oci_ads.availability_domains.1.name
} 