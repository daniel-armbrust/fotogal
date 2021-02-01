//
// iac/prd/logging/variables.tf
//

variable "compartment_ocid" {}

variable "log_group_display_name" {
    default = "fotogal_loggroup"
}

variable "log_display_name" {
    default = "fotogal_customlog_app"
}

variable "log_retention_duration" {
    // Log retention duration in 30-day increments (30, 60, 90 and so on).
    default = 30
}