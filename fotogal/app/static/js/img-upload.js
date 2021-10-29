Dropzone.options.myDropzone = {    
    acceptedFiles: 'image/*',
    paramName: 'upload_img_file',
    headers: {
        'X-CSRFToken': CSRF_TOKEN
    },
    autoProcessQueue: false,    
    addRemoveLinks: true,
    maxFiles: 3,

    dictRemoveFile: 'Remover',
    dictDefaultMessage: '<p class="h3">Clique aqui ou arraste suas imagen(s) pra cá!</p>', 
    dictResponseError: '<span class="text-danger">ERRO ao enviar o(s) arquivo(s). Tente novamente mais tarde ...</span>',   
    dictCancelUpload: 'Cancelar',
    dictCancelUploadConfirmation: 'Deseja cancelar o envio?',
    dictMaxFilesExceeded: 'Número máximo de arquivos excedido!',    
  
    init: function() {
      var submitButton = document.querySelector('#id_upload_all_img_files');
          myDropzone = this; // closure
  
      submitButton.addEventListener("click", function() {
          myDropzone.processQueue(); // Tell Dropzone to process all queued files.
      });
        
      this.on('addedfile', function() {          
          $('#id_upload_all_img_files').prop('disabled', false);
      });

      this.on('removedfile', function() {  

          var totalImages = $('form').find('img').length;

          if (totalImages === 0)         
            $('#id_upload_all_img_files').prop('disabled', true);
      });

      this.on('success', function(file, responseText) {
          
          var imgId = responseText.image_id;
          var imgOwner = responseText.image_owner;
          var profileImgUrl = responseText.profile_image_url;          
          var uploadedImgUrl = responseText.image_url;                    

          showMyPost(imgId, imgOwner, profileImgUrl, uploadedImgUrl);          
      });

      this.on('complete', function(file) {          

          myDropzone.removeAllFiles();
          
      }); 

      this.on("maxfilesexceeded", function(file) {
          myDropzone.removeFile(file);
      }); 

    }
};
  