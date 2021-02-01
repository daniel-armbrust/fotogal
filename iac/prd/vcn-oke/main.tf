//
// iac/prd/vcn-oke/main.tf
//

# VCN
resource "oci_core_vcn" "vcn" {
  compartment_id = var.compartment_ocid    
  cidr_blocks    = var.vcn_cidr_blocks  
  display_name   = var.vcn_display_name
  dns_label      = var.vcn_dns_label
}

# DHCP OPTIONS
resource "oci_core_dhcp_options" "dhcp_options" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.vcn.id
  display_name   = var.dhcp_options_display_name
  
  options {
    type        = "DomainNameServer"
    server_type = "VcnLocalPlusInternet"
  }
  
  options {
    type                = "SearchDomain"
    search_domain_names = ["vcnoke.oraclevcn.com"]
  }
}

# INTERNET GATEWAY
resource "oci_core_internet_gateway" "internet_gateway" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.vcn.id
  display_name   = var.internet_gateway_display_name
}

# NAT GATEWAY
resource "oci_core_nat_gateway" "nat_gateway" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.vcn.id
  display_name   = var.nat_gateway_display_name
}

# SERVICE GATEWAY
resource "oci_core_service_gateway" "service_gateway" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.vcn.id
  display_name   = var.service_gateway_display_name

  services {
     service_id = data.oci_core_services.oci_services.services[0]["id"]
  }
}

# ROUTE TABLE
resource "oci_core_route_table" "rtb_subnprv-1_vcn-oke-prd" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.vcn.id
  display_name   = "rtb_subnprv-1_vcn-oke-prd"

  route_rules {    
    destination       = data.oci_core_services.oci_services.services[0]["cidr_block"]
    destination_type  = "SERVICE_CIDR_BLOCK"
    network_entity_id = oci_core_service_gateway.service_gateway.id    
  }

  route_rules {    
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_nat_gateway.nat_gateway.id
  }
}

# ROUTE TABLE
resource "oci_core_route_table" "rtb_subnpub-1_vcn-oke-prd" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.vcn.id
  display_name   = "rtb_subnpub-1_vcn-oke-prd"

  route_rules {    
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_internet_gateway.internet_gateway.id
  }
}

# SECURITY LIST
resource "oci_core_security_list" "secl-1_subnpub-1_vcn-oke-prd" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.vcn.id
  display_name   = "secl-1_subnpub-1_vcn-oke-prd"
    
  egress_security_rules {   
    destination = "0.0.0.0/0"
    protocol    = "ALL"
    stateless   = false   
  }
  
  // HTTP 80/TCP
  ingress_security_rules {
    protocol  = "6" // tcp
    source    = "0.0.0.0/0"
    stateless = false

    tcp_options {
      source_port_range {
        min = 1024
        max = 65535
      }

      // These values correspond to the destination port range.
      min = 80
      max = 80
    }
  }
  
  // HTTPS 443/TCP
  ingress_security_rules {
    protocol  = "6" // tcp
    source    = "0.0.0.0/0"
    stateless = false

    tcp_options {
      source_port_range {
        min = 1024
        max = 65535
      }

      // These values correspond to the destination port range.
      min = 443
      max = 443
    }
  } 
}

# SECURITY LIST
resource "oci_core_security_list" "secl-1_subnprv-1_vcn-oke-prd" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.vcn.id
  display_name   = "secl-1_subnprv-1_vcn-oke-prd"
  
  egress_security_rules {
    destination = "0.0.0.0/0"
    protocol    = "ALL" 
	  stateless   = false
  }  
 
  ingress_security_rules {   
    source    = "0.0.0.0/0"
     protocol  = "ALL" 
    stateless = false
  }   
}

# SUBNET
resource "oci_core_subnet" "subnpub-1" {
  compartment_id = var.compartment_ocid
  vcn_id = oci_core_vcn.vcn.id  
  cidr_block = var.public_subnet_cidr_block
  display_name = var.public_subnet_display_name
  dns_label = var.public_subnet_dns_label
  security_list_ids = [oci_core_security_list.secl-1_subnpub-1_vcn-oke-prd.id]
  route_table_id = oci_core_route_table.rtb_subnpub-1_vcn-oke-prd.id
  dhcp_options_id = oci_core_dhcp_options.dhcp_options.id
  prohibit_public_ip_on_vnic = false
}

# SUBNET
resource "oci_core_subnet" "subnprv-1" {
  compartment_id = var.compartment_ocid
  vcn_id = oci_core_vcn.vcn.id  
  cidr_block = var.private_subnet_cidr_block
  display_name = var.private_subnet_display_name
  dns_label = var.private_subnet_dns_label
  security_list_ids = [oci_core_security_list.secl-1_subnprv-1_vcn-oke-prd.id]
  route_table_id = oci_core_route_table.rtb_subnprv-1_vcn-oke-prd.id
  dhcp_options_id = oci_core_dhcp_options.dhcp_options.id
  prohibit_public_ip_on_vnic = true
}
