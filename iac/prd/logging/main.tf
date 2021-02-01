//
// iac/prd/logging/main.tf
//

resource "oci_logging_log_group" "log_group" {  
  compartment_id = var.compartment_ocid
  display_name = var.log_group_display_name
}

resource "oci_logging_log" "logging_log" {  
  display_name = var.log_display_name
  log_group_id = oci_logging_log_group.log_group.id
  log_type = "CUSTOM"
  is_enabled = true
  retention_duration = var.log_retention_duration
}