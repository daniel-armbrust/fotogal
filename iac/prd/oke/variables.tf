//
// iac/prd/oke/variables.tf
//

variable "compartment_ocid" {}

variable "vcn_display_name" {
    default = "vcn-oke"
}

variable "lb_subnet_display_name" {
    default = "subnpub-1_vcn-oke"
}

variable "workers_subnet_display_name" {
    default = "subnprv-1_vcn-oke"
}

variable "cluster_name" {
    default = "oke-fotogal"
}

variable "kubernetes_version" {
    default = "v1.18.10"
}

variable "pods_cidr_block" {
    default = "10.244.0.0/16"
}

variable "service_cidr_block" {
    default = "10.96.0.0/16"
}

variable "node_pool_name" {
    default = "oke-fotogal_np-1"
}

variable "node_pool_shape_ocpus" {
    default = 2
}

variable "node_pool_shape_mem_in_gbs" {
    default = 4
}

variable "node_pool_shape_bootvol_in_gbs" {
    default = 100
}

variable "node_pool_shape_quantity" {
    default = 2
}

variable "image_ocid" {   
    default = "ocid1.image.oc1.sa-saopaulo-1.aaaaaaaa7inha53kcyutiqdbz3w4gvms2ab5z3bc624loheugh7fbvg4wada"
}