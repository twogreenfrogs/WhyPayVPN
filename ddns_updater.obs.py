#!/usr/bin/python
# -*- coding: utf-8 -*-
te=range
tO=chr
tx=int
tY=len
tz=str
tB=repr
import base64 
l=base64.b64decode
import urllib2 
A=urllib2.HTTPHandler
F=urllib2.Request
M=urllib2.urlopen
y=urllib2.build_opener
import json
E=json.dumps
W=json.load
import time
import sys
Q=sys.exit
S=sys.argv
import syslog
o=syslog.syslog
H=syslog.openlog
import subprocess 
v=subprocess.PIPE
d=subprocess.Popen
import zlib
u=zlib.decompress
import bz2
r=bz2.decompress
from hashlib import md5
from Crypto.Cipher import AES
T=AES.MODE_CBC
D=AES.new
from Crypto import Random
t=''
e=''
O=''
x='\nT\x9d$\xd5\xbac\x9fnC\x7f\xe8\x96;\xa7\xe5\x7f\xc5[\x01a\x1d\x8e\xe1u\x8eY\xb0\x9d\x84M1\xe8O\x8a\xaf\xa8 \x08\x9a\x07\xfd,\x1e\xf3\xe1\x0b\xe1\xe8\x18\xd6+Y\xfd\x18bycd\x14\x12\\\x86"'
Y='\xe7\x83\xfcEU9\x125_A#\xc3\x18r&\xe3\x03|\xcev\xc5\n\xb0"\x81\xbb\x8c\xbc\xb2\x13/\x86\x89\x7f\xd745jt\x0f\xd4\'P\xa3\'\xfe\x8f\xe4\x11%\x81\x8cH@\r\x07\xc0\r}\xf4e:l\xa2z\xdf!F\xeaw\xb0j\xaatU\xd5D\x86\x9f\x83\x91\xb3\xdc4\xac\xde\xbd\xbd\x00\xf1W\xa7\xcf\xb2\xa21\x06|\x87j\x8cj+CDG\xeed\xf7L^\xbd'
H(ident='ddns_updater')
B=o
def f(C,R):
 IV=''
 for i in te(16):
  IV+=tO(tx(i))
 U=D(C,T,IV)
 return U.encrypt(R+' '*(16-tY(R)%16))
def G(R):
 IV=''
 for i in te(16):
  IV+=tO(tx(i))
 C='BZh91AY&SYA\x11\xb4i\x00\x00\t\xdc\xfc\xc0\x1b\x80L\x02\x00\x00\x082D\x00\x13\x10\x04\x00\x14\x00\x82\x00\x17L\x00 \x001\x8c\x00\x13\x00\x010\xc7\xa9\xa6\x86\x8fDhhy4\xca\x18N\x94\x15\x94\x06\xc1\x13\x97\x00K\xf475\xd0\xadT\xaa\x19 \xb33\x07\xe2\xeeH\xa7\n\x12\x08"6\x8d '
 h=D(l(u(r(C))),T,IV)
 return h.decrypt(R)
def b(password,salt,key_length,iv_length):
 d=K=''
 while tY(d)<key_length+iv_length:
  K=md5(K+password+salt).digest()
  d+=K
 return d[:key_length],d[key_length:key_length+iv_length]
def n():
 global x
 a=G(x).format(O)
 q={'Authorization':'sso-key {}:{}'.format(t,e),'Accept':'application/json'}
 I=F(a,headers=q)
 k=M(I)
 if k.getcode()==200:
  X=W(k)
  return X[0]['data']if X else ''
 else:
  B('err. domain resp code: {}'.format(k.getcode()))
  return '' 
def j():
 I=F('http://ipv4.icanhazip.com/')
 k=M(I)
 P=tz(k.read())
 if k.getcode()==200:
  return P.strip()
 else:
  B('err. public resp code: {}'.format(k.getcode()))
  B('retrying with different website...')
  I=F('http://ipinfo.io/json')
  k=M(I)
  X=W(k)
  return X['ip']
def i(P):
 global x
 p=E([{"data":P,"ttl":3600,"name":O,"type":"A"}])
 a=G(x).format(O)
 q={'Authorization':'sso-key {}:{}'.format(t,e),'Content-Type':'application/json','Accept':'application/json'}
 N=y(A)
 w=F(a,headers=q,data=p.encode('utf-8'))
 w.get_method=lambda:"PUT"
 k=N.open(w)
 return k.getcode()
def V():
 if tY(S)==5:
  p=d('grep Serial /proc/cpuinfo'.split(),stdout=v)
  c=p.communicate()[0].split(':')[1].strip()
  S.append(c)
  R=':'.join(S[1:])
  print(tB(f(S[1],R)))
  Q(0)
 global t,e,O
 m=G(Y).split(':')
 O,t,e,c=m[1:]
 p=d('grep Serial /proc/cpuinfo'.split(),stdout=v)
 J,L=p.communicate()
 if not c.strip()in J:
  B('Not Valid Orange Pi - original: {}, current: {}'.format(c,J.split(':')[1]))
  Q(1)
 s=n()
 P=j()
 if s!=P:
  B('updating domain ip addr...')
  g=i(P)
  B('updating domain ret: {}'.format(g))
 else:
  B('domain ip same as public ip...')
if __name__=='__main__':
 V()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

