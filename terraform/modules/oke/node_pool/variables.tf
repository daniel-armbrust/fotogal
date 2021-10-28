#
# modules/oke/node_pool/variables.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/containerengine_node_pool
#

variable "compartment_id" {
    description = "(Required) The OCID of the compartment in which the node pool exists."
    type = string    
}

variable "cluster_id" {
    description = "(Required) The OCID of the cluster to which this node pool is attached."
    type = string
}

variable "k8s_version" {
    description = "(Required) (Updatable) The version of Kubernetes to install on the nodes in the node pool."   
    type = string
    default = "v1.20.11"
}

variable "nodepool_name" {
    description = "(Required) (Updatable) The name of the node pool."
    type = string
    default = "oke_nodepool_v1.20.11"
}

variable "nodepool_ad" {
    description = "(Required) (Updatable) The availability domain in which to place nodes."
    type = string   
}

variable "subnet_id" {
    description = "(Required) (Updatable) The OCID of the subnet in which to place nodes."
    type = string
}

variable "node_shape" {
    description = "(Required) (Updatable) The name of the node shape of the nodes in the node pool." 
    type = string
    default = "VM.Standard2.1"
}

variable "node_memory_gbs" {
    description = "(Optional) (Updatable) The total amount of memory available to each node, in gigabytes."
    type = number
    default = 15
}

variable "node_ocpus_count" {
    description = "(Optional) (Updatable) The total number of OCPUs available to each node in the node pool."
    type = number
    default = 1
}

variable "node_bootvol_gbs" {
    description = "(Optional) (Updatable) The size of the boot volume in GBs. Minimum value is 50 GB."
    type = number
    default = 100
}

variable "node_image_id" {
    description = "(Required) (Updatable) The OCID of the image used to boot the node."
    type = string
}

variable "node_image_source_type" {
    description = "(Required) (Updatable) The source type for the node. Use IMAGE when specifying an OCID of an image."
    type = string
    default = "IMAGE"
}

variable "node_count" {
    description = "(Optional) (Updatable) The number of nodes to create in each subnet."
    type = number
    default = 2
}

variable "node_ssh_pubkey" {
    description = "(Optional) (Updatable) The SSH public key on each node in the node pool on launch."
    type = string
    default = ""
}