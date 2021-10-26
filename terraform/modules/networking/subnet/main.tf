#
# modules/networking/subnet/main.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_subnet
#

resource "oci_core_subnet" "subnet_with_dnslabel_ipv6block" {
    count = var.dns_label != null && var.ipv6cidr_block != null ? 1 : 0

    compartment_id = var.compartment_id
    vcn_id = var.vcn_id
    dhcp_options_id = var.dhcp_options_id
    route_table_id = var.route_table_id
    security_list_ids = var.security_list_ids

    display_name = var.display_name    
    dns_label = var.dns_label
    cidr_block = var.cidr_block
    ipv6cidr_block = var.ipv6cidr_block
    prohibit_public_ip_on_vnic = var.prohibit_public_ip_on_vnic
}

resource "oci_core_subnet" "subnet_with_dnslabel" {
    count = var.dns_label != null && var.ipv6cidr_block == null ? 1 : 0

    compartment_id = var.compartment_id
    vcn_id = var.vcn_id
    dhcp_options_id = var.dhcp_options_id
    route_table_id = var.route_table_id
    security_list_ids = var.security_list_ids

    display_name = var.display_name    
    dns_label = var.dns_label
    cidr_block = var.cidr_block    
    prohibit_public_ip_on_vnic = var.prohibit_public_ip_on_vnic
}

resource "oci_core_subnet" "subnet_with_ipv6block" {
    count = var.dns_label == null && var.ipv6cidr_block != null ? 1 : 0

    compartment_id = var.compartment_id
    vcn_id = var.vcn_id
    dhcp_options_id = var.dhcp_options_id
    route_table_id = var.route_table_id
    security_list_ids = var.security_list_ids

    display_name = var.display_name    
    ipv6cidr_block = var.ipv6cidr_block
    cidr_block = var.cidr_block    
    prohibit_public_ip_on_vnic = var.prohibit_public_ip_on_vnic
}

resource "oci_core_subnet" "subnet" {
    count = var.dns_label == null && var.ipv6cidr_block == null ? 1 : 0

    compartment_id = var.compartment_id
    vcn_id = var.vcn_id
    dhcp_options_id = var.dhcp_options_id
    route_table_id = var.route_table_id
    security_list_ids = var.security_list_ids

    display_name = var.display_name        
    cidr_block = var.cidr_block    
    prohibit_public_ip_on_vnic = var.prohibit_public_ip_on_vnic
}