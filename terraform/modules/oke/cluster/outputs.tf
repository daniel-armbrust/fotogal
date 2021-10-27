#
# modules/oke/cluster/outputs.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/containerengine_cluster
#

output "id" {
    value = oci_containerengine_cluster.oke_cluster.id
}
