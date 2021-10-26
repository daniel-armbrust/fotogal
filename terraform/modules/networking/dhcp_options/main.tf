#
# modules/networking/dhcp_options/main.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_dhcp_options
#

#
# VCN Local with Internet + custom SearchDomain
#
resource "oci_core_dhcp_options" "dhcp_search_domain_names" {
    count = var.server_type == "VcnLocalPlusInternet" && length(var.search_domain_names) > 0 ? 1 : 0

    compartment_id = var.compartment_id
    vcn_id = var.vcn_id
    display_name = var.display_name
    
    options {
        type = "DomainNameServer"
        server_type = "VcnLocalPlusInternet"
    }

    options {
        type = "SearchDomain"
        search_domain_names = var.search_domain_names
    }
}

#
# VCN Local with Internet
#
resource "oci_core_dhcp_options" "dhcp_default" {
    count = var.server_type == "VcnLocalPlusInternet" && length(var.search_domain_names) <= 0 ? 1 : 0

    compartment_id = var.compartment_id
    vcn_id = var.vcn_id
    display_name = var.display_name
    
    options {
        type = "DomainNameServer"
        server_type = "VcnLocalPlusInternet"
    }
}

#
# Custom DNS Server
#
resource "oci_core_dhcp_options" "dhcp_custom_dnsservers" {
    count = var.server_type == "CustomDnsServer" ? 1 : 0

    compartment_id = var.compartment_id
    vcn_id = var.vcn_id
    display_name = var.display_name
    
    options {
        type = "DomainNameServer"
        server_type = "CustomDnsServer"
        custom_dns_servers = var.custom_dns_servers
    }

    options {
        type = "SearchDomain"
        search_domain_names = var.search_domain_names
    }
}