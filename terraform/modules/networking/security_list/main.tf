#
# modules/networking/security_list/main.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/core_security_list
#

terraform { 
  experiments = [module_variable_optional_attrs]
}

resource "oci_core_security_list" "security_list" {
    compartment_id = var.compartment_id
    vcn_id = var.vcn_id
    display_name = var.display_name

    dynamic "egress_security_rules" {
        iterator = egress_iterator
        for_each = var.egress_security_rules

        content {
           description      = egress_iterator.value["description"]
           destination      = egress_iterator.value["destination"]
           destination_type = egress_iterator.value["destination_type"]
           protocol         = egress_iterator.value["protocol"]
           stateless        = egress_iterator.value["stateless"]

           dynamic "tcp_options" {
              for_each = egress_iterator.value["protocol"] == "6" ? [1] : []

              content {
                  min = egress_iterator.value["dst_min_port"]
                  max = egress_iterator.value["dst_max_port"]

                  source_port_range {
                      min = egress_iterator.value["src_min_port"]
                      max = egress_iterator.value["src_max_port"]
                  }
              }
           }

           dynamic "udp_options" {
              for_each = egress_iterator.value["protocol"] == "17" ? [1] : []

              content {
                  min = egress_iterator.value["dst_min_port"]
                  max = egress_iterator.value["dst_max_port"]

                  source_port_range {
                      min = egress_iterator.value["src_min_port"]
                      max = egress_iterator.value["src_max_port"]
                  }
              }
           }

           dynamic "icmp_options" {
              for_each = egress_iterator.value["protocol"] == "1" ? [1] : []

              content {
                  type = egress_iterator.value["icmp_type"]
                  code = egress_iterator.value["icmp_code"]
              }
           }
        }
    }   

    dynamic "ingress_security_rules" {
        iterator = ingress_iterator
        for_each = var.ingress_security_rules

        content {
           description = ingress_iterator.value["description"]
           source      = ingress_iterator.value["source"]
           source_type = ingress_iterator.value["source_type"]
           protocol    = ingress_iterator.value["protocol"]
           stateless   = ingress_iterator.value["stateless"]

           dynamic "tcp_options" {
              for_each = ingress_iterator.value["protocol"] == "6" ? [1] : []

              content {
                  min = ingress_iterator.value["dst_min_port"]
                  max = ingress_iterator.value["dst_max_port"]

                  source_port_range {
                      min = ingress_iterator.value["src_min_port"]
                      max = ingress_iterator.value["src_max_port"]
                  }
              }
           }

           dynamic "udp_options" {
              for_each = ingress_iterator.value["protocol"] == "17" ? [1] : []

              content {
                  min = ingress_iterator.value["dst_min_port"]
                  max = ingress_iterator.value["dst_max_port"]

                  source_port_range {
                      min = ingress_iterator.value["src_min_port"]
                      max = ingress_iterator.value["src_max_port"]
                  }
              }
           }

           dynamic "icmp_options" {
              for_each = ingress_iterator.value["protocol"] == "1" ? [1] : []

              content {
                  type = ingress_iterator.value["icmp_type"]
                  code = ingress_iterator.value["icmp_code"]
              }
           }
        }
    }
}