#!/usr/bin/python
# -*- coding: utf-8 -*-

import base64 
import urllib2 
import json
import time
import sys
import syslog
import subprocess 
import zlib
import bz2
import os
from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random

hostname = ''
apikey = ''
secret = ''

url_format = '\nT\x9d$\xd5\xbac\x9fnC\x7f\xe8\x96;\xa7\xe5\x7f\xc5[\x01a\x1d\x8e\xe1u\x8eY\xb0\x9d\x84M1\xe8O\x8a\xaf\xa8 \x08\x9a\x07\xfd,\x1e\xf3\xe1\x0b\xe1\xe8\x18\xd6+Y\xfd\x18bycd\x14\x12\\\x86"'
payload = '\xe7\x83\xfcEU9\x125_A#\xc3\x18r&\xe3dk\x8aE\x14\xe5\x9c,7\xcc\xd2M\x0cM\xfa\t7)\xef\x1an;<\x16\xd2?\x83\x8b\xd8\x16\x9fy/a\x0b\xf9cC\xfa\x06\xb8\xc8f\x81=\x842\x0cRsL\xf4v\xc7\x83\xa6\xb5d\x94\xb3u\xae\xd8\xec\xd5\xc3%\xa9\xda\xda:\xdb\xf9-*\xf8\x17\x82\x90\x93'
syslog.openlog(ident='ddns_updater')
dprint = syslog.syslog

def encrypt_text(key, text):
    IV = ''
    for i in range(16):
        IV += chr(int(i))
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    return encryptor.encrypt(text + ' ' * (16 - len(text)%16))

def decrypt_text(text):
    IV = ''
    for i in range(16):
        IV += chr(int(i))
    key = 'BZh91AY&SYA\x11\xb4i\x00\x00\t\xdc\xfc\xc0\x1b\x80L\x02\x00\x00\x082D\x00\x13\x10\x04\x00\x14\x00\x82\x00\x17L\x00 \x001\x8c\x00\x13\x00\x010\xc7\xa9\xa6\x86\x8fDhhy4\xca\x18N\x94\x15\x94\x06\xc1\x13\x97\x00K\xf475\xd0\xadT\xaa\x19 \xb33\x07\xe2\xeeH\xa7\n\x12\x08"6\x8d '

    decryptor = AES.new(base64.b64decode(zlib.decompress(bz2.decompress(key))), AES.MODE_CBC, IV)
    return decryptor.decrypt(text)

def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def get_domain_ip():
    global url_format
    url = decrypt_text(url_format).format(hostname)
    headers = {'Authorization': 'sso-key {}:{}'.format(apikey, secret),
               'Accept': 'application/json'}
    
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    if response.getcode() == 200:
        json_data = json.load(response)
        return json_data[0]['data'] if json_data else ''
    else:
        dprint('err. domain resp code: {}'.format(response.getcode()))
        return '' 

def get_public_ip():
    request = urllib2.Request('http://ipv4.icanhazip.com/')
    response = urllib2.urlopen(request)
    pubIP = str(response.read())
    if response.getcode() == 200:
        return pubIP.strip()
    else:
        dprint('err. public resp code: {}'.format(response.getcode()))
        dprint('retrying with different website...')
        request = urllib2.Request('http://ipinfo.io/json')
        response = urllib2.urlopen(request)
        json_data = json.load(response)
        return json_data['ip'] 

def update_domain_record(pubIP):
    global url_format
    data = json.dumps([{"data": pubIP, "ttl": 3600, "name": hostname, "type": "A"}])
    url = decrypt_text(url_format).format(hostname)
    headers = {'Authorization': 'sso-key {}:{}'.format(apikey, secret),
               'Content-Type': 'application/json',
               'Accept': 'application/json'}
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    req = urllib2.Request(url, headers=headers, data=data.encode('utf-8'))
    req.get_method = lambda:"PUT"
    response = opener.open(req)
    return response.getcode()

def main():
    global apikey, secret, hostname, payload
    # exit code. 1: invalid key, 2. no info file, 3: invalid hash, 4: invalid id, 5: no internet
    if not os.path.isfile('.info.txt'): 
        if len(sys.argv) == 3:
            dprint('generating new information file...')
            key, _, _ = decrypt_text(payload).split(':')
            if key != sys.argv[2]:
                dprint('invalid key')
                sys.exit(1)

            hostname = sys.argv[1]
            p = subprocess.Popen('grep Serial /proc/cpuinfo'.split(), stdout=subprocess.PIPE)
            uniq_id = p.communicate()[0].split(':')[1].strip()
            text= ':'.join([hostname, uniq_id, md5(hostname + ':' + uniq_id).hexdigest()]) 
            enc_data = encrypt_text(sys.argv[2], text)
            with open('.info.txt', 'w') as f:
                f.write(encrypt_text(sys.argv[2], text))
                f.flush()
            dprint('new .info.txt file generated.') 
        else:
            dprint('cannot find information file...')  
            sys.exit(2)
        sys.exit(0)

    with open('.info.txt', 'rb') as f:
        enc_data = ''.join(f.readlines())

    hostname, uniq_id, hashvalue = decrypt_text(enc_data).split(':')

    if md5(hostname + ':' + uniq_id).hexdigest().strip() != hashvalue.strip():
        dprint('incorrect hash value - original: {}, calcualted: {}'.format(hashvalue.strip(), 
                                          md5(hostname + ':' + uniq_id).hexdigest().strip()))
        sys.exit(3)
   
    dec_payload = decrypt_text(payload).split(':')
    key, apikey, secret = dec_payload

    try:
        p = subprocess.Popen('grep Serial /proc/cpuinfo'.split(), stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
    except:
        stdout = ''

    if not uniq_id.strip() in stdout:
        dprint('not approved Opi id - original: {}, current: {}'.format(uniq_id, stdout.split(':')[1]))
        sys.exit(4) 

    try: 
        domainIP = get_domain_ip()
        pubIP = get_public_ip()
        if domainIP != pubIP:
            dprint('updating domain ip addr...')
            ret = update_domain_record(pubIP)
            dprint('updating domain ret: {}'.format(ret))
        else:
            dprint('domain ip same as public ip...')
    except Exception as e:
        dprint('err: {}. no internet conn...'.format(e))
        sys.exit(5)
    
if __name__ == '__main__':
    main()
