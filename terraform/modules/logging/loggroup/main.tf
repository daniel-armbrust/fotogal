#
# modules/logging/loggroup/main.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/logging_log_group
#

resource "oci_logging_log_group" "log_group" {
    compartment_id = var.compartment_id
    display_name = var.display_name
    description = var.description
}
