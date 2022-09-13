import hvac
import sys
import base64
import json

def lambda_handler(event, context) :
    
    print("Authenticating to local proxy")
    client = hvac.Client(url='http://127.0.0.1:8200')
    # print(f" Is client authenticated: {client.is_authenticated()}")

    print("### reading kv secret")
    read_response = client.secrets.kv.v2.read_secret(mount_point='kv', path='secret')
    # print(read_response)
    print('The value under path ("/kv/secret") is: name = {value}'.format(
        value=read_response['data']['data']['name'],
    ))
    
    print("### encrypting data")
    encrypt_data_response = client.secrets.transit.encrypt_data(
        name='my-key',
        plaintext=base64.b64encode(b'some-plaintext'),
    )
    ciphertext = encrypt_data_response['data']['ciphertext']
    print('Encrypted plaintext ciphertext is: {cipher}'.format(cipher=ciphertext))
    
    print("### retrieve db creds from disk")
    try:
        f = open("/tmp/vault_secret.json", "r")
        #print(f.read())
        db_data = json.loads(f.read())

        print('Username is: {username}'.format(username=db_data['data']['username']))
        print('Password is: {password}'.format(password=db_data['data']['password']))
    except Exception as e:
        print(e)