#
# locals.tf
#

locals {    
   anywhere = "0.0.0.0/0" 
   all_protocols = "all"

   # IANA protocol numbers
   icmp_protocol = 1
   tcp_protocol = 6
   udp_protocol = 17
   
   # Service Gateway
   gru_all_oci_services = lookup(data.oci_core_services.gru_all_oci_services.services[0], "id")
   gru_oci_services_cidr_block = lookup(data.oci_core_services.gru_all_oci_services.services[0], "cidr_block")

   # Availability Domains
   ads = {
      gru_ad1_id = data.oci_identity_availability_domains.gru_ads.availability_domains[0].id
      gru_ad1_name = data.oci_identity_availability_domains.gru_ads.availability_domains[0].name
   }

   # Fault Domains
   fds = {
      gru_fd1_id = data.oci_identity_fault_domains.gru_fds.fault_domains[0].id,
      gru_fd1_name = data.oci_identity_fault_domains.gru_fds.fault_domains[0].name,

      gru_fd2_id = data.oci_identity_fault_domains.gru_fds.fault_domains[1].id,
      gru_fd2_name = data.oci_identity_fault_domains.gru_fds.fault_domains[1].name,

      gru_fd3_id = data.oci_identity_fault_domains.gru_fds.fault_domains[2].id,
      gru_fd3_name = data.oci_identity_fault_domains.gru_fds.fault_domains[2].name
   }

   # GRU Object Storage Namespace
   gru_objectstorage_ns = data.oci_objectstorage_namespace.gru_objectstorage_ns.namespace
}
