#!/bin/sh
#
# iac/run.sh
#

### Change this variables if necessary
OCI_CONFIG_DIR="`readlink -f ../fotogal/oci_config/`"
OCI_CONFIG_FILE="$OCI_CONFIG_DIR/oci.conf"
OCI_PRIVATE_KEY_FILE="$OCI_CONFIG_DIR/oci_api_key.pem"

show_help() {

cat <<EOH

FotoGal terraform script
========================

Usage: $(basename "$0") [-d|-t|-p] [init|validate|plan|apply|destroy] [-f]

  Environment options (required):
     -d  Process DEVELOPMENT environment
     -t  Process HOMOL/Q&A environment
     -p  Process PRODUCTION environment

  Terraform commands (required):
     init      Prepare your working directory for other commands
     validate  Check whether the configuration is valid
     plan      Show changes required by the current configuration
     apply     Create or update infrastructure
     destroy   Destroy previously-created infrastructure

  Global options:
     -f  Force operation

  Examples:
    $(basename "$0") -d plan
    $(basename "$0") -t init
    $(basename "$0") -p apply -f

EOH

  exit 1
}

set_env_vars() {
   local env="$1"

   if [ \( ! -f "$OCI_CONFIG_FILE" \) -o \( ! -f "$OCI_PRIVATE_KEY_FILE" \) ]; then
     echo "The OCI config file or private key was not found in dir: $OCI_CONFIG_DIR"
     echo "Exiting..."
     exit 1
   else
     set +o history

     # https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm
     export TF_VAR_tenancy_ocid="`cat "$OCI_CONFIG_FILE" | grep ^tenancy | cut -f2 -d '='`"
     export TF_VAR_user_ocid="`cat "$OCI_CONFIG_FILE" | grep ^user | cut -f2 -d '='`"
     export TF_VAR_compartment_ocid="`cat "$OCI_CONFIG_FILE" | grep ^compartment | cut -f2 -d '='`"
     export TF_VAR_fingerprint="`cat "$OCI_CONFIG_FILE" | grep ^fingerprint | cut -f2 -d '='`"
     export TF_VAR_region="`cat "$OCI_CONFIG_FILE" | grep ^region | cut -f2 -d '='`"
     export TF_VAR_private_key_path="$OCI_PRIVATE_KEY_FILE"
     export TF_VAR_environment="$env"

     set -o history
   fi
}

tf_init() {
  local env="$1"	
  local force="$2"

  if [ "$force" == '-f' ]; then
     tfcmd="terraform init -reconfigure"
  else
     tfcmd="terraform init"
  fi

  local cdir="`pwd`"
  cd "$env/"

  set_env_vars "$env"

  for tfdir in `find . -type d | egrep -v "(/\.|^.$)"`; do
     echo -e "\n+++ Initializing dir \"$tfdir\" ...\n"
     cd "$tfdir"
     $tfcmd
     cd - 1>/dev/null
  done

  cd "$cdir" 1>/dev/null

  exit 0
}

tf_validate() {
  local env="$1"

  local cdir="`pwd`"
  cd "$env/"

  set_env_vars "$env"

  for tfdir in `find . -type d | egrep -v "(/\.|^.$)"`; do
     echo -e "\n+++ Checking dir \"$tfdir\" ...\n"
     cd "$tfdir"
     terraform validate
     cd - 1>/dev/null
  done

  cd "$cdir" 1>/dev/null

  exit 0
}

tf_plan() {
  local env="$1"

  local cdir="`pwd`"
  cd "$env/"

  set_env_vars "$env"

  for tfdir in `find . -type d | egrep -v "(/\.|^.$)"`; do
     echo -e "\n+++ Planning dir \"$tfdir\" ...\n"
     cd "$tfdir"
     terraform plan
     cd - 1>/dev/null
  done

  cd "$cdir" 1>/dev/null

  exit 0
}

tf_apply() {
  local env="$1"
  local force="$2"

  local apply_order=('logging' 'vcn-oke' 'oke' 'nosql' 'objectstorage')

  if [ "$force" == '-f' ]; then
     tfcmd="terraform apply -auto-approve"
  else
     tfcmd="terraform apply"
  fi

  local cdir="`pwd`"
  cd "$env/"

  set_env_vars "$env"

  local i=0
  while [ $i -lt ${#apply_order[*]} ]; do
    tfdir="${apply_order[$i]}"
    let i+=1

    echo -e "\n+++ Applying dir \"$tfdir\" ...\n"

    if [ ! -d "$tfdir" ]; then
      echo "++++++ Dir \"$tfdir\" not found! Skipping ..."
      continue
    fi 

    cd "$tfdir"
    $tfcmd

    cd - 1>/dev/null
  done

  cd "$cdir" 1>/dev/null

  exit 0
}

tf_destroy() {
  local env="$1"
  local force="$2"

  local destroy_order=('oke' 'vcn-oke' 'nosql' 'objectstorage' 'logging')

  if [ "$force" == '-f' ]; then
     tfcmd="terraform destroy -auto-approve"
  else
     tfcmd="terraform destroy"
  fi

  local cdir="`pwd`"
  cd "$env/"

  set_env_vars "$env"

  local i=0
  while [ $i -lt ${#destroy_order[*]} ]; do
    tfdir="${destroy_order[$i]}"

    echo -e "\n+++ Destroying dir \"$tfdir\" ...\n"

    if [ ! -d "$tfdir" ]; then
      echo "++++++ Dir \"$tfdir\" not found! Skipping ..."
      continue
    fi 

    cd "$tfdir"
    $tfcmd

    cd - 1>/dev/null

    let i+=1
  done

  cd "$cdir" 1>/dev/null

  exit 0
}

clean() {
  local env="$1"

  local cdir="`pwd`"
  cd "$env/"

  for tfdir in `find . -type d | egrep -v "(/\.|^.$)"`; do
    echo -e "\n+++ Cleaning dir \"$tfdir\" ...\n"
    test -d "$tfdir/.terraform/" && rm -rf "$tfdir/.terraform/"
  done 

  cd "$cdir" 1>/dev/null

  exit 0
}


process_env() {
  local tfenv="$1"
  local tfcmd="$2"
  local force="$3"

  if [ ! -d "$tfenv" ]; then
    echo "ERROR! Directory \"iac/$tfenv/\" was not found!"
    echo "Exiting..."
    exit 1
  fi

  case "$tfcmd" in
       init)
              tf_init "$tfenv" "$force"
                 ;;
       validate)
              tf_validate "$tfenv"
                 ;;
       plan)
              tf_plan "$tfenv"
                 ;;
       apply)
              tf_apply "$tfenv" "$force"
                 ;;
       destroy)
              tf_destroy "$tfenv" "$force"
                 ;;
       clean)
              clean "$tfenv"
                 ;;	      
  esac

}

while getopts "d:t:p:" opt; do

  case "$opt" in
       d)
          tf_cmd="$OPTARG"
          process_env "dev" "$tf_cmd" "$3"
          ;;
       t)
          tf_cmd="$OPTARG"
          process_env "hml" "$tf_cmd" "$3"
          ;;
       p)
          tf_cmd="$OPTARG"
          process_env "prd" "$tf_cmd" "$3" "$4"
          ;;
       *)
          show_help
          ;;

  esac

done

if [ -z "$terraform_cmd" ]; then
  show_help
fi


exit 0
