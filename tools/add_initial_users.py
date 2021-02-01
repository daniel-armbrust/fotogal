#!/usr/bin/env python3

#
# This script will add some initial users in the application.
#

import sys
import os
import datetime
import random
import string
import time
import tarfile
import shutil

import oci
from borneo.iam import SignatureProvider
from borneo import NoSQLHandle, NoSQLHandleConfig, Regions, PutRequest, QueryRequest
from werkzeug.security import generate_password_hash

## OCI
oci_config_file = '../fotogal/oci_config/oci.conf'
oci_private_key = '../fotogal/oci_config/oci_api_key.pem'
oci_compartment_ocid = 'ocid1.compartment.oc1..aaaaaaaaro7baesjtceeuntyqxajzotsthm4bg46bwumacmbltuhw6gvb2mq'

oci_config = oci.config.from_file(oci_config_file, 'DEFAULT')
oci_config['key_file'] = oci_private_key

## OCI NoSQL
nosql_sig_prov = SignatureProvider(
  tenant_id=oci_config['tenancy'],
  user_id=oci_config['user'],
  private_key=oci_config['key_file'],
  fingerprint=oci_config['fingerprint']
)

nosql_config = NoSQLHandleConfig(Regions.SA_SAOPAULO_1).set_authorization_provider(nosql_sig_prov).set_default_compartment(oci_compartment_ocid)
nosql_handler = NoSQLHandle(nosql_config)

## OCI Object Storage
object_storage = oci.object_storage.ObjectStorageClient(oci_config)


def return_random_string():
  RANDOM_STR_LENGTH = 50

  ts = datetime.datetime.now().strftime('%s')

  letters_and_digits = string.ascii_letters + string.digits
  result_str = ''.join((random.choice(letters_and_digits) for i in range(RANDOM_STR_LENGTH))) + '_' + ts

  return result_str


def return_new_filename(original_filename):
  try:
    file_ext = original_filename.split('.')[1]
  except IndexError:
    file_ext = 'unknown'

  random_str = return_random_string()

  new_filename = random_str + '.' + file_ext

  return new_filename


def return_objectstorage_image_hostname(image_url):
  """ Return the host fqdn portion of OCI Object Storage Image URL.

  """
  str_temp_1 = image_url[image_url.find('/') + 2:]
  image_host_fqdn = str_temp_1[:str_temp_1.find('/')]

  return image_host_fqdn


def return_objectstorage_image_uri(image_url):
  """ Return the URI portion of OCI Object Storage Image URL.

  """
  str_temp_1 = image_url[image_url.find('/') + 2:]
  image_uri = str_temp_1[str_temp_1.find('/'):]

  return image_uri


def pause():
  print('Sleeping ...')
  time.sleep(random.randint(3, 5))


def load_img_objectstorage(img_filepath, user_id, username, is_profile=False, comment=''):
  """ Load an image to OCI Object Storage

  """  
  img_content = open(img_filepath, 'rb').read()

  original_filename = img_filepath[img_filepath.index('/')+1:]
  new_filename = return_new_filename(original_filename)

  oci_namespace = object_storage.get_namespace().data
  objs_response = object_storage.put_object(oci_namespace, 'fotogal_bucket_images', new_filename, img_content)

  # Calcula uma data de criacao.
  datetime_now_obj = datetime.datetime.now()
  timedelta_obj = datetime.timedelta(hours=(random.randint(1, 6)))
  datetime_calc = datetime_now_obj - timedelta_obj
  img_created_ts = datetime_calc.strftime('%s') 

  nosql_img_data = {'image_url': '', 'image_filename': new_filename,
     'image_original_filename': original_filename, 'image_host_fqdn': '', 'image_uri': '',
     'image_type': 'jpeg', 'created_ts': img_created_ts, 'user_id': user_id, 'liked_list': [],
     'disliked_list': [], 'main_comment': comment, 'is_profile': is_profile}

  if objs_response.status == 200:
    nosql_img_data['image_url'] = objs_response.request.url
    nosql_img_data['image_host_fqdn'] = return_objectstorage_image_hostname(nosql_img_data['image_url'])
    nosql_img_data['image_uri'] = return_objectstorage_image_uri(nosql_img_data['image_url'])

    nosql_request = PutRequest().set_table_name('fotogal_ntable_images')
    nosql_request.set_value(nosql_img_data)
    nosql_put_result = nosql_handler.put(nosql_request)

    return new_filename

  else:
    print('Error! Cannot save the image into Object Storage!')
    sys.exit(1)


def add_new_user(user_data_dict):
   nosql_request = PutRequest().set_table_name('fotogal_ntable_users')
   nosql_request.set_value(user_data_dict)
   nosql_put_result = nosql_handler.put(nosql_request)

   user_saved_id = nosql_put_result.get_generated_value()

   return user_saved_id


