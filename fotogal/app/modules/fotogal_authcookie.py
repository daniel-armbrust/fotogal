#
# fotogal/app/modules/fotogal_authcookie.py
#
import datetime
import secrets
import os
import binascii

from flask import current_app as app
from cryptography.fernet import Fernet, InvalidToken

from app.modules import utils
from app.modules.fotogal_nosql import FotogalNosql
from app.modules.fotogal_user import FotogalUser


class FotogalAuthCookie():    
    """Simple class to generate an authentication cookie values for 
    FotoGal application.
    
    """
    def __init__(self):             
        self._nosql_table = app.config.get('NOSQL_TABLE_AUTHSESSION')
        self._secret_key = app.config.get('AUTH_COOKIE_SECRET_KEY')
        self._cookie_name = app.config.get('AUTH_COOKIE_NAME')
    
    def __encrypt(self, value):                
        f = Fernet(self._secret_key)
        encrypted_base64 = f.encrypt(value.encode()).decode()

        return encrypted_base64

    def __decrypt(self, value):
        f = Fernet(self._secret_key)
        decrypted = f.decrypt(value.encode()).decode()

        return decrypted

    def __gen_random_token(self):
        secrets_token_1 = secrets.token_hex(12)
        secrets_token_2 = binascii.hexlify(os.urandom(12)).decode()
        ts = datetime.datetime.now().strftime('%s')

        # Oracle NoSQL primary key of 64 chars is the limit.
        random_token = '%s:%s:%s' % (secrets_token_1, secrets_token_2, ts,)

        return random_token

    def create(self, user_id):
        """Create and return cookie properties to create a cookie for
        authentication purposes.
        
        """
        fotogal_user = FotogalUser()

        if utils.validate_id(user_id) and fotogal_user.exists(id=user_id):
            random_token = self.__gen_random_token()
            random_token = str(user_id) + ':' + random_token

            # truncate to 64 chars because of the primary key limit.
            if len(random_token) > 64:
                random_token = random_token[:64]

            datetime_now = datetime.datetime.now()
            expire_timedelta = datetime_now + datetime.timedelta(days=7)

            created_ts = int(datetime_now.strftime('%s'))
            expire_ts = int(expire_timedelta.strftime('%s'))
            
            enc_base64_value = self.__encrypt(random_token)
            
            auth_session_dict = {'random_token': random_token, 
                'created_ts': created_ts, 'expire_ts': expire_ts, 
                'user_id': user_id}
                        
            nosql = FotogalNosql()
            nosql_result = nosql.add(self._nosql_table, auth_session_dict)

            if nosql_result:
                return (self._cookie_name, enc_base64_value, expire_ts,)
        
        return None
            
    def validate(self, enc_cookie_value, user_id):
        """Return TRUE if the encrypted cookie value is valid.

        """
        if utils.validate_id(user_id):            
            try:          
                random_token = self.__decrypt(enc_cookie_value)           
            except InvalidToken as e:                
                return False

            cookie_user_id = int(random_token[:random_token.index(':')])

            if utils.validate_id(cookie_user_id):                
                fields = 'random_token, created_ts, expire_ts'
                table = self._nosql_table        
                conditions = 'random_token = "%s" AND user_id = %d LIMIT 1' % (random_token, user_id,)

                query = f'SELECT {fields} FROM {table} WHERE {conditions}'

                nosql = FotogalNosql()
                nosql_result = nosql.exec_query(table, query)

                if len(nosql_result) > 0:
                    if user_id == cookie_user_id:
                        now_ts = int(datetime.datetime.now().strftime('%s'))
                        expire_ts = int(nosql_result[0]['expire_ts'])

                        if now_ts >= expire_ts:                            
                            self.remove(enc_cookie_value, user_id)
                            app.logger.debug('Removing cookie (%s)' % (enc_cookie_value,))
                            return False
                        else:
                            return True

                    else:                        
                        return False
                else:                    
                    return False
        
        return False
    
    def remove(self, enc_cookie_value, user_id):
        """Validate and remove the auth cookie values.

        """
        if utils.validate_id(user_id):
            if self.validate(enc_cookie_value, user_id):
                random_token = self.__decrypt(enc_cookie_value)

                table = self._nosql_table                
                conditions = 'random_token = "%s" AND user_id = %d' % (random_token, user_id,)

                query = f'DELETE FROM {table} WHERE {conditions}'

                nosql = FotogalNosql()
                nosql_result = nosql.exec_query(table, query)

                if len(nosql_result) > 0:
                    return True               
        
        return False