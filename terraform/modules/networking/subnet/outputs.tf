#
# modules/networking/subnet/outputs.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_subnet
#

output "id" {
    value = join("", oci_core_subnet.subnet_with_dnslabel_ipv6block.*.id, oci_core_subnet.subnet_with_dnslabel.*.id, oci_core_subnet.subnet_with_ipv6block.*.id, oci_core_subnet.subnet.*.id)
}

output "cidr_block" {
    value = join("", oci_core_subnet.subnet_with_dnslabel_ipv6block.*.cidr_block, oci_core_subnet.subnet_with_dnslabel.*.cidr_block, oci_core_subnet.subnet_with_ipv6block.*.cidr_block, oci_core_subnet.subnet.*.cidr_block)
}