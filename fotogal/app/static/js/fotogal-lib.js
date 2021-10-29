/*
 * fotogal-lib.js
 *
 */

function addRemoveLikeDislike(imageId, action) {         
         
    var likeImageId = 'id_img_like_' + imageId;
    var dislikeImageId = 'id_img_dislike_' + imageId;

    if (action === 'like') {

      var currentImageSrc = $('#' + likeImageId).attr('src');            
      var ajaxUrl = URL_API_LIKE;
      var httpMethod = '';

      if (currentImageSrc === IMAGE_LIKE_SRC_DEFAULT)
        httpMethod = 'PUT';
      else if (currentImageSrc === IMAGE_SRC_LIKED)
        httpMethod = 'DELETE';
      else
        return false;
      
      sendAjaxLikeDislike(ajaxUrl, httpMethod, imageId, action);

      return true;

    } else if (action === 'dislike') {
     
      var currentImageSrc = $('#' + dislikeImageId).attr('src');
      var ajaxUrl = URL_API_DISLIKE;
      var httpMethod = '';

      if (currentImageSrc === IMAGE_DISLIKE_SRC_DEFAULT)
        httpMethod = 'PUT';
      else if (currentImageSrc === IMAGE_SRC_DISLIKED)   
        httpMethod = 'DELETE';
      else
        return false;
                  
      sendAjaxLikeDislike(ajaxUrl, httpMethod, imageId, action);

      return true;

    } else {
       return false;
    }         
}

function sendAjaxLikeDislike(url, httpMethod, imageId, action) {                
    
    var likeImageId = 'id_img_like_' + imageId;
    var dislikeImageId = 'id_img_dislike_' + imageId;

    var likeAnchorId = 'id_a_like_' + imageId;
    var dislikeAnchorId = 'id_a_dislike_' + imageId;

    var currentLikeImageSrc = $('#' + likeImageId).attr('src');
    var currentDislikeImageSrc = $('#' + dislikeImageId).attr('src');

    $.ajax({
          url: url,
          type: httpMethod,
          data: {'image_id': imageId},
          beforeSend: function(xhr) {

             xhr.setRequestHeader('X-CSRFToken', CSRF_TOKEN);

             $('#' + likeAnchorId).click(function(e) { e.preventDefault(); });
             $('#' + dislikeAnchorId).click(function(e) { e.preventDefault(); });

             $('#' + likeImageId).attr('src', IMAGE_LIKED_SRC_IN_PROGRESS);
             $('#' + dislikeImageId).attr('src', IMAGE_DISLIKE_SRC_IN_PROGRESS);

          },
          success: function() {
                              
             if (action === 'like') {
               
               if (httpMethod === 'PUT')
                 $('#' + likeImageId).attr('src', IMAGE_SRC_LIKED);
               else
                 $('#' + likeImageId).attr('src', IMAGE_LIKE_SRC_DEFAULT);                                         

               $('#' + dislikeImageId).attr('src', IMAGE_DISLIKE_SRC_DEFAULT);

             } else {

               if (httpMethod === 'PUT')
                 $('#' + dislikeImageId).attr('src', IMAGE_SRC_DISLIKED);
               else
                 $('#' + dislikeImageId).attr('src', IMAGE_DISLIKE_SRC_DEFAULT);

               $('#' + likeImageId).attr('src', IMAGE_LIKE_SRC_DEFAULT);
             }

          },
          error: function() {

            $('#' + likeImageId).attr('src', currentLikeImageSrc);
            $('#' + dislikeImageId).attr('src', currentDislikeImageSrc);

          }
    });
}

function showPhotoDeleteModal(modalContainerId, photoHtmlId, colHtmlId) {
  
   var modalDialogHtml = `<div class="modal fade" id="id_modal_delete_photo" tabindex="-1" role="dialog" 
                               aria-labelledby="id_modal_delete_photo_label" aria-hidden="true">
                             <div class="modal-dialog">
                               <div class="modal-content">
                                  <div class="modal-header">
                                     <h5 class="modal-title" id="id_modal_delete_photo_label">Confirme</h5>
                                     <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                     </button>
                                  </div>
                                  <div class="modal-body">
                                     <p class="h5">Deseja realmente excluír esta foto?</p>
                                  </div>
                                  <div class="modal-footer">                  
                                     <button type="button" class="btn btn-danger" data-dismiss="modal">Não</button>
                                     <button type="button" class="btn btn-success" data-dismiss="modal"
                                             onclick="sendAjaxPhotoDelete('${photoHtmlId}', '${colHtmlId}');">Sim</button>
                                     </div>
                                  </div>
                             </div>
                          </div>`;

   $('#' + modalContainerId).html(modalDialogHtml);   
   $('#id_modal_delete_photo').modal('show');  
}

