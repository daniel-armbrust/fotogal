#
# modules/nosql/index/outputs.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/nosql_index
#

output "id" {
    value = oci_nosql_index.nosql_index.id
}