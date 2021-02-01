//
// iac/prd/oke/outputs.tf
//

data "oci_core_vcns" "vcn" {
  compartment_id = var.compartment_ocid
  filter {
      name = "display_name"
      values = [var.vcn_display_name]
  }
}

data "oci_core_subnets" "public_subnet" {
  compartment_id = var.compartment_ocid
  filter {
      name = "display_name"
      values = [var.lb_subnet_display_name]
  }
}

data "oci_core_subnets" "private_subnet" {
  compartment_id = var.compartment_ocid
  filter {
      name = "display_name"
      values = [var.workers_subnet_display_name]
  }
}

data "oci_containerengine_cluster_option" "cluster_option" {
  cluster_option_id = "all"
}

data "oci_identity_availability_domain" "ad1" {
  compartment_id = var.compartment_ocid
  ad_number = 1
}