#
# modules/networking/service_gateway/outputs.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_service_gateway
#

output "id" {
    value = oci_core_service_gateway.service_gateway.id    
}