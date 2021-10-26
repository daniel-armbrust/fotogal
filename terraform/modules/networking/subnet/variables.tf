#
# modules/networking/subnet/variables.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_subnet
#

variable "compartment_id" {
    description = "(Required) (Updatable) The OCID of the compartment to contain the subnet."
    type = string    
}

variable "display_name" {
    description = "(Optional) (Updatable) A user-friendly name."
    type = string
    default = "subnet"
}

variable "vcn_id" {
    description = "(Required) The OCID of the VCN to contain the subnet."
    type = string    
}

variable "dhcp_options_id" {
    description = "(Optional) (Updatable) The OCID of the set of DHCP options the subnet will use."
    type = string
}

variable "dns_label" {
    description = "(Optional) A DNS label for the subnet, used in conjunction with the VNIC's hostname and VCN's DNS label to form a fully qualified domain name (FQDN)."
    type = string
    default = null  
}

variable "cidr_block" {
    description = "(Required) (Updatable) The CIDR IP address range of the subnet."
    type = string
}

variable "ipv6cidr_block" {
    description = "(Optional) (Updatable) Use this to enable IPv6 addressing for this subnet. The VCN must be enabled for IPv6."
    type = string 
    default = null      
}

variable "prohibit_public_ip_on_vnic" {
    description = "(Optional) Whether VNICs within this subnet can have public IP addresses."
    type = bool
    default = true
}

variable "route_table_id" {
    description = "(Optional) (Updatable) The OCID of the route table the subnet will use."
    type = string    
}

variable "security_list_ids" {
    description = "(Optional) (Updatable) The OCIDs of the security list or lists the subnet will use."
    type = list(string) 
}