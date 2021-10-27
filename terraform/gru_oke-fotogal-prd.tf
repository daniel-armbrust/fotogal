#
# gru_oke-fotogal-prd.tf
#

#-------------------
# OKE Fotogal
#-------------------
module "gru_oke-cluster-fotogal_prd" {
    source = "./modules/oke/cluster"
   
    providers = {
       oci = oci.gru
    }
   
    compartment_id = var.compartment_id

    vcn_id = module.gru_vcn-prd.id
    subnet_id = module.gru_subprv-backend_vcn-prd.id
    lb_subnet_ids = [module.gru_subpub-frontend_vcn-prd.id]

    cluster_name = "oke_fotogal"
    pods_cidr = "10.244.0.0/16"
    services_cidr = "10.96.0.0/16"
}    

module "gru_oke-nodepool-fotogal_prd" {
    source = "./modules/oke/node_pool"

    providers = {
       oci = oci.gru
    }
   
    compartment_id = var.compartment_id
    cluster_id = module.gru_oke-cluster-fotogal_prd.id
    subnet_id = module.gru_subprv-backend_vcn-prd.id

    nodepool_name = "oke_nodepool_fotogal"
    nodepool_ad = local.ads.gru_ad1_name
    node_image_id = local.compute_image_id.gru.ol8
    node_count = 2
}