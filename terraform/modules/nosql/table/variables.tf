#
# modules/nosql/table/variables.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/nosql_table
#

variable "compartment_id" {
    description = "(Required) (Updatable) The OCID of the compartment to contain the NoSQL Table."
    type = string    
}

variable "nosql_table" {
    description = "(Optional) NoSQL Database Table properties."

    type = object({
        name = string
        ddl_statement = string
        read_units = string
        write_units = string
        storage_gbs = string
    })

    default = null
}