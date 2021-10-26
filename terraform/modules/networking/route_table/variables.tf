#
# modules/networking/route_table/variables.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_route_table
#

variable "compartment_id" {
    description = "(Required) (Updatable) The OCID of the compartment to contain the route table."
    type = string    
}

variable "display_name" {
    description = "(Optional) (Updatable) A user-friendly name."
    type = string
    default = "rtb"
}

variable "vcn_id" {
    description = "(Required) The OCID of the VCN the route table belongs to."
    type = string    
}

variable "route_rules" {
    description = "(Optional) (Updatable) The collection of rules used for routing destination IPs to network devices."

    type = list(object({
        destination       = string
        destination_type  = string
        network_entity_id = string
        description       = string
    }))
    
    default = null    
}