function showErrorModal(msg) {

  if (! msg)
    msg = 'Erro ao processar sua requisição! Por favor, tente novamente mais tarde.';

  var modalDialogHtml = `<div class="modal fade" id="id_modal_alert" tabindex="-1" role="dialog" 
                              aria-labelledby="id_modal_alert_label" aria-hidden="true">
                            <div class="modal-dialog">
                              <div class="modal-content">
                                 <div class="modal-header">
                                    <h5 class="modal-title" id="id_modal_alert_label">Erro!</h5>
                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                      <span aria-hidden="true">&times;</span>
                                    </button>
                                 </div>
                                 <div class="modal-body">
                                    ${msg}                          
                                 </div>
                                 <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>                                  
                                 </div>
                              </div>
                            </div>
                         </div>`;

  $('#id_error_modal').html(modalDialogHtml);   
  $('#id_modal_alert').modal('show');    
}

function sendAjaxPhotoDelete(photoHtmlId, colHtmlId) {

   var photoUrl = $('#' + photoHtmlId).attr('src');

   $.ajax({
     url: photoUrl,
     type: 'DELETE',     
     beforeSend: function(xhr) {
        $('#' + colHtmlId).remove();
        xhr.setRequestHeader('X-CSRFToken', CSRF_TOKEN);
     }});
}

function sendFollowRequest(url, userId, userFollowId, isPrivate) {

  var idDivFollowPrefix = 'id_follow_' + userFollowId;
  var htmlFollowBtn = `<button type="button" class="btn btn-primary font-weight-bold" id="id_btn_follow_${userFollowId}" onclick="sendFollowRequest('${url}', '${userId}', '${userFollowId}', ${isPrivate});">Seguir</button>`;
  var htmlFollowingBtn = '<button type="button" class="btn btn-light font-weight-bold" disabled>Seguindo</button>';           
  var htmlRequestedBtn = '<button type="button" class="btn btn-light font-weight-bold" disabled>Solicitado</button>';           
  var htmlAjaxLoading = `<img src="${AJAX_BTN_FOLLOW_IMG_URL}" class="img-fluid" alt="Loading">`;
  
  $.ajax({
        url: url,
        type: 'PUT',
        data: {'user_id': userId, 'user_follow_id': userFollowId},
        beforeSend: function(xhr) {
            
            xhr.setRequestHeader('X-CSRFToken', CSRF_TOKEN);

            $('#' + idDivFollowPrefix).empty();
            $('#' + idDivFollowPrefix).html(htmlAjaxLoading);
        },
        success: function() {

            $('#' + idDivFollowPrefix).empty();

            if (isPrivate) 
              $('#' + idDivFollowPrefix).html(htmlRequestedBtn);
            else
              $('#' + idDivFollowPrefix).html(htmlFollowingBtn);
        },
        error: function() {
           
            $('#' + idDivFollowPrefix).empty();

            if (isPrivate)
              $('#' + idDivFollowPrefix).html(htmlRequestedBtn); 
            else
              $('#' + idDivFollowPrefix).html(htmlFollowingBtn);

            showErrorModal();
        }
  });
}

