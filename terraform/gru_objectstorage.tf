#
# gru_objectstorage.tf
#

#-------------------
# Object Storage
#-------------------
module "gru_objectstorage_bucket" {
    source = "./modules/objectstorage"
   
    providers = {
       oci = oci.gru
    }

    compartment_id = var.compartment_id
    bucket_name = "fotogal_bucket_images"
    bucket_namespace = local.gru_objectstorage_ns        
}
    