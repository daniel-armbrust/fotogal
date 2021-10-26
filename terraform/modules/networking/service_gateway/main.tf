#
# modules/networking/service_gateway/main.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_service_gateway
#

resource "oci_core_service_gateway" "service_gateway" {    
    compartment_id = var.compartment_id
    display_name = var.display_name    
    vcn_id = var.vcn_id    
    route_table_id = var.route_table_id

    services {
        service_id = var.service_id
    }
}