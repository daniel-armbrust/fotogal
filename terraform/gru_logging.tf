#
# gru_logging.tf
#

#-------------------
# Logging
#-------------------
module "gru_logging_group" {
    source = "./modules/logging/loggroup"
   
    providers = {
       oci = oci.gru
    }

    compartment_id = var.compartment_id
    display_name = "fotogal_loggroup"
}

module "gru_log" {
    source = "./modules/logging/log"

    providers = {
       oci = oci.gru
    }

    loggroup_id = module.gru_logging_group.id
    
    display_name = "fotogal_customlog_app"
    log_type = "CUSTOM"
}