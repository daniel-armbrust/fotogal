#
# modules/networking/route_table/main.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_nat_gateway
#

resource "oci_core_nat_gateway" "nat_gateway" {
    compartment_id = var.compartment_id
    vcn_id = var.vcn_id
    display_name = var.display_name
    block_traffic = var.block_traffic
    public_ip_id = var.public_ip_id    
}