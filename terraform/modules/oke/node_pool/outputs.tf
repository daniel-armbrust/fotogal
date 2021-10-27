#
# modules/oke/node_pool/outputs.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/containerengine_node_pool
#

output "id" {
    value = oci_containerengine_node_pool.oke_node_pool.id
}
