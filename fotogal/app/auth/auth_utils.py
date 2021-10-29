#
# fotogal/app/auth/utils.py
#

from functools import wraps

from flask import request, url_for, current_app, redirect, session

from app import auth
from app.modules import utils
from app.modules.fotogal_authcookie import FotogalAuthCookie


def ensure_logged_in(fn):  
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if (not 'user_id' in session) and (not 'username' in session):            
            return redirect(url_for('auth.login'))
    
        user_id = session['user_id']
        username = session['username']

        if (not utils.validate_id(user_id)) and (not utils.validate_username(username)):            
            return redirect(url_for('auth.login'))

        cookie_name = current_app.config.get('AUTH_COOKIE_NAME')
        cookie_value = request.cookies.get(cookie_name, '')  
        
        if cookie_value:
            auth_cookie = FotogalAuthCookie()

            if not auth_cookie.validate(cookie_value, user_id):                        
                return redirect(url_for('auth.login'))  

        else:            
            return redirect(url_for('auth.login'))  
      
        return fn(*args, **kwargs)

    return wrapper