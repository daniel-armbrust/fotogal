#
# modules/networking/nat_gateway/outputs.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_nat_gateway
#

output "id" {
    value = oci_core_nat_gateway.nat_gateway.id
}