#
# fotogal/app/modules/fotogal_user.py
#

from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from app.modules import utils
from app.modules.fotogal_nosql import FotogalNosql


class FotogalUser():
    """Class for manipulating FotoGal users.

    """
    def __init__(self):        
        self._nosql_table = app.config.get('NOSQL_TABLE_USERS')   
  
    def __get_all_user_props(self, id=None, email=None, username=None):
        """Return all user's properties.

        """
        if id and utils.validate_id(id):
           conditions = 'id = %d LIMIT 1' % (id,)
        elif email and utils.validate_email(email):
           conditions = 'email = "%s" LIMIT 1' % (email,)   
        elif username and utils.validate_username(username):
           conditions = 'username = "%s" LIMIT 1' % (username,)               
        else:
           return None

        fields = '*'
        table = self._nosql_table
        
        query = f'SELECT {fields} FROM {table} WHERE {conditions}'

        nosql = FotogalNosql()
        nosql_result = nosql.exec_query(table, query)

        profile_dict = {'id': '', 'email': '', 'full_name': '', 'username': '',
            'password': '', 'follow_list': [], 'follow_sent_list': [],
            'follow_you_list': [], 'follow_received_list': [], 'created_ts': '', 
            'is_private': '', 'is_professional_account': '', 'profile_image_url': '', 
            'user_data': {'birthday_ts': '', 'website': '', 'bio': '', 
            'gender': '', 'phone_number': ''}}
        
        if len(nosql_result) > 0:
           
            for k,v in profile_dict.items():
                if k == 'user_data':
                    for k,v in nosql_result[0]['user_data'].items():
                        profile_dict['user_data'][k] = v
                else:
                    profile_dict[k] = nosql_result[0][k]

            return profile_dict

        else:
            return None

    def get_pkey_values(self, id=None, email=None, username=None):
        """Returns the user's primary key values. Some operations in Oracle 
        NoSQL (like UPDATE) requires all primary key values to be informed.

        """
        if id and utils.validate_id(id):
           conditions = 'id = %d LIMIT 1' % (id,)
        elif email and utils.validate_email(email):
           conditions = 'email = "%s" LIMIT 1' % (email,)   
        elif username and utils.validate_username(username):
           conditions = 'username = "%s" LIMIT 1' % (username,)               
        else:
           return None    
        
        fields = 'id, email, username'
        table = self._nosql_table
        
        query = f'SELECT {fields} FROM {table} WHERE {conditions}'

        nosql = FotogalNosql()
        nosql_result = nosql.exec_query(table, query)

        user_dict = {'id': '', 'username': '', 'email': ''}

        if len(nosql_result) > 0:
            user_dict['id'] = nosql_result[0]['id']
            user_dict['username'] = nosql_result[0]['username']
            user_dict['email'] = nosql_result[0]['email']
            
            return user_dict

        else:
            return user_dict       

    def get_id(self, email=None, username=None):
        """Return the user ID.

        """
        if email and utils.validate_email(email):
           conditions = 'email = "%s" LIMIT 1' % (email,)   
        elif username and utils.validate_username(username):
           conditions = 'username = "%s" LIMIT 1' % (username,)               
        else:
           return None

        fields = 'id'
        table = self._nosql_table  

        query = f'SELECT {fields} FROM {table} WHERE {conditions}'

        nosql = FotogalNosql()
        nosql_result = nosql.exec_query(table, query)

        if len(nosql_result) > 0:
            return nosql_result[0]['id']
        else:
            return None

    def get_username(self, id=None, email=None):
        """Return the username.

        """
        if id and utils.validate_id(id):
            conditions = 'id = %d LIMIT 1' % (id,)
        elif email and utils.validate_email(email):
            conditions = 'email = "%s" LIMIT 1'
        else:
            return None
        
        fields = 'username'
        table = self._nosql_table

        query = f'SELECT {fields} FROM {table} WHERE {conditions}'

        nosql = FotogalNosql()
        nosql_result = nosql.exec_query(table, query)

        if len(nosql_result) > 0:
            return nosql_result[0]['username']
        else:
            return None

    def get_profile_img_url(self, id=None, email=None, username=None):
        """Return the image profile URL.

        """
        if id and utils.validate_id(id):
           conditions = 'id = %d LIMIT 1' % (id,)
        elif email and utils.validate_email(email):
           conditions = 'email = "%s" LIMIT 1' % (email,)   
        elif username and utils.validate_username(username):
           conditions = 'username = "%s" LIMIT 1' % (username,)               
        else:
           return None
        
        fields = 'profile_image_url'
        table = self._nosql_table

        query = f'SELECT {fields} FROM {table} WHERE {conditions}'

        nosql = FotogalNosql()
        nosql_result = nosql.exec_query(table, query)

        if len(nosql_result) > 0:
            return nosql_result[0]['profile_image_url']
        else:
            return None

    def get_profile_props(self, id=None, email=None, username=None):
        """Return the user profile properties.

        """
        if id and utils.validate_id(id):
           conditions = 'id = %d LIMIT 1' % (id,)
        elif email and utils.validate_email(email):
           conditions = 'email = "%s" LIMIT 1' % (email,)   
        elif username and utils.validate_username(username):
           conditions = 'username = "%s" LIMIT 1' % (username,)               
        else:
           return None

        fields = 'id, email, username, full_name, is_private, is_professional_account, user_data, created_ts, profile_image_url'
        table = self._nosql_table      

        query = f'SELECT {fields} FROM {table} WHERE {conditions}'
        
        nosql = FotogalNosql()
        nosql_result = nosql.exec_query(table, query)

        profile_dict = {'id': '', 'email': '', 'username': '', 'full_name': '', 
            'created_ts': '', 'is_private': '', 'is_professional_account': '',
            'profile_image_url': '', 'user_data': {'birthday_ts': '',
            'website': '', 'bio': '', 'gender': '', 'phone_number': ''}}

        if len(nosql_result) > 0:            

            for k,v in profile_dict.items():                
                if k == 'user_data':
                    for k,v in nosql_result[0]['user_data'].items():
                        profile_dict['user_data'][k] = v                    
                else:               
                    profile_dict[k] = nosql_result[0][k]            
            
            return profile_dict

        else:
            return None       

    def update_profile_props(self, id=None, email=None, username=None, profile_dict={}):
        """Update the user profile properties. 
        
        """
        if id and utils.validate_id(id):
           user_props_dict = self.__get_all_user_props(id=id)           
        elif email and utils.validate_email(email):
           user_props_dict = self.__get_all_user_props(email=email)           
        elif username and utils.validate_username(username):
           user_props_dict = self.__get_all_user_props(username=username)           
        else:
           return None    

        # this fields will not be updated by this method. 
        protected_fields = ('id', 'email', 'username', 'password',)

        for k,v in user_props_dict.items():
            if k in protected_fields:
                continue
            elif k in profile_dict:
                user_props_dict[k] = profile_dict[k]
        
        table = self._nosql_table
        nosql = FotogalNosql()
        nosql_result = nosql.update(table, user_props_dict)

        return nosql_result

    def exists(self, id=None, email=None, username=None):
        """Check if the user exists.

        """
        if id and utils.validate_id(id):
           conditions = 'id = %d LIMIT 1' % (id,)
        elif email and utils.validate_email(email):
           conditions = 'email = "%s" LIMIT 1' % (email,)   
        elif username and utils.validate_username(username):
           conditions = 'username = "%s" LIMIT 1' % (username,)               
        else:
           return False    

        fields = 'username AS result' 
        table = self._nosql_table        

        query = f'SELECT {fields} FROM {table} WHERE {conditions}'

        nosql = FotogalNosql()
        nosql_result = nosql.exec_query(table, query)

        if len(nosql_result) > 0:                
            return True
        else:
            return False        

    def is_private(self, id=None, email=None, username=None):
        """Check if the user is a private user.

        """
        if id and utils.validate_id(id):
           conditions = 'id = %d LIMIT 1' % (id,)
        elif email and utils.validate_email(email):
           conditions = 'email = "%s" LIMIT 1' % (email,)   
        elif username and utils.validate_username(username):
           conditions = 'username = "%s" LIMIT 1' % (username,)               
        else:
           return False    

        fields = 'is_private'
        table = self._nosql_table        

        query = f'SELECT {fields} FROM {table} WHERE {conditions}'

        nosql = FotogalNosql()
        nosql_result = nosql.exec_query(table, query)

        if len(nosql_result) > 0:
            return nosql_result[0]['is_private']
        else:
            return None   

    def check_passwd(self, id=None, email=None, username=None, passwd=''):
        """Checks the user password.

        """
        if id and utils.validate_id(id):
           conditions = 'id = %d LIMIT 1' % (id,)
        elif email and utils.validate_email(email):
           conditions = 'email = "%s" LIMIT 1' % (email,)   
        elif username and utils.validate_username(username):
           conditions = 'username = "%s" LIMIT 1' % (username,)               
        else:
           return False    

        fields = 'password'
        table = self._nosql_table        

        query = f'SELECT {fields} FROM {table} WHERE {conditions}'

        nosql = FotogalNosql()
        nosql_result = nosql.exec_query(table, query)

        if len(nosql_result) > 0:
            passwd_db_hash = nosql_result[0]['password']

            try:
                passwd_check_status = check_password_hash(passwd_db_hash, passwd)
            except:
                return False
            else:
                if passwd_check_status:
                    return True
                else:
                    return False
        else:
            return False    
        
    def update_passwd(self, id=None, email=None, username=None, passwd=''):
        """Generate a new password hash and update the user.

        """
        if id and utils.validate_id(id):
           user_pkey_dict = self.get_pkey_values(id=id)           
        elif email and utils.validate_email(email):
           user_pkey_dict = self.get_pkey_values(email=email)           
        elif username and utils.validate_username(username):
           user_pkey_dict = self.get_pkey_values(username=username)           
        else:
           return None    
                
        new_passwd_hash = generate_password_hash(passwd)

        fields = 'SET password = "%s"' % (new_passwd_hash,)        
        table = self._nosql_table

        conditions = 'id = %d AND email = "%s" AND username = "%s"' % (user_pkey_dict['id'], 
            user_pkey_dict['email'], user_pkey_dict['username'],)

        query = f'UPDATE {table} {fields} WHERE {conditions}'

        nosql = FotogalNosql()
        nosql_result = nosql.exec_query(table, query)

        if len(nosql_result) > 0:

            if nosql_result[0]['NumRowsUpdated'] == 1:
                return True
            else:
                return False

        else:
            return False

    def add_new_user(self, new_user_dict={}):
        """Add a new user and return the new generated ID from NoSQL.

        """
        if 'password' in new_user_dict:
            passwd_hash = generate_password_hash(new_user_dict['password'])
            new_user_dict['password'] = passwd_hash

            table = self._nosql_table

            nosql = FotogalNosql()
            nosql_result = nosql.add(table, new_user_dict)

            return nosql_result

        else:
            return None