#
# modules/networking/route_table/outputs.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_route_table
#

output "id" {
    value = oci_core_route_table.route_table.id
}