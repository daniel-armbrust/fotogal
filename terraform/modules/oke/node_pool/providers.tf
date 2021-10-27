#
# modules/oke/node_pool/providers.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs
#

terraform {
  required_providers {      
    oci = {
      source = "hashicorp/oci"
    }
  }
}