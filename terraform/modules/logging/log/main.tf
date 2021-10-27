#
# modules/logging/log/main.tf
# https://registry.terraform.io/providers/hashicorp/oci/latest/docs/resources/logging_log
#

resource "oci_logging_log" "log" {    
    display_name = var.display_name

    log_group_id = var.loggroup_id
    log_type = var.log_type
    is_enabled = var.is_enable
    retention_duration = var.retention_duration
}