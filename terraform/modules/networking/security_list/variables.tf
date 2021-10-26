#
# modules/networking/security_list/variables.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_security_list
#

variable "compartment_id" {
    description = "(Required) (Updatable) The OCID of the compartment to contain the security list."
    type = string    
}

variable "display_name" {
    description = "(Optional) (Updatable) A user-friendly name."
    type = string
    default = "secl"
}

variable "vcn_id" {
    description = "(Required) The OCID of the VCN the security list belongs to."
    type = string    
}

variable "egress_security_rules" {
    description = "(Optional) (Updatable) Rules for allowing egress IP packets."
    type = list(object({
        description      = string
        destination      = string
        destination_type = string
        protocol         = string
        stateless        = bool
        dst_min_port     = optional(string)
        dst_max_port     = optional(string)
        src_min_port     = optional(string)
        src_max_port     = optional(string)
        icmp_type        = optional(number)
        icmp_code        = optional(number)
    }))

    default = null
}

variable "ingress_security_rules" {
    description = "(Optional) (Updatable) Rules for allowing ingress IP packets."
    type = list(object({
        description  = string
        source       = string
        source_type  = string
        protocol     = string
        stateless    = bool
        dst_min_port = optional(string)
        dst_max_port = optional(string)
        src_min_port = optional(string)
        src_max_port = optional(string)
        icmp_type    = optional(number)
        icmp_code    = optional(number)
    }))

    default = null
}