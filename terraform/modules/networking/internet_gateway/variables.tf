#
# modules/networking/internet_gateway/variables.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_internet_gateway
#

variable "compartment_id" {
    description = "(Required) (Updatable) The OCID of the compartment to contain the internet gateway."
    type = string    
}

variable "display_name" {
    description = "(Optional) (Updatable) A user-friendly name."
    type = string
    default = "igw"
}

variable "enabled" {
    description = "(Optional) (Updatable) Whether the gateway is enabled upon creation."
    type = bool
    default = true
}

variable "vcn_id" {
    description = "(Required) The OCID of the VCN the internet gateway is attached to."
    type = string    
}