function showUserTimeline(url) {  

    $.when(       

      $.ajax({
        url: url,
        cache: false,
        type: 'GET',
        beforeSend: function() {     
                      
            var ajaxImgHtml = `<br><img class="img-fluid" src="${AJAX_LAZY_IMG_URL_PATH}" alt="Loading..."><br>`;

            $('#id_img_ajax_load').append(ajaxImgHtml);
        },
        complete: function() {

            $('#id_img_ajax_load').empty();          
        },
        error: function() {
           showErrorModal();
        }
      })

    ).then(function(respData, textStatus, jqXHR) {

        $(function() {
            $('.lazy').Lazy();
        });

        var imageList = respData.image_list;
        
        for (var i = 0 ; i < imageList.length ; i++) { 
          var imageOwnerUsername = imageList[i].username;
          var profileImageUrl = imageList[i].profile_image_url;
          var imageFilename = imageList[i].image_filename;
          var imageMainComment = imageList[i].main_comment;
          var imageId = imageList[i].id;
          var likedByMe = imageList[i].liked_by_me;
          var dislikedByMe = imageList[i].disliked_by_me;
        
          var imageUrl = '/' + imageOwnerUsername + '/image/' + imageFilename;

          var likeImageSrc;                 
          var dislikeImageSrc;

          if (! profileImageUrl)
            profileImageUrl = '/static/img/no-picture.png';

          if (likedByMe)
            likeImageSrc = IMAGE_SRC_LIKED;                 
          else 
            likeImageSrc = IMAGE_LIKE_SRC_DEFAULT;                   
                          
          if (dislikedByMe) 
            dislikeImageSrc = IMAGE_SRC_DISLIKED;                                    
          else 
            dislikeImageSrc = IMAGE_DISLIKE_SRC_DEFAULT;        
            
          var htmlStr = `
              <div class="row pt-4 pb-4">
                    <div class="col-md">
                      <div class="bg-white shadow border w-100 p-4">
                          <article>
                            <header>
                                <a class="text-decoration-none" href="/profile/${imageOwnerUsername}">
                                  <div class="text-left">                                       
                                      <img class="lazy img-fluid float-left rounded-circle" style="width: 50px; border: 2px solid #810BD3;"
                                        src="${AJAX_LAZY_IMG_URL_PATH}"
                                        data-src="${profileImageUrl}" title="${imageOwnerUsername}" alt="${imageOwnerUsername}">
                                      <p class="font-weight-bold pt-2">&nbsp;&nbsp;${imageOwnerUsername}</p>   
                                      <br>
                                  </div>      
                                </a>                              
                            </header>                                    
                            <div class="row">
                                <div class="col-md">
                                  <img class="lazy img-fluid rounded pt-2 pb-2" src="${AJAX_LAZY_IMG_URL_PATH}" 
                                       id="id_follow_user_img_${imageId}"
                                       data-src="${imageUrl}" title="" alt="${imageMainComment}">
                                  <h3 class="pt-2 h5 text-left">${imageMainComment}</h3>
                                </div>
                            </div>   
                            <div class="row pt-2">
                                <div class="col-md text-left">
                                    <a class="text-decoration-none" id="id_a_like_${imageId}" 
                                      href="javascript:void(0);" onclick="return addRemoveLikeDislike(${imageId}, 'like');">
                                      <img class="img-fluid" id="id_img_like_${imageId}" title="Eu gostei" alt="Eu gostei" style="width: 30px;"
                                          src="${likeImageSrc}">
                                    </a>
                                    &nbsp;&nbsp;
                                    <a class="text-decoration-none" id="id_a_dislike_${imageId}"
                                      href="javascript:void(0);" onclick="return addRemoveLikeDislike(${imageId}, 'dislike');">
                                      <img class="img-fluid" id="id_img_dislike_${imageId}" title="Eu não gostei" alt="Eu não gostei" style="width: 30px;"
                                          src="${dislikeImageSrc}">
                                    </a>
                                </div>
                            </div>
                          </article>
                      </div>
                    </div>
              </div>`;
          
          $('#id_timeline').append(htmlStr);
        }              
    });
}

function showMyPost(imgId, imgOwner, profileImgUrl, uploadedImgUrl) {
  
  $(function() {
    $('.lazy').Lazy();
  });
  
  var htmlStr = `
     <div class="row pt-4 pb-4">
        <div class="col-md">
          <div class="bg-white shadow border w-100 p-4">
              <article>
                <header>
                    <a class="text-decoration-none" href="#">
                      <div class="text-left">                                       
                          <img class="lazy img-fluid float-left rounded-circle" style="width: 50px; border: 2px solid #810BD3;"
                            src="${AJAX_LAZY_IMG_URL_PATH}"
                            data-src="${profileImgUrl}" title="${imgOwner}" alt="${imgOwner}">
                          <p class="font-weight-bold pt-2">&nbsp;&nbsp;${imgOwner}</p>   
                          <br>
                      </div>      
                    </a>                              
                </header>                                    
                <div class="row">
                    <div class="col-md">
                      <img class="lazy img-fluid rounded pt-2 pb-2" src="${AJAX_LAZY_IMG_URL_PATH}" 
                           id="id_follow_user_img_${imgId}"
                           data-src="${uploadedImgUrl}" title="" alt="">
                      <h3 class="pt-2 h5 text-left"></h3>
                    </div>
                </div>   
                <div class="row pt-2">
                    <div class="col-md text-left">
                        <a class="text-decoration-none" id="id_a_like_${imgId}" 
                          href="javascript:void(0);" onclick="return addRemoveLikeDislike(${imgId}, 'like');">
                          <img class="img-fluid" id="id_img_like_${imgId}" title="Eu gostei" alt="Eu gostei" style="width: 30px;"
                              src="${IMAGE_LIKE_SRC_DEFAULT}">
                        </a>
                        &nbsp;&nbsp;
                        <a class="text-decoration-none" id="id_a_dislike_${imgId}"
                          href="javascript:void(0);" onclick="return addRemoveLikeDislike(${imgId}, 'dislike');">
                          <img class="img-fluid" id="id_img_dislike_${imgId}" title="Eu não gostei" alt="Eu não gostei" style="width: 30px;"
                              src="${IMAGE_DISLIKE_SRC_DEFAULT}">
                        </a>
                    </div>
                </div>
              </article>
          </div>
        </div>
     </div>`;

   $('#id_timeline').prepend(htmlStr);
}