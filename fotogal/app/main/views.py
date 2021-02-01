#
# fotogal/app/main/views.py
#

from flask import flash as flask_flash, abort as flask_abort, render_template
from flask import request, redirect, url_for, make_response, current_app
from flask import Response, session
from werkzeug.utils import secure_filename

from . import main
from .forms import RegistrationForm, ProfileForm, ProfilePasswdForm

from app.modules import utils
from app.modules.fotogal_user import FotogalUser
from app.modules.fotogal_authcookie import FotogalAuthCookie
from app.modules.fotogal_follow import FotogalFollow
from app.modules.fotogal_image import FotogalImage

from app import auth
from app.auth.auth_utils import ensure_logged_in


@main.route('/register', methods=['GET', 'POST'])
def register():
    """User registration form.

    """
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():      
            email = request.form.get('email', '')
            full_name = request.form.get('full_name', '')
            username = request.form.get('username', '')
            password = request.form.get('password', '')  

            fotogal_user = FotogalUser()

            if fotogal_user.exists(email=email) or fotogal_user.exists(username=username):
                flask_flash(u'E-mail/Nome de usuário já cadastrado(s)!', 'error')
            else:
                created_ts = utils.return_now_ts()

                new_user_dict = {'email': email, 'full_name': full_name, 
                    'username': username, 'password': password, 'follow_list': [],
                    'follow_sent_list': [], 'follow_you_list': [], 
                    'follow_received_list': [], 'created_ts': created_ts, 
                    'is_private': False, 'is_professional_account': False, 
                    'profile_image_url': '', 
                    'user_data': {
                        'birthday_ts': 0, 'website': '', 'bio': '', 'gender': '', 
                        'phone_number': ''}}

                new_user_id = fotogal_user.add_new_user(new_user_dict)

                if new_user_id:
                    auth_cookie = FotogalAuthCookie()

                    (cookie_name, cookie_value, expire_ts,) = auth_cookie.create(new_user_id)

                    cookie_secure = current_app.config.get('AUTH_COOKIE_SECURE')
                    cookie_httponly = current_app.config.get('AUTH_COOKIE_HTTPONLY')
    
                    resp = make_response(redirect(url_for('main.initial_suggestions')))
                    resp.set_cookie(cookie_name, cookie_value, max_age=expire_ts, \
                        secure=cookie_secure, httponly=cookie_httponly)

                    return resp

                else:
                    # error in creating a new user.
                    flask_flash(u'Erro ao processar o formulário!', 'error')

        else:
            flask_flash(u'Erro ao processar o formulário!', 'error')

    return render_template('register.html', form=form)  


@main.route('/', methods=['GET'])
@ensure_logged_in
def index():  
    user_id = session.get('user_id', None)
    username = session.get('username', None)    

    fotogal_user = FotogalUser()
    profile_dict = fotogal_user.get_profile_props(id=user_id)

    fotogal_image = FotogalImage()
    total_posted_images = fotogal_image.get_posted_imgs_total(user_id)

    fotogal_follow = FotogalFollow()
    following_total = fotogal_follow.get_following_total(user_id)
    
    if not following_total:
        return redirect(url_for('main.initial_suggestions'))
    else:
        # Initialize user settings
        user_settings = {'follow_list_step': 10, 'follow_list_idx_low': 0, 
            'follow_list_idx_high': 10, 'query_limit': 5, 'query_offset': 0}    

        session['user_settings'] = user_settings
    
        return render_template('index.html', user_id=user_id, username=username, 
            total_posted_images=total_posted_images, profile_dict=profile_dict)


@main.route('/initial/suggestions', methods=['GET'])
@ensure_logged_in
def initial_suggestions():
    """Show some initial suggestions to follow after registration.

    """
    user_id = session.get('user_id', None)
    
    fotogal_follow = FotogalFollow()

    following_total = fotogal_follow.get_following_total(user_id)
 
    if not following_total:
        users_to_follow = fotogal_follow.get_suggestions()

        return render_template('initial_suggestions.html', \
            users_to_follow=users_to_follow, user_id=user_id)

    else:
        return redirect(url_for('main.index'))


@main.route('/profile/<img_owner_username>/image/<img_filename>', methods=['GET'])
@ensure_logged_in
def get_image_profile_content(img_owner_username, img_filename):
    if utils.validate_username(img_owner_username) and img_filename:
        user_id = session.get('user_id', None)    

        fotogal_image = FotogalImage()
        
        (img_headers, img_content,) = fotogal_image.get_profile_img(img_owner_username, img_filename)

        if img_headers and img_content:
            resp = Response(img_content)

            for k,v in img_headers.items():
                resp.headers.add(k, v)

            return resp

        else:
            flask_abort(404)  

    else:
        flask_abort(404)


