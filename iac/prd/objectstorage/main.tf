//
// iac/prd/objectstorage/main.tf
//

data "oci_objectstorage_namespace" "ns" {
  compartment_id = var.compartment_ocid
}

resource "oci_objectstorage_bucket" "object_storage" {
    count = length(var.private_bucket_list)
    compartment_id = var.compartment_ocid
    
    namespace = data.oci_objectstorage_namespace.ns.namespace        
    name = var.private_bucket_list[count.index]
    access_type = "NoPublicAccess"
}
