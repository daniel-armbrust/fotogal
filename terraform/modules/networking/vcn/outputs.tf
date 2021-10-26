#
# modules/networking/vcn/outputs.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_vcn
#

output "id" {
    value = oci_core_vcn.vcn.id
}