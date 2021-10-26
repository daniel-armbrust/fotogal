#
# modules/nosql/table/outputs.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/nosql_table
#

output "id" {
    value = oci_nosql_table.nosql_table.id
}