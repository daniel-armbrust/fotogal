#
# modules/networking/vcn/main.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_vcn
#

resource "oci_core_vcn" "vcn" {
    compartment_id = var.compartment_id
    cidr_blocks = var.cidr_blocks
    display_name = var.display_name
    dns_label = var.dns_label
    is_ipv6enabled = var.is_ipv6enabled
}