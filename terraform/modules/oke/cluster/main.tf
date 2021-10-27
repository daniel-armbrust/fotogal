#
# modules/oke/cluster/main.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/containerengine_cluster
#

resource "oci_containerengine_cluster" "oke_cluster" {
    compartment_id = var.compartment_id

    name = var.cluster_name
    kubernetes_version = var.k8s_version    

    vcn_id = var.vcn_id

    endpoint_config {    
        is_public_ip_enabled = var.is_public_ip_enabled       
        subnet_id = var.subnet_id
    }
    
    options {    
        kubernetes_network_config {
            pods_cidr = var.pods_cidr
            services_cidr = var.services_cidr
        }

        add_ons {
            is_kubernetes_dashboard_enabled = var.dashboard_enabled
            is_tiller_enabled = var.tiller_enabled
        }

        admission_controller_options {
             is_pod_security_policy_enabled = var.pod_secpol_enabled
        }

        service_lb_subnet_ids = var.lb_subnet_ids
    }  
}