//
// iac/prd/oke/main.tf
//

resource "oci_containerengine_cluster" "containerengine_cluster" {  
  compartment_id = var.compartment_ocid
  kubernetes_version = var.kubernetes_version
  name = var.cluster_name
  vcn_id = lookup(data.oci_core_vcns.vcn.virtual_networks[0], "id")
  
  options {
    service_lb_subnet_ids = [lookup(data.oci_core_subnets.public_subnet.subnets[0], "id")]

    add_ons {    
      is_kubernetes_dashboard_enabled = true
      is_tiller_enabled = true
    }

    admission_controller_options {      
      is_pod_security_policy_enabled = false
    }

    kubernetes_network_config {      
      pods_cidr = var.pods_cidr_block
      services_cidr = var.service_cidr_block
    }
  }
}

resource "oci_containerengine_node_pool" "node_pool" {  
  cluster_id = oci_containerengine_cluster.containerengine_cluster.id
  compartment_id = var.compartment_ocid
  kubernetes_version = var.kubernetes_version
  name = var.node_pool_name  
  
  node_config_details {
     placement_configs {
         availability_domain = data.oci_identity_availability_domain.ad1.name
         subnet_id = lookup(data.oci_core_subnets.private_subnet.subnets[0], "id")
     }   
     
     size = var.node_pool_shape_quantity  
  }

  node_shape = "VM.Standard.E3.Flex"  

  node_shape_config {
    ocpus = var.node_pool_shape_ocpus
    memory_in_gbs = var.node_pool_shape_mem_in_gbs
  }

  node_source_details {    
    image_id = var.image_ocid
    source_type = "IMAGE"
    boot_volume_size_in_gbs = var.node_pool_shape_bootvol_in_gbs
  } 
}