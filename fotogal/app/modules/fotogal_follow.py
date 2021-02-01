#
# fotogal/app/modules/fotogal_follow.py
#
from flask import current_app as app

from app.modules import utils
from app.modules.fotogal_nosql import FotogalNosql
from app.modules.fotogal_user import FotogalUser


class FotogalFollow():
    """Class for manipulating FotoGal Followers/Following users.

    """
    def __init__(self):        
        self._nosql_table = app.config.get('NOSQL_TABLE_USERS')
    
    def __add_list_item(self, list_name, list_owner_id, user_follow_id):
        """Add the "user_follow_id" into the "list_name" from "list_owner_id".

        """
        fotogal_user = FotogalUser()
        owner_list_dict = fotogal_user.get_pkey_values(id=list_owner_id)
        
        nosql = FotogalNosql()
        table = self._nosql_table
        
        # Check if the ID doesn't exist in follow_list array.
        fields = 'id'
        conditions = 'id = %d AND %s[] =any %d' % (owner_list_dict['id'], list_name, user_follow_id,)        

        query = f'SELECT {fields} FROM {table} WHERE {conditions}'

        nosql_result = nosql.exec_query(table, query)

        if len(nosql_result) > 0:
            return False
        else:
            fields = '%s %d' % (list_name, user_follow_id,)
            conditions = 'id = %d AND username = "%s" AND email = "%s"' % (owner_list_dict['id'], owner_list_dict['username'], owner_list_dict['email'],)

            query = f'UPDATE {table} ADD {fields} WHERE {conditions}'
            
            nosql = FotogalNosql()
            nosql_result = nosql.exec_query(table, query)

            return True

    def is_following(self, user_id, follow_user_id):
        """Return TRUE if the "user_id" is following the "follow_user_id".

        """
        if utils.validate_id(user_id) and utils.validate_id(follow_user_id):
            fields = 'follow_list[$element = %d] AS follow_user_id' % (follow_user_id,)            
            table = self._nosql_table
            conditions = 'id = %d' % (user_id,)

            query = f'SELECT {fields} FROM {table} WHERE {conditions}'

            nosql = FotogalNosql()
            nosql_result = nosql.exec_query(table, query)

            if len(nosql_result) > 0:
                if nosql_result[0]['follow_user_id'] == follow_user_id:
                    return True
                else:
                    return False

    def get_suggestions(self):
        """Return some users as suggestions to follow.

        """
        MAX_USERS_TO_RETURN = 30

        fields = 'id, full_name, username, profile_image_url, is_private'
        conditions = 'is_professional_account = TRUE LIMIT %d' % (MAX_USERS_TO_RETURN,)
        table = self._nosql_table

        query = f'SELECT {fields} FROM {table} WHERE {conditions}'

        nosql = FotogalNosql()
        nosql_result = nosql.exec_query(table, query)

        return nosql_result

    def get_following_total(self, user_id):
        """Returns the total from "follow_list".

        """
        if utils.validate_id(user_id):
            fields = 'count(follow_list[]) AS total'
            table = self._nosql_table
            conditions = 'id = %d' % (user_id,)

            query = f'SELECT {fields} FROM {table} WHERE {conditions}'

            nosql = FotogalNosql()
            nosql_result = nosql.exec_query(table, query)

            if len(nosql_result) > 0:
                return nosql_result[0]['total']
            else:
                return 0

    def get_followers_total(self, user_id):
        """Returns the total from "follow_you_list".

        """
        if utils.validate_id(user_id):
            fields = 'count(follow_you_list[]) AS total'
            table = self._nosql_table
            conditions = 'id = %d' % (user_id,)

            query = f'SELECT {fields} FROM {table} WHERE {conditions}'

            nosql = FotogalNosql()
            nosql_result = nosql.exec_query(table, query)

            if len(nosql_result) > 0:
                return nosql_result[0]['total']
            else:
                return 0

    def get_follow_list(self, user_id=None, index_low=None, index_high=None):        
        """Returns a sublist of user IDs from the "follow_list".

        """
        if utils.validate_id(user_id):
            if index_low and index_high:
                fields = '[follow_list[%d:%d]] AS follow_list' % (index_low, index_high,)            
            else:
                fields = 'follow_list AS follow_list'
                
            table = self._nosql_table
            conditions = 'id = %d LIMIT 1' % (user_id,)

            query = f'SELECT {fields} FROM {table} WHERE {conditions}'

            nosql = FotogalNosql()
            nosql_result = nosql.exec_query(table, query)

            return nosql_result[0]['follow_list']
    
    def add(self, user_id, user_id_follow):
        """Add the "user_id_follow" into the "user_id" follow list if the
        user to follow is not a private user. If the user to follow is private,
        the id will be inserted in the "follow_received_list".

        """
        if utils.validate_id(user_id) and utils.validate_id(user_id_follow):            
            fotogal_user = FotogalUser()

            if fotogal_user.is_private(user_id_follow):
                self.__add_list_item('follow_sent_list', user_id, user_id_follow)
                self.__add_list_item('follow_received_list', user_id_follow, user_id)        
            else:
                self.__add_list_item('follow_list', user_id, user_id_follow)
                self.__add_list_item('follow_you_list', user_id_follow, user_id)

            return True