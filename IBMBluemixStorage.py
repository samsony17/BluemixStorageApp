import swiftclient.client as swiftclient
import gnupg
import os
 # connecting python app to VCAP services using the Object storage credentials
auth_url='https://identity.open.softlayer.com/v3'
project_id='ff46d533a01b4ba59aea034bfe8f4fa2'
user_id='6b339aa01c83485ca6bb2d540fd6ce26'
region_name='dallas'
password='Y8NfU*D[7P9Vli3Q'
conn = swiftclient.Connection(
    key='Y8NfU*D[7P9Vli3Q',
    authurl='https://identity.open.softlayer.com/v3',
    auth_version='3',
    os_options={"project_id":'ff46d533a01b4ba59aea034bfe8f4fa2',
            "user_id":'6b339aa01c83485ca6bb2d540fd6ce26',
            "region_name":'dallas'});


# creating the container in IBM bluemix
container_name='mycontainer'
file_name='example.txt'
conn.put_container('mycontainer')
print"\n Container %s created succesfully ."%container_name
print("\nContainer List:")
for container in conn.get_account()[1]:
    print container['name']


    
# uploading the file into Bluemix
conn.put_object('mycontainer',
    'samson.txt',
    contents= "i love u ",
    content_type='text/plain')
conn.put_object('mycontainer',
    'linked.txt',
    contents= "welcome to ibm bluemix",
    content_type='text/plain')

#deleting the file from Bluemix
conn.delete_object('mycontainer','linked.txt')


# listing all the object in the container
print ("\nObject List:")
for container in conn.get_account()[1]:
    for data in conn.get_container(container['name'])[1]:
        print 'object: {0}\t size: {1}\t date: {2}'.format(data['name'], data['bytes'], data['last_modified'])


        

# key generation
gpg = gnupg.GPG(gnupghome='C:\Users\samss\gnupg')
input_data = gpg.gen_key_input(key_type="RSA",
                               key_length=1024,
                               passphrase='n0sm@sy0')
key =gpg.gen_key(input_data)
print key



# encrypting the file with gpg
with open('samson.txt','rb')as f:
    status = gpg.encrypt_file(f,None,passphrase ='n0sm@sy0',symmetric='AES256',output='samson.txt.gpg')
print 'ok: ', status.ok
print 'status: ', status.status
print 'stderr: ', status.stderr




# uploading the file into  Bluemix
conn.put_object('mycontainer',
    'samson.txt.gpg',
    contents= "i love u ",
    content_type='text/plain')



# listing the files in the container
print ("\nObject List:")
for container in conn.get_account()[1]:
    for data in conn.get_container(container['name'])[1]:
        print 'object: {0}\t size: {1}\t date: {2}'.format(data['name'], data['bytes'], data['last_modified'])


#decrypting the file 
with open('samson.txt.gpg', 'rb') as f:
    status = gpg.decrypt_file(f, passphrase='n0sm@sy0', output='samson.txt')

print 'ok: ', status.ok
print 'status: ', status.status
print 'stderr: ', status.stderr
    
