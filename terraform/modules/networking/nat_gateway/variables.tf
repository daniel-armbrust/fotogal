#
# modules/networking/nat_gateway/variables.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_nat_gateway
#

variable "compartment_id" {
    description = "(Required) (Updatable) The OCID of the compartment to contain the NAT gateway."
    type = string    
}

variable "display_name" {
    description = "(Optional) (Updatable) A user-friendly name."
    type = string
    default = "ngw"
}

variable "vcn_id" {
    description = "(Required) The OCID of the VCN the gateway belongs to."
    type = string    
}

variable "block_traffic" {
    description = "(Optional) (Updatable) Whether the NAT gateway blocks traffic through it."
    type = bool
    default = false
}

variable "public_ip_id" {
    description = "(Optional) The OCID of the public IP address associated with the NAT gateway. "
    type = string
    default = ""
}