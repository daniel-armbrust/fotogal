#
# modules/oke/cluster/variables.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/containerengine_cluster
#

variable "compartment_id" {
    description = "(Required) The OCID of the compartment in which to create the cluster."
    type = string    
}

variable "vcn_id" {
    description = "(Required) The OCID of the virtual cloud network (VCN) in which to create the cluster."
    type = string    
}

variable "subnet_id" {
    description = "(Optional) The OCID of the regional subnet in which to place the Cluster endpoint."
    type = string
}

variable "k8s_version" {
    description = "(Required) (Updatable) The version of Kubernetes to install into the cluster masters."   
    type = string
    default = "v1.20.11"
}

variable "cluster_name" {
    description = "(Required) (Updatable) The name of the cluster."
    type = string
    default = "oke_cluster_v1.20.11"
}

variable "is_public_ip_enabled" {
    description = "(Optional) Whether the cluster should be assigned a public IP address."
    type = bool
    default = false
}

variable "dashboard_enabled" {
    description = "(Optional) Whether or not to enable the Kubernetes Dashboard add-on."
    type = bool
    default = true
}

variable "tiller_enabled" {
    description = "(Optional) Whether or not to enable the Tiller add-on."
    type = bool
    default = true
}

variable "pod_secpol_enabled" {
    description = "(Optional) (Updatable) Whether or not to enable the Pod Security Policy admission controller."
    type = bool
    default = true
}

variable "pods_cidr" {
    description = "(Optional) The CIDR block for Kubernetes pods."
    type = string
    default = "10.244.0.0/16"
}

variable "services_cidr" {
    description = "(Optional) The CIDR block for Kubernetes services."
    type = string
    default = "10.96.0.0/16"
}

variable "lb_subnet_ids" {
    description = "(Optional) The OCIDs of the subnets used for Kubernetes services load balancers."
    type = list(string)
    default = null
}