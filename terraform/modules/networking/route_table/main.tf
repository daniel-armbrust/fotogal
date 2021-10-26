#
# modules/networking/route_table/main.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_route_table
#

resource "oci_core_route_table" "route_table" {
    compartment_id = var.compartment_id
    vcn_id = var.vcn_id
    display_name = var.display_name

    dynamic "route_rules" {
        iterator = iterator_route_rules
        for_each = var.route_rules
        content {
            destination = iterator_route_rules.value["destination"]
            destination_type = iterator_route_rules.value["destination_type"]
            network_entity_id = iterator_route_rules.value["network_entity_id"]
            description = iterator_route_rules.value["description"]
        }              
    }
}