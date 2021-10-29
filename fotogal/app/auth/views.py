#
# fotogal/app/auth/views.py
#

from flask import flash as flask_flash, request, render_template 
from flask import make_response, redirect, current_app, url_for, session

from . import auth
from .forms import LoginForm
from .auth_utils import ensure_logged_in

from app.modules import utils
from app.modules.fotogal_user import FotogalUser
from app.modules.fotogal_authcookie import FotogalAuthCookie


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():    
            email = request.form.get('email')
            password = request.form.get('password')

            fotogal_user = FotogalUser()

            if fotogal_user.exists(email=email) and fotogal_user.check_passwd(email=email, passwd=password):
                user_id = fotogal_user.get_id(email=email)
                username = fotogal_user.get_username(id=user_id)

                auth_cookie = FotogalAuthCookie()

                (cookie_name, cookie_value, expire_ts,) = auth_cookie.create(user_id)

                if cookie_value and expire_ts:
                    cookie_secure = current_app.config.get('AUTH_COOKIE_SECURE')
                    cookie_httponly = current_app.config.get('AUTH_COOKIE_HTTPONLY')          
      
                    # Save session values after login
                    session['user_id'] = user_id
                    session['username'] = username                   

                    resp = make_response(redirect(url_for('main.index')))
                    # set_cookie(key, value='', max_age=None, expires=None, path='/', 
                    # domain=None, secure=False, httponly=False, samesite=None)
                    # TODO: samesite
                    resp.set_cookie(cookie_name, value=cookie_value, max_age=expire_ts, \
                        secure=cookie_secure, httponly=cookie_httponly)

                    return resp

                else:
                    # TODO: generate a log message for this error.
                    redirect(url_for('auth.login'))

            else:  
                flask_flash(u'Nome de usuário ou Senha inválido(s)!', 'error')      
        
        else:
            flask_flash(u'Erro ao processar o formulário!', 'error')      
    
    return render_template('login.html', form=form)


@auth.route('/logoff', methods=['GET'])
@ensure_logged_in
def logoff():
    user_id = session['user_id']

    if utils.validate_id(user_id):
        auth_cookie_name = current_app.config.get('AUTH_COOKIE_NAME')
        auth_cookie_secure = current_app.config.get('AUTH_COOKIE_SECURE')
        auth_cookie_httponly = current_app.config.get('AUTH_COOKIE_HTTPONLY')       

        auth_cookie_value = request.cookies.get(auth_cookie_name, '')  

        auth_cookie = FotogalAuthCookie()
        auth_cookie.remove(auth_cookie_value, user_id)

        resp = make_response(redirect(url_for('auth.login')))
        resp.set_cookie(auth_cookie_name, '', expires=0, secure=auth_cookie_secure, httponly=auth_cookie_httponly)

        session.clear()

        return resp

    else:
        return redirect(url_for('main.index'))