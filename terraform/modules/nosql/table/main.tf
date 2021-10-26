#
# modules/nosql/table/main.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/nosql_table
#

resource "oci_nosql_table" "nosql_table" {
    compartment_id = var.compartment_id
    name = var.nosql_table["name"]
    ddl_statement = var.nosql_table["ddl_statement"]

    table_limits {     
        max_read_units = var.nosql_table["read_units"]
        max_storage_in_gbs = var.nosql_table["storage_gbs"]
        max_write_units = var.nosql_table["write_units"]
    }
}