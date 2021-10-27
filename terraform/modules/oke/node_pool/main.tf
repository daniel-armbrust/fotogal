#
# modules/oke/node_pool/main.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/containerengine_node_pool
#

resource "oci_containerengine_node_pool" "oke_node_pool" {
    compartment_id = var.compartment_id

    name = var.nodepool_name
    cluster_id = var.cluster_id
    
    kubernetes_version = var.k8s_version
    
    node_config_details {
        placement_configs {
            availability_domain = var.nodepool_ad
            subnet_id = var.subnet_id   
        }

        size = var.node_count
    } 

    node_shape = var.node_shape

    node_shape_config {
        memory_in_gbs = var.node_memory_gbs
        ocpus = var.node_ocpus_count
    }

    node_source_details {
        image_id = var.node_image_id
        source_type = var.node_image_source_type
        boot_volume_size_in_gbs = var.node_bootvol_gbs
    }

    ssh_public_key = var.node_ssh_pubkey
}