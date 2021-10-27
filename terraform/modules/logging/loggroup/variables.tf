#
# modules/logging/loggroup/variables.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/logging_log_group
#

variable "compartment_id" {
    description = "(Optional) The OCID of the compartment that the resource belongs to."
    type = string    
}

variable "display_name" {
    description = "(Required) (Updatable) The user-friendly display name of the Log Group."
    type = string
}

variable "description" {
    description = "(Optional) (Updatable) Description for this resource."
    type = string
    default = ""
}
