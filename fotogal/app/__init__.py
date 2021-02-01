#
# fotogal/app/__init__.py
#
import sys
import logging

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from app.modules.fotogal_log import FotogalLog
from app.modules.fotogal_nosql import FotogalNosql

import oci

from config import config

csrf = CSRFProtect()

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])
  config[config_name].init_app(app)

  app.jinja_env.trim_blocks = True
  app.jinja_env.lstrip_blocks = True

  # Init OCI SDK
  oci_config_filepath = app.root_path + '/../' + app.config.get('OCI_CONFIG_FILE')
  oci_privkey_filepath = app.root_path + '/../' + app.config.get('OCI_PRIVKEY_FILE')

  oci_config = oci.config.from_file(oci_config_filepath)
  oci_config['key_file'] = oci_privkey_filepath  

  app.config['oci_config'] = oci_config

  # App Log
  oci_loggroup_name = app.config.get('LOG_GROUP_NAME')
  oci_customlog_name = app.config.get('LOG_NAME')
    
  log_handler = FotogalLog.create_handler(oci_config, oci_loggroup_name, oci_customlog_name)  
  app.logger.addHandler(log_handler)
    
  # CSRF Token
  csrf.init_app(app)
 
  # Init and get the OCI NoSQL handle.
  # A handle has memory and network resources associated with it. To minimize 
  # network activity as well as resource allocation and deallocation overheads, 
  # it’s best to avoid repeated creation and closing of handles. So we create 
  # and globalize the handle here for the entire app.
  app._nosql_handle = FotogalNosql.create_handler(oci_config,  app.logger)
  
  from .auth import auth as auth_blueprint
  from .main import main as main_blueprint
  from .api import api as api_blueprint
  
  app.register_blueprint(auth_blueprint)
  app.register_blueprint(main_blueprint)  
  app.register_blueprint(api_blueprint, url_prefix='/api/v1')  

  return app
