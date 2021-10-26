#
# modules/networking/internet_gateway/main.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_internet_gateway
#

resource "oci_core_internet_gateway" "internet_gateway" { 
    compartment_id = var.compartment_id
    vcn_id = var.vcn_id   
    enabled = var.enabled    
    display_name = var.display_name        
}