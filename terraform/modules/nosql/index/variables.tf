#
# modules/nosql/index/variables.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/nosql_index
#

variable "compartment_id" {
    description = "The OCID of the NoSQL Table's compartment."
    type = string    
}

variable "column_name" {
    description = "(Required) The name of a column to be included as an index key."
    type = string
}

variable "index_name" {
    description = "(Required) Index name."
    type = string
}

variable "table_name_or_id" {
    description = "(Required) A table name within the compartment, or a table OCID."
    type = string
}