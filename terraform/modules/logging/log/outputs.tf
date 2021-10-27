#
# modules/logging/log/outputs.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/logging_log
#

output "id" {
    value = oci_logging_log.log.id
}