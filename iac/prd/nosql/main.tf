//
// iac/prd/nosql/main.tf
//

//
// Table: fotogal_ntable_images
//
resource "oci_nosql_table" "fotogal_ntable_images" {
  compartment_id = var.compartment_ocid
  ddl_statement  = var.fotogal_ntable_images_ddl
  name           = "fotogal_ntable_images"

  table_limits {
    max_read_units     = "10"
    max_write_units    = "10"
    max_storage_in_gbs = "1"
  }
}

resource "oci_nosql_index" "ntable_images_user_id_idx" {
  keys {
    column_name = "user_id"
  }

  name = "user_id_idx"
  table_name_or_id = oci_nosql_table.fotogal_ntable_images.id
}

resource "oci_nosql_index" "ntable_images_created_ts_idx" {
  keys {
    column_name = "created_ts"
  }

  name = "created_ts_idx"
  table_name_or_id = oci_nosql_table.fotogal_ntable_images.id
}


//
// Table: fotogal_ntable_users
//
resource "oci_nosql_table" "fotogal_ntable_users" {
  compartment_id = var.compartment_ocid
  ddl_statement  = var.fotogal_ntable_users_ddl
  name           = "fotogal_ntable_users"

  table_limits {
    max_read_units     = "10"
    max_write_units    = "10"
    max_storage_in_gbs = "1"
  }
}


//
// Table: fotogal_ntable_authsession
//
resource "oci_nosql_table" "fotogal_ntable_authsession" {
  compartment_id = var.compartment_ocid
  ddl_statement  = var.fotogal_ntable_authsession_ddl
  name           = "fotogal_ntable_authsession"

  table_limits {
    max_read_units     = "5"
    max_write_units    = "5"
    max_storage_in_gbs = "1"
  }
}

resource "oci_nosql_index" "ntable_authsession_user_id_idx" {
  keys {
    column_name = "user_id"
  }

  name = "user_id_idx"
  table_name_or_id = oci_nosql_table.fotogal_ntable_authsession.id
}