def update_user_img_profile(user_id, username, email, profile_img_url):
  sql = 'UPDATE fotogal_ntable_users SET profile_image_url = "%s" WHERE id = %d AND username = "%s" AND email = "%s"' % (profile_img_url, user_id, username, email,)
  nosql_request = QueryRequest().set_statement(sql)
  nosql_result = nosql_handler.query(nosql_request).get_results()


def get_user_id(username):
  sql = 'SELECT id FROM fotogal_ntable_users WHERE username = "%s" LIMIT 1' % (username,)
  nosql_request = QueryRequest().set_statement(sql)
  nosql_result = nosql_handler.query(nosql_request).get_results()
  
  return nosql_result[0]['id']

def main():
  users_to_load = {0: {'email': 'ludimila@gmail.com', 'full_name': 'Ludimila da Silva',
                      'username': 'ludimilaoficial', 'password': '1234asAS()2mjca',
                      'follow_list': [], 'follow_sent_list': [], 'follow_you_list': [], 'follow_received_list': [],
                      'created_ts': 1606855555, 'is_private': False, 'is_professional_account': True,
                      'profile_image_url': '',
                      'user_data': {                        
                        'birthday_ts': '', 'website': 'www.ludimilaoficial.com.br',
                        'bio': '', 'gender': 'Feminino', 'phone_number': ''
                      }
                  },
                  1: {'email': 'contato@postoshell.com.br', 'full_name': 'Posto Shell',
                     'username': 'postoshell', 'password': '0303SJSsm###@am',
                     'follow_list': [], 'follow_sent_list': [], 'follow_you_list': [], 'follow_received_list': [],
                     'created_ts': 1606855555, 'is_private': False, 'is_professional_account': True,
                     'profile_image_url': '',
                     'user_data': {                        
                        'birthday_ts': '', 'website': 'www.postoshell.com.br',
                        'bio': '', 'gender': 'Masculino', 'phone_number': ''
                     }
                  },
                  2: {'email': 'larry.ellison@oracle.com', 'full_name': 'Larry Ellison',
                     'username': 'larry.ellison', 'password': 'asaki#@!#$as#3',
                     'follow_list': [], 'follow_sent_list': [], 'follow_you_list': [], 'follow_received_list': [],
                     'created_ts': 1606855555, 'is_private': True, 'is_professional_account': True,
                     'profile_image_url': '',
                     'user_data': {                        
                        'birthday_ts': '', 'website': 'www.oracle.com',
                        'bio': '', 'gender': 'Masculino', 'phone_number': ''
                     }
                  },
                  3: {'email': 'xuxa@globo.com', 'full_name': 'Maria da Graça Xuxa Meneghel',
                     'username': 'xuxa.meneghel', 'password': 'sos#)3mc1-9ssss0m',
                     'follow_list': [], 'follow_sent_list': [], 'follow_you_list': [], 'follow_received_list': [],
                     'created_ts': 1606855555, 'is_private': True, 'is_professional_account': True,
                     'profile_image_url': '',
                     'user_data': {                        
                        'birthday_ts': '', 'website': 'www.xuxa.com.br',
                        'bio': '', 'gender': 'Feminino', 'phone_number': ''
                     }
                  },
                  4: {'email': 'linus@linux.com', 'full_name': 'Linus Torvalds',
                     'username': 'linustorvalds', 'password': 'ssosososmcm#$#####',
                     'follow_list': [], 'follow_sent_list': [], 'follow_you_list': [], 'follow_received_list': [],
                     'created_ts': 1606855555, 'is_private': False, 'is_professional_account': True,
                     'profile_image_url': '',
                     'user_data': {                        
                        'birthday_ts': '', 'website': 'www.xuxa.com.br',
                        'bio': '', 'gender': 'Masculino', 'phone_number': ''
                     }
                  }}

  profile_img_list = ['ludmila-profile-img.jpg', 'shell-profile-img.jpg', 'larry-profile-img.jpg',
    'xuxa-profile-img.jpg', 'linux_torvalds-profile-img.jpg']

  post_img_dict = {
    0: [
         {'img': 'ludmila_1.jpg', 'main_comment': u'Eu tirando foto pra TV!!!!!!'},
         {'img': 'ludmila_2.jpg', 'main_comment': u'Meninassss do sertãooo!!!! Seguraaaaaaa!!!!!!!!!!!'},
         {'img': 'ludmila_3.jpg', 'main_comment': u'Chutou é GOOOLLLL!'},
         {'img': 'ludmila_4.jpg', 'main_comment': u'FOTO!'},
         {'img': 'ludmila_5.jpg', 'main_comment': u'Eu, Eu, Eu ... tirando foto.'}
       ],
    1: [
         {'img': 'postoshell_1.jpg', 'main_comment': u'vem pro Posto Shell ...'},
         {'img': 'postoshell_2.jpg', 'main_comment': u'vem pro Posto Shell ...'},
         {'img': 'postoshell_3.jpg', 'main_comment': u'vem pro Posto Shell ...'},
         {'img': 'postoshell_4.jpg', 'main_comment': u'vem pro Posto Shell ...'},
         {'img': 'postoshell_5.jpg', 'main_comment': u'vem pro Posto Shell ...'}
       ],
    2: [
         {'img': 'larry_1.jpg', 'main_comment': u'#Larry'},
         {'img': 'larry_2.jpg', 'main_comment': u'#LarryEllison'},
         {'img': 'larry_3.jpg', 'main_comment': u'#Ellison'},
         {'img': 'larry_4.jpg', 'main_comment': u'Larry Ellison'},
       ],
    3: [
         {'img': 'xuxa_1.jpg', 'main_comment': u'Tudo que vamos levar desta vida é a forma como vivemos cada momento dela.'},
         {'img': 'xuxa_2.jpg', 'main_comment': u'Não julgue quem eu sou, porque você não sabe de onde eu vim.'},
         {'img': 'xuxa_3.jpg', 'main_comment': u'Quem me conhece me valoriza, me quer bem e tranquiliza. Sou quem sou e quem tenho!'},
         {'img': 'xuxa_4.jpg', 'main_comment': u'Reconheça seus limites, mas nunca duvidando das suas capacidades.'},
       ],
    4: [
         {'img': 'linus_1.jpg', 'main_comment': u'Deus abre o caminho, mas é você que o tem de percorrer.'},
         {'img': 'linus_2.jpg', 'main_comment': u'Mantendo o foco no que é importante e verdadeiro, pois o resto é passageiro.'},
         {'img': 'linus_3.jpg', 'main_comment': u'Você sempre sabe quando não fez o suficiente, mas você nunca sabe quando fez demais.'},
         {'img': 'linus_4.jpg', 'main_comment': u'A vida é muito curta para ser pequena.'},
         {'img': 'linus_5.jpg', 'main_comment': u'Não é por surgirem algumas nuvens escuras que eu deixarei de olhar o céu.'}
       ]}

  imgs_targz = 'imgs.tar.gz'
  imgs_tmpdir = 'imgstmp/'

  print('FotoGal')
  print('Loading data ....')

  if (not os.path.isfile(oci_config_file)) and (not os.path.isfile(oci_private_key)):
    print('Error! Could not open "%s" or "%s".' % (oci_config_file, oci_private_key,))
    sys.exit(1)

  # uncompress images
  if not os.path.isfile(imgs_targz):
    print('Error! Image file does not exists: "%s".' % (imgs_targz,))
    sys.exit(1)

  os.mkdir(imgs_tmpdir)  
  tar = tarfile.open(imgs_targz, 'r:gz')

  for tar_data in tar:
    tar.extract(tar_data, imgs_tmpdir)
  tar.close()  

  for i, user_data in users_to_load.items():
    profile_img_path = imgs_tmpdir + profile_img_list[i]

    if not os.path.isfile(profile_img_path):
      print('Error! Could not load the image file: %s' % (profile_img_path,))  
      continue
 
    # Save the new user and return the NoSQL ID
    user_data['password'] = generate_password_hash(user_data['password'])
    new_user_saved_id = add_new_user(user_data)
    user_id = new_user_saved_id

    # Profile Image URL
    new_filename = load_img_objectstorage(img_filepath=profile_img_path, user_id=user_id, username=user_data['username'], is_profile=True)
    profile_img_url = '/profile/' + user_data['username'] + '/image/' + new_filename    
    update_user_img_profile(user_id, user_data['username'], user_data['email'], profile_img_url)   
    
    # User post images
    post_list = post_img_dict[i]

    for post_dict in post_list:
      post_img_path = imgs_tmpdir + post_dict['img']
      post_comment = post_dict['main_comment']

      if not os.path.isfile(post_img_path):
        print('Error! Could not load the image file: %s' % (post_img_path,))
        continue  

      new_post_filename = load_img_objectstorage(img_filepath=post_img_path, user_id=user_id, username=user_data['username'], comment=post_comment)        
      pause()


  nosql_handler.close()

  shutil.rmtree(imgs_tmpdir)

  # remove borneo logs dir.
  if os.path.isdir('logs/'):
    shutil.rmtree('logs/')

  print('Done ...')
  sys.exit(0)


if __name__ == '__main__':
  main()
else:
  sys.exit(1)
