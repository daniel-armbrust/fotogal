#
# modules/nosql/index/main.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/nosql_index
#

resource "oci_nosql_index" "nosql_index" {
    compartment_id = var.compartment_id

    name = var.index_name
    table_name_or_id = var.table_name_or_id

    keys {
        column_name = var.column_name        
    }
}