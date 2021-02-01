//
// iac/prd/vcn-oke/main.tf
//

variable "compartment_ocid" {}

variable "vcn_display_name" {
    default = "vcn-oke"
}

variable "vcn_dns_label" {
    default = "vcnoke"
}

variable "vcn_cidr_blocks" {
    default = ["10.39.0.0/16"]
}

variable "dhcp_options_display_name" {
    default = "dhcp_vcn-oke"
}

variable "internet_gateway_display_name" {
    default = "igw_vcn-oke"
}

variable "nat_gateway_display_name" {
    default = "natgw_vcn-oke"
}

variable "service_gateway_display_name" {
    default = "srvgw_vcn-oke"
}

// Public Subnet
variable "public_subnet_display_name" {
    default = "subnpub-1_vcn-oke"
}

variable "public_subnet_cidr_block" {
    default = "10.39.1.0/24"
}

variable "public_subnet_dns_label" {
    default = "subnpub1vcnoke"
}

// Private Subnet
variable "private_subnet_display_name" {
    default = "subnprv-1_vcn-oke"
}

variable "private_subnet_cidr_block" {
    default = "10.39.2.0/24"
}

variable "private_subnet_dns_label" {
    default = "subnprv1vcnoke"
}