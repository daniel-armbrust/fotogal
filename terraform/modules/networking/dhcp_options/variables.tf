#
# modules/networking/dhcp_options/variables.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_dhcp_options
#

variable "compartment_id" {
    description = "(Required) (Updatable) The OCID of the compartment to contain the set of DHCP options."
    type = string    
}

variable "display_name" {
    description = "(Optional) (Updatable) A user-friendly name."
    type = string
    default = "dhcp"
}

variable "vcn_id" {
    description = "(Required) The OCID of the VCN the set of DHCP options belongs to."
    type = string    
}

variable "domain_name_type" {
    description = "(Optional) (Updatable) The search domain name type of DHCP options."
    type = string    
    default = null
}

variable "type" {
    description = "(Required) (Updatable) The specific DHCP option. Either DomainNameServer (for DhcpDnsOption) or SearchDomain (for DhcpSearchDomainOption)."
    type = string
    default = "DomainNameServer"
}

variable "server_type" {
    description = "VcnLocalPlusInternet or CustomDnsServer."
    type = string
    default = "VcnLocalPlusInternet"
}

variable "custom_dns_servers" {
    description = "(Applicable when type=DomainNameServer) (Updatable) If you set serverType to CustomDnsServer specify the IP address of at least one DNS server of your choice (three maximum)."
    type = list(string)
    default = []
}

variable "search_domain_names" {
    description = "(Required when type=SearchDomain) (Updatable) A single search domain name. The OS will append this search domain name to the value being queried."
    type = list(string)
    default = []
}