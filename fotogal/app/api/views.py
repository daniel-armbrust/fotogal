#
# fotogal/app/api/views.py
#

import datetime

from flask import request, jsonify, session
from werkzeug.utils import secure_filename

from . import api
from .errors import not_found, internal_server_error

from app.modules import utils
from app.auth.auth_utils import ensure_logged_in
from app.modules.fotogal_user import FotogalUser
from app.modules.fotogal_follow import FotogalFollow
from app.modules.fotogal_image import FotogalImage


@api.route('/follow', methods=['PUT'])
@ensure_logged_in
def follow():
    """Add an user into a follow list.

    """
    user_id = request.form.get('user_id', type=int)
    user_follow_id = request.form.get('user_follow_id', type=int)

    fotogal_user = FotogalUser()

    if fotogal_user.exists(id=user_id) and fotogal_user.exists(id=user_follow_id):
        fotogal_follow = FotogalFollow()
        fotogal_follow.add(user_id, user_follow_id)
        
        return jsonify({'status': '204', 'message': 'No Content'}), 204        
        
    else:
        return jsonify({'status': '404', 'message': 'Not Found'}), 404        


@api.route('/timeline', methods=['GET'])
@ensure_logged_in
def timeline():
    """Return a JSON that has the timeline of photos.
    
    """
    if 'user_settings' not in session:
        return jsonify({'status': '404', 'message': 'Not Found'}), 404

    user_id = session['user_id']
        
    # Return the "follow_list"
    fotogal_follow = FotogalFollow()
    follow_list = fotogal_follow.get_follow_list(user_id=user_id)

    # Add my id to the follow_list to get my posted images
    follow_list.append(user_id)

    if len(follow_list) > 0:        
        timeline_imgs_unordered_list = []
        posted_imgs_list = []

        fotogal_image = FotogalImage()       

        for follow_user_id in follow_list:
            posted_imgs_list = fotogal_image.get_posted_imgs_list(user_id=user_id, follow_user_id=follow_user_id)            

            for dict_tmp in posted_imgs_list:
                timeline_imgs_unordered_list.append(dict_tmp)                       
                
        # Order by created_ts
        timeline_imgs_list = utils.sort_list_by_timestamp(timeline_imgs_unordered_list)
                        
        return jsonify({'status': '200', 'message': 'OK', 'image_list': timeline_imgs_list}), 200 

    else:
        return jsonify({'status': '200', 'message': 'OK'}), 200


@api.route('/image/like', methods=['PUT', 'DELETE'])
@ensure_logged_in
def image_like():
    """Process a photo like request.

    """
    img_id = request.form.get('image_id', type=int)

    user_id = session['user_id'] 

    if utils.validate_id(img_id):
        fotogal_image = FotogalImage()

        if request.method == 'PUT':
            fotogal_image.add_like(img_id, user_id)      
        elif request.method == 'DELETE':
            fotogal_image.remove_like(img_id, user_id)
        
        return jsonify({'status': '200', 'message': 'OK'}), 200

    else:
        return jsonify({'status': '400', 'message': 'Bad Request'}), 400


@api.route('/image/dislike', methods=['PUT', 'DELETE'])
@ensure_logged_in
def image_dislike():
    """Process a photo dislike request.

    """
    img_id = request.form.get('image_id', type=int)

    user_id = session['user_id']

    if utils.validate_id(img_id):
        fotogal_image = FotogalImage()

        if request.method == 'PUT':
            fotogal_image.add_dislike(img_id, user_id)      
        elif request.method == 'DELETE':
            fotogal_image.remove_dislike(img_id, user_id)
        
        return jsonify({'status': '200', 'message': 'OK'}), 200

    else:
        return jsonify({'status': '400', 'message': 'Bad Request'}), 400


@api.route('/image/upload', methods=['POST'])
@ensure_logged_in
def upload_image():
    if 'upload_img_file' not in request.files:
        return jsonify({'status': '400', 'message': 'Bad Request'}), 400        

    img_data = request.files['upload_img_file']
    img_filename = secure_filename(img_data.filename)
    
    if utils.allowed_img_ext(img_filename):           
        img_content = img_data.read()
        img_type = utils.return_img_type(img_content)    

        if img_type:            
            user_id = session['user_id']
            username = session['username']

            fotogal_image = FotogalImage()
            new_img_id = fotogal_image.save(user_id, img_filename, img_content, False)           

            if new_img_id:                
                img_data_dict = fotogal_image.get_img_props(new_img_id)

                fotogal_user = FotogalUser()
                profile_img_url = fotogal_user.get_profile_img_url(id=user_id)

                new_img_filename_url = '/%s/image/%s' % (username, img_data_dict['image_filename'],)
                
                return jsonify({'status': '200', 'message': 'OK', 'image_id': new_img_id, 
                    'image_owner': username, 'profile_image_url': profile_img_url, 
                    'image_url': new_img_filename_url}), 200           

    return jsonify({'status': '400', 'message': 'Bad Request'}), 400


@api.route('/profile/image/upload', methods=['POST'])
@ensure_logged_in
def profile_image_upload():
    """Upload profile image.

    """
    if 'profile_img' not in request.files:
        return jsonify({'status': '400', 'message': 'Bad Request'}), 400
    
    img_data = request.files['profile_img']
    img_filename = secure_filename(img_data.filename)

    if not utils.allowed_img_ext(img_filename):        
        return jsonify({'status': '400', 'message': 'Bad Request'}), 400
    
    img_content = img_data.read()
    img_type = utils.return_img_type(img_content)

    if img_type:
        user_id = session['user_id']
        username = session['username']      

        fotogal_user = FotogalUser()
        fotogal_image = FotogalImage()

        current_img_url = fotogal_user.get_profile_img_url(id=user_id)
        
        if current_img_url:
            # extract the filename portion from the url.
            current_img_filename = current_img_url[current_img_url.rindex('/')+1:]

            if not fotogal_image.remove(user_id, current_img_filename):
                return jsonify({'status': '500', 'message': 'Internal Server Error'}), 500

        new_img_id = fotogal_image.save(user_id, img_filename, img_content, is_profile=True)
        img_data_dict = fotogal_image.get_img_props(new_img_id)

        profile_img_url = '/profile/%s/image/%s' % (username, img_data_dict['image_filename'],)
        profile_dict = {'profile_image_url': profile_img_url}

        if fotogal_user.update_profile_props(id=user_id, profile_dict=profile_dict):
            return jsonify({'status': '200', 'message': 'OK', 'profile_image_url': profile_img_url}), 200
    
    return jsonify({'status': '500', 'message': 'Internal Server Error'}), 500
            

@api.route('/my/images', methods=['GET'])
@ensure_logged_in
def my_images():
    """Returns a JSON that has the all images posted by a logged user.

    """
    user_id = session['user_id']  
  
    fotogal_image = FotogalImage()

    img_list = fotogal_image.get_user_imgs_list(user_id=user_id, limit=100, offset=0)

    return jsonify({'status': '200', 'message': 'OK', 'image_list': img_list}), 200