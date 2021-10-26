#
# modules/networking/dhcp_options/outputs.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_dhcp_options
#

output "id" {       
    value = join("", oci_core_dhcp_options.dhcp_search_domain_names.*.id, oci_core_dhcp_options.dhcp_default.*.id, oci_core_dhcp_options.dhcp_custom_dnsservers.*.id)
}