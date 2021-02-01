#
# fotogal/app/modules/fotogal_nosql.py
#

import logging

from flask import current_app as app

from borneo.iam import SignatureProvider
from borneo import NoSQLHandle, NoSQLHandleConfig, Regions, GetResult, QueryRequest
from borneo import PutRequest, PutOption

class FotogalNosql():
  """OCI NoSQL class for FotoGal application.

  """
  _nosql_handle = None
 
  @staticmethod
  def create_handler(oci_config, log_handler):
      """Create the handle used to perform OCI NoSQL operations on tables.

      """    
      sigprov = SignatureProvider(tenant_id=oci_config['tenancy'],
          user_id=oci_config['user'], private_key=oci_config['key_file'],
          fingerprint=oci_config['fingerprint'])

      nosql_handle_config = NoSQLHandleConfig(Regions.SA_SAOPAULO_1)
      nosql_handle_config.set_authorization_provider(sigprov)
      nosql_handle_config.set_default_compartment(oci_config['compartment'])      
      nosql_handle_config.set_logger(log_handler)

      nosql_handle = NoSQLHandle(nosql_handle_config)
      
      sigprov.close()
      
      return nosql_handle  

  def __init__(self):
      # Get OCI NoSQL handle from Flask global app.    
      self._nosql_handle = app._nosql_handle 

  def exec_query(self, table=None, sql=None):
      """Execute a SQL Query that return a single result.

      """
      nosql_result = []

      query_request = QueryRequest()     
      nosql_request = query_request.set_statement(sql)        
      query_request.close()             
                            
      nosql_result = self._nosql_handle.query(query_request)
     
      return nosql_result.get_results()
  
  def exec_query_loop(self, table=None, sql=None):
      """Execute a SQL Query that return multiples results.

      """
      nosql_result = []

      query_request = QueryRequest()     
      nosql_request = query_request.set_statement(sql)        
      query_request.close()             
      
      while True:
          nosql_exec_query = self._nosql_handle.query(query_request)
          nosql_result = nosql_exec_query.get_results()
      
          if len(nosql_result) > 0:          
             break
        
          if nosql_request.is_done():
             break
    
      return nosql_result
  
  def add(self, table=None, data_dict=None):
      """Insert new single row.

      """     
      put_request = PutRequest()
      put_request.set_table_name(table)
      put_request.set_option(PutOption.IF_ABSENT)
      put_request.set_value(data_dict)
      
      nosql_result = self._nosql_handle.put(put_request)
     
      # a successful put returns a non-empty version
      if nosql_result.get_version() is not None:
          generated_value = nosql_result.get_generated_value()

          if generated_value:
              return generated_value              
          else:
              return True
      else:
          return False     
  
  def update(self, table=None, data_dict=None):
      """Update existing single row.
      
      """    
      put_request = PutRequest()
      put_request.set_table_name(table)
      put_request.set_option(PutOption.IF_PRESENT)
      put_request.set_value(data_dict)    
      
      nosql_result = self._nosql_handle.put(put_request)

      # a successful put returns a non-empty version
      if nosql_result.get_version() is not None:
          existing_value = nosql_result.get_existing_value()
          
          if existing_value:
              return existing_value
          else:
              return True

      else:
          return False