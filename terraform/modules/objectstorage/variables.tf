#
# modules/objectstorage/variables.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/objectstorage_bucket
#

variable "compartment_id" {
    description = "(Required) (Updatable) The ID of the compartment in which to create the bucket."
    type = string    
}

variable "bucket_name" {
    description = "(Required) The name of the bucket. Valid characters are uppercase or lowercase letters, numbers, hyphens, underscores, and periods. Bucket names must be unique within an Object Storage namespace."
    type = string
}

variable "bucket_namespace" {
    description = "(Required) The Object Storage namespace used for the request."
    type = string
}

variable "access_type" {
    description = "(Optional) (Updatable) The type of public access enabled on this bucket."
    type = string
    default = "NoPublicAccess"
}

variable "storage_tier" {
    description = "(Optional) The type of storage tier of this bucket (Standard or Archive)."
    type = string
    default = "Standard"

    validation {
        condition = contains(["Standard", "Archive"], var.storage_tier)
        error_message = "The storage_tier must be Standard or Archive."
    }    
}

variable "versioning" {
    description = "(Optional) (Updatable) Set the versioning status on the bucket (Enabled or Disabled). Objects in a version enabled bucket are protected from overwrites and deletions."
    type = string
    default = "Disabled"

    validation {
        condition = contains(["Enabled", "Disabled"], var.versioning)
        error_message = "The versioning must be Enabled or Disabled."
    }    
} 