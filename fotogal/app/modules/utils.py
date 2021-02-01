#
# fotogal/app/modules/utils.py
#

"""
Utility functions for FotoGal application.
"""

import datetime
import random
import string
import re


def sort_list_by_timestamp(unsorted_list):
    if type(unsorted_list) is list:
        sorted_list_result = []
        sorted_list = []

        i = 0
        while i < len(unsorted_list):
            for item in unsorted_list[i]:
                if item == 'created_ts':
                    sorted_list.append(unsorted_list[i]['created_ts'])
            i += 1

        sorted_list.sort()

        while True:
            try:
                ts = sorted_list.pop()
            except IndexError:
                break

            for dict_items in unsorted_list:
                if dict_items['created_ts'] == ts:
                    sorted_list_result.append(dict_items)
                    break
        
        return sorted_list_result

    else:
        return None

def return_random_string():
    RANDOM_STR_LENGTH = 50

    ts = datetime.datetime.now().strftime('%s')

    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(RANDOM_STR_LENGTH))) + '_' + ts

    return result_str

def allowed_img_ext(img_filename):
    ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'gif',)

    try:
        ext = img_filename.rsplit('.', 1)[1].lower()
    except IndexError:
        return False
  
    if ext in ALLOWED_EXTENSIONS:
        return True
    else:
        return False 

def return_img_type(img_content):
    """Return the type of the image.

       https://github.com/python/cpython/blob/3.9/Lib/imghdr.py#L48

    """
    if img_content:    
        file_header = img_content[0:32]

        if file_header[6:10] in (b'JFIF', b'Exif'):
            return 'jpeg'
        elif file_header.startswith(b'\211PNG\r\n\032\n'):
            return 'png'
        elif file_header[:6] in (b'GIF87a', b'GIF89a'):
            return 'gif'
      
    return ''

def return_img_mimetype(img_type):
    """Return image MIME TYPE.

    """
    if img_type == 'jpg' or img_type == 'jpeg':
        return 'image/jpeg'
    elif img_type == 'png':
        return 'image/png'
    elif img_type == 'gif':
        return 'image/gif'
    else:
        return ''

def validate_username(username):
    """Validate username string.

    """  
    if type(username) is str and re.match(r'^[A-Za-z0-9\_\.]{3,50}$', username):
        return True
    else:
        return False  

def validate_password(passwd):
    """Validate password complexity string.

    """
    if type(passwd) is str and re.fullmatch(r'^[A-Za-z0-9@#$%^&+=]{8,30}$', passwd):
        return True
    else:
        return False  

def validate_email(email):
    """Validate e-mail string.

    """
    if type(email) is str and re.match(r'^[A-Za-z0-9]+[\._]?[A-Za-z0-9]+[@]\w+[.]\w{2,3}$', email):
        return True
    else:
        return False  

def validate_id(id):
    """Validate id number.

    """
    if type(id) is str or type(id) is int:
        id_str = str(id)   
    
        if re.match(r'^\d+$', id_str):
            return True
        else:
            return False                  
    else:
        return False

def return_now_ts():    
    return datetime.datetime.now().strftime('%s')