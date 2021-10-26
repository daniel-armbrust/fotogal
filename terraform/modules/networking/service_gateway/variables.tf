#
# modules/networking/service_gateway/variables.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_service_gateway
#

variable "compartment_id" {
    description = "(Required) (Updatable) The OCID of the compartment to contain the service gateway."
    type = string    
}

variable "display_name" {
    description = "(Optional) (Updatable) A user-friendly name."
    type = string
    default = "sgw"
}

variable "vcn_id" {
    description = "(Required) The OCID of the VCN."
    type = string    
}

variable "route_table_id" {
    description = "(Optional) (Updatable) The OCID of the route table the service gateway will use."
    type = string
    default = null
}

variable "service_id" {
    description = "(Required) (Updatable) The OCID of the Service. This list can be empty if you don't want to enable any Service objects when you create the gateway."
    type = string  
}