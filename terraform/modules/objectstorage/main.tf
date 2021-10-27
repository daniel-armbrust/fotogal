#
# modules/objectstorage/main.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/objectstorage_bucket
#

resource "oci_objectstorage_bucket" "objectstorage_bucket" {    
    compartment_id = var.compartment_id
    name = var.bucket_name
    namespace = var.bucket_namespace
    access_type = var.access_type
    storage_tier = var.storage_tier
    versioning = var.versioning
}