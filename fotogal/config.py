#
# fotogal/config.py
#

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config: 
  SECRET_KEY = os.environ.get('SECRET_KEY')
  WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY')
  AUTH_COOKIE_SECRET_KEY = os.environ.get('AUTH_COOKIE_SECRET_KEY')

  JSONIFY_PRETTYPRINT_REGULAR = False 

  # Upload maximum allowed payload to 16 megabytes
  MAX_CONTENT_LENGTH = 16 * 1024 * 1024

  # OCI Mail Delivery
  FLASKY_MAIL_SUBJECT_PREFIX = '[FotoGal]'
  FLASKY_MAIL_SENDER = 'FotoGal <no-reply@fotogal.ocibook.com.br>'
  MAIL_SERVER = ''
  MAIL_PORT = 587
  MAIL_USE_TLS = 1
  MAIL_USERNAME = ''
  MAIL_PASSWORD = ''

  @staticmethod
  def init_app(app):
     pass


class DevelopmentConfig(Config):
  DEBUG = True
  
  SESSION_COOKIE_NAME = 'xFotoGalxDevxSession'
  SESSION_COOKIE_HTTPONLY = True
  SESSION_COOKIE_SAMESITE = 'Lax'
  SESSION_PERMANENT = True
  
  AUTH_COOKIE_NAME = 'xFotoGalxDevxAuthx'
  AUTH_COOKIE_HTTPONLY = True
  AUTH_COOKIE_SECURE = False
  
  OCI_CONFIG_FILE = 'oci_config/oci.conf'
  OCI_PRIVKEY_FILE = 'oci_config/oci_api_key.pem'

  # OCI NoSQL Tables
  NOSQL_TABLE_USERS = 'fotogal_ntable_users'
  NOSQL_TABLE_IMAGES = 'fotogal_ntable_images'
  NOSQL_TABLE_AUTHSESSION = 'fotogal_ntable_authsession'

  # OCI Object Storage BUCKET
  IMG_BUCKET_NAME = 'fotogal_bucket_images'

  # OCI Logging
  LOG_GROUP_NAME = 'fotogal_loggroup'
  LOG_NAME = 'fotogal_customlog_app'


class ProductionConfig(Config):
  DEBUG = False  
  
  APP_HOSTNAME = 'fotogal.ocibook.com.br'

  SESSION_COOKIE_NAME = 'xFotoGalxSession'
  SESSION_COOKIE_SECURE = True
  SESSION_COOKIE_HTTPONLY = True
  SESSION_COOKIE_SAMESITE='Lax'
  PERMANENT_SESSION_LIFETIME = 600

  AUTH_COOKIE_NAME = 'xFotoGalxAuthx'
  AUTH_COOKIE_HTTPONLY = True
  AUTH_COOKIE_SECURE = True

  OCI_CONFIG_FILE = 'oci_config/oci.conf'
  OCI_PRIVKEY_FILE = 'oci_config/oci_api_key.pem'

  # OCI NoSQL Tables
  NOSQL_TABLE_USERS = 'fotogal_ntable_users'
  NOSQL_TABLE_IMAGES = 'fotogal_ntable_images'
  NOSQL_TABLE_AUTHSESSION = 'fotogal_ntable_authsession'

  # OCI Object Storage BUCKET
  IMG_BUCKET_NAME = 'fotogal_bucket_images'

  # OCI Logging
  LOG_GROUP_NAME = 'fotogal_loggroup'
  LOG_NAME = 'fotogal_customlog_app'


config = {
  'development': DevelopmentConfig,
  'production': ProductionConfig,

  'default': DevelopmentConfig
}
