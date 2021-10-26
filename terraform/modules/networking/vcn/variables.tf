#
# modules/networking/vcn/variables.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_vcn
#

variable "compartment_id" {
    description = "(Required) (Updatable) The OCID of the compartment to contain the VCN."
    type = string    
}

variable "cidr_blocks" {
    description = "(Optional) (Updatable) The list of one or more IPv4 CIDR blocks for the VCN"
    type = list(string)    
}

variable "display_name" {
    description = "(Optional) (Updatable) A user-friendly name."
    type = string
    default = "vcn"
}

variable "dns_label" {
    description = "(Optional) A DNS label for the VCN."
    type = string
}

variable "is_ipv6enabled" {
    description = "(Optional) Whether IPv6 is enabled for the VCN."
    type = bool
    default = false
}