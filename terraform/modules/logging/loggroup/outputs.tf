#
# modules/logging/loggroup/outputs.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/logging_log_group
#

output "id" {
    value = oci_logging_log_group.log_group.id
}