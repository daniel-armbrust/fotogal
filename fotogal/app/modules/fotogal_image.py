#
# fotogal/app/modules/fotogal_image.py
#
import datetime

from flask import current_app as app

import oci

from app.modules import utils
from app.modules.fotogal_nosql import FotogalNosql
from app.modules.fotogal_user import FotogalUser
from app.modules.fotogal_follow import FotogalFollow


class FotogalImage():    
    """Class for manipulating FotoGal images.

    """
    def __init__(self):
        self._oci_config = app.config.get('oci_config')
        self._img_nosql_table = app.config.get('NOSQL_TABLE_IMAGES')
        self._usr_nosql_table = app.config.get('NOSQL_TABLE_USERS')        
        self._objs_img_bucket = app.config.get('IMG_BUCKET_NAME')
    
    def __get_new_filename(self, filename):
        """Return a random string that will be used to save files in the 
        Object Storage.

        """
        try:
            file_ext = filename.split('.')[1]
        except IndexError:
            file_ext = 'unknown'

        random_str = utils.return_random_string()
        new_filename = random_str + '.' + file_ext

        return new_filename

    def __get_objs_img_hostname(self, img_url):
        """Return the hostname portion of the "img_url".

        """
        str_temp_1 = img_url[img_url.find('/') + 2:]
        img_host_fqdn = str_temp_1[:str_temp_1.find('/')]

        return img_host_fqdn
    
    def __get_objs_img_uri(self, img_url):
        """Return the URI portion of the "img_url".

        """
        str_temp_1 = img_url[img_url.find('/') + 2:]
        img_uri = str_temp_1[str_temp_1.find('/'):]

        return img_uri

    def __get_img_data(self, img_filename):
        """Return the image headers and content from Object Storage.

        """
        object_storage = oci.object_storage.ObjectStorageClient(self._oci_config)
        oci_namespace = object_storage.get_namespace().data

        try:
            object_storage_resp = object_storage.get_object(oci_namespace, self._objs_img_bucket, img_filename)
        except oci.exceptions.ServiceError as e:
            return (None, None,)
        
        if object_storage_resp.status == 200:
            img_headers = {}
            img_content = None    
            
            img_content = object_storage_resp.data.content
            img_type = utils.return_img_type(img_content)

            img_headers['Content-Type'] = utils.return_img_mimetype(img_type)
            img_headers['Last-Modified'] = object_storage_resp.headers['last-modified']
            img_headers['Etag'] = object_storage_resp.headers['etag']
            img_content = object_storage_resp.data.content

            return (img_headers, img_content,)

        else:
            return (None, None,)

    def __add_img_data(self, img_filename, img_content):
        """Save the image contents in Object Storage.

        """
        img_data_dict = {}   

        object_storage = oci.object_storage.ObjectStorageClient(self._oci_config)
        oci_namespace = object_storage.get_namespace().data

        try:
            objs_response = object_storage.put_object(oci_namespace, self._objs_img_bucket, img_filename, img_content)
        except oci.exceptions.ServiceError as e:
            return False        

        if objs_response.status == 200:
            img_url = objs_response.request.url

            img_data_dict = {'image_url': img_url, 
                'image_host_fqdn': self.__get_objs_img_hostname(img_url),
                'image_uri': self.__get_objs_img_uri(img_url),
                'image_type': utils.return_img_type(img_content)}

            return img_data_dict
        else:
            return False

    def __del_img_data(self, img_filename):
        """Delete the image contents from Object Storage.

        """
        object_storage = oci.object_storage.ObjectStorageClient(self._oci_config)
        oci_namespace = object_storage.get_namespace().data

        try:
            objs_response = object_storage.delete_object(oci_namespace, self._objs_img_bucket, img_filename)
        except oci.exceptions.ServiceError as e:                        
            return False
        else:
            return True

    def save(self, user_id, img_filename, img_content, is_profile):
        """Save the image content into Object Storage and register the
        properties in NoSQL.

        """
        if utils.validate_id(user_id):
            new_img_filename = self.__get_new_filename(img_filename)
            img_data_dict = self.__add_img_data(new_img_filename, img_content)

            if img_data_dict:
                img_created_ts = datetime.datetime.now().strftime('%s')

                img_dict = {'image_url': '', 'image_filename': new_img_filename,
                    'image_original_filename': img_filename, 'image_host_fqdn': '', 
                    'image_uri': '', 'image_type': '', 'created_ts': img_created_ts, 
                    'user_id': user_id, 'liked_list': [], 'disliked_list': [], 
                    'main_comment': '', 'is_profile': is_profile}
                
                for k,v in img_data_dict.items():
                    img_dict[k] = img_data_dict[k]
                
                nosql = FotogalNosql()
                new_img_id = nosql.add(self._img_nosql_table, img_dict)

                return new_img_id

        return None
    
    def remove(self, user_id, img_filename):
        """Remove an image by filename.

        """        
        if utils.validate_id(user_id): 
            table = self._img_nosql_table
            conditions = 'user_id = %d AND image_filename = "%s"' % (user_id, img_filename,)    
            
            query = f'DELETE FROM {table} WHERE {conditions}'

            nosql = FotogalNosql()
            nosql_result = nosql.exec_query(table, query)

            if len(nosql_result) > 0 and nosql_result[0]['numRowsDeleted'] == 1:
                self.__del_img_data(img_filename)

                return True
            else:
                return False

        return None

    def get_img_props(self, id):
        """Return image properties.

        """
        if utils.validate_id(id):
            fields = 'id, image_filename, image_original_filename, user_id, created_ts, is_profile'
            table = self._img_nosql_table
            conditions = 'id = %d LIMIT 1' % (id,)            

            query = f'SELECT {fields} FROM {table} WHERE {conditions}'

            nosql = FotogalNosql()
            nosql_result = nosql.exec_query(table, query)

            if len(nosql_result) > 0:
                return nosql_result[0]
            
        return None

    def get_posted_imgs_list(self, user_id=None, follow_user_id=None, limit=None, offset=None):
        """Returns a list of a user's posted images

        """
        if utils.validate_id(user_id):
            posted_imgs_list = []                      

            if limit and offset:
                conditions = '(user_id = %d AND is_profile = FALSE) ORDER BY created_ts DESC LIMIT %d OFFSET %d' % (follow_user_id, limit, offset,)
            else:
                conditions = '(user_id = %d AND is_profile = FALSE) ORDER BY created_ts DESC' % (follow_user_id,)

            fields = 'id, user_id, image_filename, main_comment, created_ts,' \
                + 'liked_list[$element = %d] AS liked_by_me, disliked_list[$element = %d] AS disliked_by_me' % (user_id, user_id,)                                           

            table = self._img_nosql_table

            query = f'SELECT {fields} FROM {table} WHERE {conditions}'
           
            nosql = FotogalNosql()
            query_result = nosql.exec_query_loop(table, query)
            
            fotogal_user = FotogalUser()

            for dict_result in query_result:                
                img_username = fotogal_user.get_username(id=dict_result['user_id'])
                profile_img_url = fotogal_user.get_profile_img_url(id=dict_result['user_id'])

                if dict_result['liked_by_me'] is not None:
                    dict_result['liked_by_me'] = True
                else:
                    dict_result['liked_by_me'] = False

                if dict_result['disliked_by_me'] is not None:
                    dict_result['disliked_by_me'] = True
                else:  
                    dict_result['disliked_by_me'] = False

                dict_result.update({'username': img_username})
                dict_result.update({'profile_image_url': profile_img_url})
                dict_result.pop('user_id')

                posted_imgs_list.append(dict_result)
            
            return posted_imgs_list

    def get_user_imgs_list(self, user_id=None, limit=None, offset=None):
        """Return a list that contains the images posted by "user_id".

        """
        if utils.validate_id(user_id):
            my_imgs_list = []

            if limit and offset:
                conditions = '(user_id = %d AND is_profile = FALSE) ORDER BY created_ts DESC LIMIT %d OFFSET %d' % (user_id, limit, offset,)
            else:
                conditions = '(user_id = %d AND is_profile = FALSE) ORDER BY created_ts DESC' % (user_id,) 
                                
            fields = 'id, image_filename, image_type'

            table = self._img_nosql_table

            query = f'SELECT {fields} FROM {table} WHERE {conditions}'

            nosql = FotogalNosql()
            query_result = nosql.exec_query_loop(table, query)                      

            for dict_result in query_result:
                my_imgs_list.append(dict_result)
            
            return my_imgs_list

    def get_profile_img(self, username=None, img_filename=None):
        """Return the profile image headers and content.

        """               
        if username and utils.validate_username(username):
           profile_img_url = '/profile/%s/image/%s' % (username, img_filename,)
           conditions = 'username = "%s" AND profile_image_url = "%s" LIMIT 1' % (username, profile_img_url,)               
        else:
           return None
        
        fields = 'profile_image_url'
        table = self._usr_nosql_table

        query = f'SELECT {fields} FROM {table} WHERE {conditions}'
        
        nosql = FotogalNosql()
        nosql_result = nosql.exec_query(table, query)

        if len(nosql_result) > 0:
            (img_headers, img_content,) = self.__get_img_data(img_filename)

            return (img_headers, img_content,)

        return (None, None,)
    
    def get_data(self, request_user_id, img_owner_username, img_filename):
        """Return the image headers and content if the user requesting the
        image has following authorization.

        """
        if utils.validate_id(request_user_id) and utils.validate_username(img_owner_username):
            fotogal_user = FotogalUser()
            img_owner_user_id = fotogal_user.get_id(username=img_owner_username)

            fotogal_follow = FotogalFollow()
            
            if request_user_id == img_owner_user_id or fotogal_follow.is_following(request_user_id, img_owner_user_id):
                fields = 'image_filename, image_type'
                table = self._img_nosql_table
                conditions = 'user_id = %d AND image_filename = "%s" LIMIT 1' % (img_owner_user_id, img_filename,)                

                query = f'SELECT {fields} FROM {table} WHERE {conditions}'

                nosql = FotogalNosql()
                nosql_result = nosql.exec_query(table, query)

                if len(nosql_result) > 0:
                    (img_headers, img_content,) = self.__get_img_data(img_filename)

                    return (img_headers, img_content,)
            
        return (None, None,)

    def add_like(self, id, user_id):
        """Add the "user_id" into "liked_list" array of the "image id".

        """
        if utils.validate_id(id) and utils.validate_id(user_id):
            table = self._img_nosql_table

            fields = 'liked_list[$element = %d] AS liked_result' % (user_id,)            
            conditions = 'id = %d' % (id,)

            query = f'SELECT {fields} FROM {table} WHERE {conditions}'

            nosql = FotogalNosql()
            nosql_result = nosql.exec_query(table, query)

            if len(nosql_result) > 0 and nosql_result[0]['liked_result'] is None:
                fields = 'liked_list %d' % (user_id,)            
                conditions = 'id = %d' % (id,)

                query = f'UPDATE {table} ADD {fields} WHERE {conditions}'

                nosql = FotogalNosql()
                nosql_result = nosql.exec_query(table, query)

                if len(nosql_result) > 0 and nosql_result[0]['NumRowsUpdated'] == 1:
                    self.remove_dislike(id, user_id)

                    return True
                else:
                    return False
    
    def remove_like(self, id, user_id):
        """Remove the "user_id" from "liked_list" array of the "image id".

        """
        if utils.validate_id(id) and utils.validate_id(user_id):
            table = self._img_nosql_table

            fields = 'liked_list[$element = %d]' % (user_id,)                        
            conditions = 'id = %d' % (id,)
            
            query = f'UPDATE {table} REMOVE {fields} WHERE {conditions}'

            nosql = FotogalNosql()
            nosql_result = nosql.exec_query(table, query)

            if len(nosql_result) > 0 and nosql_result[0]['NumRowsUpdated'] == 1:
                return True
            else:
                return False

    def add_dislike(self, id, user_id):
        """Add the "user_id" into "disliked_list" array of the "img_id".

        """
        if utils.validate_id(id) and utils.validate_id(user_id):
            table = self._img_nosql_table

            fields = 'disliked_list[$element = %d] AS disliked_result' % (user_id,)                        
            conditions = 'id = %d' % (id,)
            
            query = f'SELECT {fields} FROM {table} WHERE {conditions}'

            nosql = FotogalNosql()
            nosql_result = nosql.exec_query(table, query)

            if len(nosql_result) > 0 and nosql_result[0]['disliked_result'] is None:
                fields = 'disliked_list %d' % (user_id,)            
                conditions = 'id = %d' % (id,)

                query = f'UPDATE {table} ADD {fields} WHERE {conditions}'

                nosql = FotogalNosql()
                nosql_result = nosql.exec_query(table, query)

                if len(nosql_result) > 0 and nosql_result[0]['NumRowsUpdated'] == 1:
                    self.remove_like(id, user_id)

                    return True
                else:
                    return False

    def remove_dislike(self, id, user_id):
        """Remove the "user_id" from "disliked_list" array of the "img_id".

        """
        if utils.validate_id(id) and utils.validate_id(user_id):
            table = self._img_nosql_table

            fields = 'disliked_list[$element = %d]' % (user_id,)                        
            conditions = 'id = %d' % (id,)
            
            query = f'UPDATE {table} REMOVE {fields} WHERE {conditions}'

            nosql = FotogalNosql()
            nosql_result = nosql.exec_query(table, query)

            if len(nosql_result) > 0 and nosql_result[0]['NumRowsUpdated'] == 1:
                return True
            else:
                return False

    def get_posted_imgs_total(self, user_id):
        """Return the total count of images posted by a "user_id".

        """
        if utils.validate_id(user_id):
            fields = 'count(image_filename) AS total'
            table = self._img_nosql_table
            conditions = 'user_id = %d AND is_profile = FALSE' % (user_id,)

            query = f'SELECT {fields} FROM {table} WHERE {conditions}'

            nosql = FotogalNosql()
            nosql_result = nosql.exec_query(table, query)

            if len(nosql_result) > 0:
                return nosql_result[0]['total']
            else:
                return 0  



    












                 