@main.route('/<img_owner_username>/image/<img_filename>', methods=['GET', 'DELETE'])
@ensure_logged_in
def get_delete_image(img_owner_username, img_filename):
    if utils.validate_username(img_owner_username) and img_filename:        
        user_id = session.get('user_id', None)

        fotogal_image = FotogalImage()

        if request.method == 'GET':
            (img_headers, img_content,) = fotogal_image.get_data(user_id, img_owner_username, img_filename)

            if img_headers and img_content:
                resp = Response(img_content)

                for k,v in img_headers.items():
                    resp.headers.add(k, v)

                return resp

            else:
                flask_abort(404)  
            
        elif request.method == 'DELETE':            
            if fotogal_image.remove(user_id, img_filename):                
                return 'OK', 200
            else:                
                flask_abort(400)  

    else:
        flask_abort(404)  
  

@main.route('/profile/<username>', methods=['GET', 'POST'])
@ensure_logged_in
def show_profile(username):
    if utils.validate_username(username):       

        fotogal_user = FotogalUser()
        profile_dict = fotogal_user.get_profile_props(username=username)

        user_id = profile_dict.get('id', None)        
        session_user_id = session.get('user_id', None)

        if session_user_id == user_id:
            profile_owner = True
        else:
            profile_owner = False
                
        fotogal_images = FotogalImage()
        imgs_list = fotogal_images.get_user_imgs_list(user_id=user_id)
        imgs_posted_total = fotogal_images.get_posted_imgs_total(user_id)

        fotogal_follow = FotogalFollow()
        following_total = fotogal_follow.get_following_total(user_id)
        followers_total = fotogal_follow.get_followers_total(user_id)

        return render_template('profile.html', username=username, profile_owner=profile_owner,
            profile_dict=profile_dict, imgs_list=imgs_list, imgs_posted_total=imgs_posted_total,
            following_total=following_total, followers_total=followers_total) 

    flask_abort(400)


@main.route('/profile/<username>/edit', methods=['GET', 'POST'])
@ensure_logged_in
def edit_profile(username):
    fotogal_user = FotogalUser()

    if fotogal_user.exists(username=username):        
        user_id = session.get('user_id', None)
        session_username = session.get('username', None)    

        if session_username != username:
            flask_abort(404)

        form = ProfileForm()

        if request.method == 'GET':
            profile_dict = fotogal_user.get_profile_props(id=user_id)

            form.full_name.data = profile_dict['full_name']
            form.username.data = profile_dict['username']
            form.email.data = profile_dict['email']
            form.gender.data = profile_dict['user_data']['gender']
            form.website.data = profile_dict['user_data']['website']
            form.bio.data = profile_dict['user_data']['bio']
            form.is_private.data = profile_dict['is_private']

            return render_template('edit_profile.html', form=form, 
                username=username, profile_img_url=profile_dict['profile_image_url'])

        else:
            if form.validate_on_submit():
                profile_dict = {'full_name': '', 'is_private': '', 
                    'user_data': {'website': '', 'bio': '', 'gender': ''}}

                for k,v in profile_dict.items():
                    if k == 'user_data':
                        for k,v in profile_dict['user_data'].items():
                            profile_dict['user_data'][k] = request.form.get(k, '')                        
                    else:
                        profile_dict[k] = request.form.get(k, '')                                     

                if profile_dict['is_private'] == 'y':
                    profile_dict['is_private'] = True
                else:
                    profile_dict['is_private'] = False            
                
                was_updated = fotogal_user.update_profile_props(id=user_id, profile_dict=profile_dict)

                if was_updated:
                    flask_flash(u'Dados atualizados com sucesso!', 'success')      
                else:
                    flask_flash(u'Erro ao atualizar os dados do usuário!', 'error')    

            else:
                flask_flash(u'Erro ao atualizar os dados do usuário!', 'error')

            return redirect(url_for('main.edit_profile', username=username))  

    else:
        flask_abort(404)


@main.route('/profile/<username>/edit/passwd', methods=['GET', 'POST'])
@ensure_logged_in
def edit_profile_passwd(username):
    fotogal_user = FotogalUser()

    if fotogal_user.exists(username=username):
        user_id = session.get('user_id', None)
        session_username = session.get('username', None)    

        if session_username != username:
            flask_abort(404)

        profile_dict = fotogal_user.get_profile_props(id=user_id)

        form = ProfilePasswdForm()

        if request.method == 'GET':
            return render_template('edit_profile_passwd.html', form=form, 
                username=username, profile_dict=profile_dict)

        else:
            if form.validate_on_submit():
                 old_passwd = request.form.get('old_password', '')
                 new_passwd = request.form.get('new_password', '')

                 if old_passwd != new_passwd and fotogal_user.check_passwd(id=user_id, passwd=old_passwd):
                     was_updated = fotogal_user.update_passwd(id=user_id, passwd=new_passwd)

                     if was_updated:
                         flask_flash(u'Sua senha foi atualizada com sucesso!', 'success')  
                     else:
                         flask_flash(u'Erro ao atualizar a sua senha!', 'error')

                 else:
                     flask_flash(u'Erro ao atualizar a sua senha!', 'error')     

            else:
                flask_flash(u'Erro ao atualizar a sua senha!', 'error')     

            return redirect(url_for('main.edit_profile_passwd', username=username))    
    else:
        flask_abort(404)


@main.route('/about', methods=['GET'])
@ensure_logged_in
def about():
    return render_template('about.html')