//
// iac/prd/objectstorage/variables.tf
//

variable "compartment_ocid" {}

variable "private_bucket_list" {    
    default = ["fotogal_bucket_images"]
}