#coding=utf8
import time
import requests
import json
import asn1

import base64
import math
import random
import codecs


'''
function nbi() {
	return new BigInteger(null)
}
'''
def nbi():
	return BigInteger(None)

'''
function nbv(e) {
	var t = nbi();
	t.fromInt(e);
	return t
}
'''
def nbv(e):
	t = nbi()
	t.bnpFromInt(e)
	return t


BI_RM = '0123456789abcdefghijklmnopqrstuvwxyz'

def int2char(e):
	return BI_RM[e]

BI_RC = {}
rr = ord('0');
for vv in range(10):
	BI_RC[rr] = vv
	rr += 1
rr = ord('a')
for vv in range(10,36):
	BI_RC[rr] = vv
	rr += 1
rr = ord('A')
for vv in range(10,36):
	BI_RC[rr] = vv
	rr += 1

'''
function nbits(e) {
var t = 1,i;
if (0 != (i = e >>> 16)) {
	e = i;
	t += 16
}
if (0 != (i = e >> 8)) {
	e = i;
	t += 8
}
if (0 != (i = e >> 4)) {
	e = i;
	t += 4
}
if (0 != (i = e >> 2)) {
	e = i;
	t += 2
}
if (0 != (i = e >> 1)) {
	e = i;
	t += 1
}
return t
}
'''
def nbits(e):
	t = 1
	i = e >> 16
	if 0 != i:
		e = i
		t += 16
	i = e >> 8
	if 0 != i:
		e = i
		t += 8
	i = e >> 4
	if 0 != i:
		e = i
		t += 4
	i = e >> 2
	if 0 != i:
		e = i
		t += 2
	i = e >> 1
	if 0 != i:
		e = i
		t += 1
	return t
#print(nbits(12345))

'''
function intAt(e, t) {
var i = BI_RC[e.charCodeAt(t)];
return null == i ? - 1 : i
}
'''
def intAt(e, t):
	try:
		if isinstance(e[t],int):
			i = BI_RC[e[t]]
		else:
			i = BI_RC[ord(e[t])]
	except KeyError:
		i = None

	if i == None:
		return -1
	else:
		return i

class BigInteger:

	def __init__(self, e, t=256):
		print("EEEEEE",t)
		self.e = e
		self.t = t
		self.content = {}
		self.DB = 28
		self.DM = 268435455
		self.DV = 268435456
		self.F1 = 24
		self.F2 = 4
		self.FV = 4503599627370496
		self.ONE = {0:1, 's': 0, 't':1}
		self.ZERO = {'s':0, 't':0}
		return self.bnpFromString(e,t)

	'''
	function bnpFromInt(e) {
		this.t = 1;
		this.s = e < 0 ? - 1 : 0;
		if (e > 0) this[0] = e;
 		else if (e < - 1) this[0] = e + DV;
 		else this.t = 0
	}
	'''
	def bnpFromInt(self,e):
		self.content['t'] = 1
		if e < 0:
			self.content['s'] = -1
		else:
			self.content['s'] = 0
		if e > 0:
			self.content[0] = e
		elif e < -1:
			self.content[0] = e + self.DV
		else:
			self.content['t'] = 0
	'''
	function bnSigNum() {
		if (this.s < 0) return - 1;
 		else if (this.t <= 0 || 1 == this.t && this[0] <= 0) return 0;
 		else return 1
	}
	'''
	def signum(self):
		if self.content['s'] < 0:
			return -1
		elif self.content['t'] <= 0 or self.content['t'] == 1 and self.content[0] <= 0:
			return 0
		else:
			return 1
	'''
	function bnpChunkSize(e) {
		return Math.floor(Math.LN2 * this.DB / Math.log(e))
	}
	'''
	def chunkSize(self, e):
		return math.floor(math.log(2) * self.DB / math.log(e))
	'''
	function bnpToRadix(e) {
		if (null == e) e = 10;
		if (0 == this.signum() || e < 2 || e > 36) return '0';
		var t = this.chunkSize(e);
		var i = Math.pow(e, t);
		var n = nbv(i),
		s = nbi(),
		r = nbi(),
		a = '';
		this.divRemTo(n, s, r);
		for (; s.signum() > 0; ) {
			a = (i + r.intValue()).toString(e).substr(1) + a;
			s.divRemTo(n, s, r)
		}
		return r.intValue().toString(e) + a
	}
	'''
	def bnpToRadix(self, e):
		if e == None:
			e = 10
		if self.signum() == 0 or e < 2 or e > 36:
			return '0'
		t = self.chunkSize(e)
		i = pow(e,t)
		n = nbv(i)
		s = nbi()
		r = nbi()
		a = ''
		self.divRemTo(n, s, r)
		while s.signum() > 0:
			a = (i + r.intValue()).toString(e).substr(1) + a
			s.divRemTo(n, s, r)
		return r.intValue().toString(e) + a


	'''
	function bnToString(e) {
		if (this.s < 0) return '-' + this.negate().toString(e);
		var t;
		if (16 == e) t = 4;
 		else if (8 == e) t = 3;
 		else if (2 == e) t = 1;
 		else if (32 == e) t = 5;
 		else if (4 == e) t = 2;
 		else return this.toRadix(e);
		var i = (1 << t) - 1,n,s = !1,r = '',a = this.t;
		var o = this.DB - a * this.DB % t;
		if (a-- > 0) {
			if (o < this.DB && (n = this[a] >> o) > 0) {
  			s = !0;
  			r = int2char(n)
		}
		for (; a >= 0; ) {
  			if (o < t) {
    			n = (this[a] & (1 << o) - 1) << t - o;
    			n |= this[--a] >> (o += this.DB - t)
  			} else {
    			n = this[a] >> (o -= t) & i;
    			if (o <= 0) {
      				o += this.DB;
      				--a
    			}
  			}
  			if (n > 0) s = !0;
  			if (s) r += int2char(n)
		}
	}
	return s ? r : '0'
	 }
	'''
	def bnToString(self,e):
		if self.content['s'] < 0:
			return '-' + self.negate().toString(e)
		t = 0
		if e == 16:
			t = 4
		elif e == 8:
			t = 3
		elif e == 2:
			t = 1
		elif e == 32:
			t = 5
		elif e == 4:
			t = 2
		else:
			return self.toRadix(e)
		i = (1 << t) - 1
		n = 0
		s = False
		r = ''
		a = self.content['t']
		o = self.DB - a * self.DB % t
		if a > 0:
			a -= 1
			n = self.content[a] >> o
			if o < self.DB and n > 0:
				s = True
				r = int2char(n)
				print(r)
			while a >= 0:
				if o < t:
					n = (self.content[a] & (1<<o) - 1) << t - o
					a -= 1
					o += self.DB - t
					n |= self.content[a] >> o
				else:
					o -= t
					n = self.content[a] >> o & i
					if o <= 0:
						o += self.DB
						a -= 1
				if n > 0:
					s = True
				if s:
					r += int2char(n)
		print(r)
		if s:
			return r
		else:
			return '0'

	def bnBitLength(self):
		if self.content['t'] <= 0:
			return 0
		else:
			return self.DB * (self.content['t'] - 1) + nbits(self.content[self.content['t']-1] ^ self.content['s'] & self.DM)

	'''
	function bnpClamp() {
		var e = this.s & this.DM;
		for (; this.t > 0 && this[this.t - 1] == e; ) --this.t
	}
	'''
	def bnpClamp(self):
		e = self.content['s'] & self.DM
		while self.content['t'] > 0 and self.content[self.content['t'] - 1] == e:
			self.content['t'] -= 1


	def bnpFromString(self, e, t):
		print(e,t)
		i = 0
		if t == 16:
			i = 4
		elif t == 8:
			i = 3
		elif t == 4:
			i = 2
		elif t == 2:
			i = 1
		elif t == 32:
			i = 5
		elif t == 256:
			i = 8
		else:
			self.fromRadix(e,t)
			return

		self.content['t'] = 0
		self.content['s'] = 0
		n = len(e)
		s = False
		r = 0
		n -= 1
		while(n>=0):
			#print(self.content)
			#print(r)
			if 8 == i:
				a = 255 & e[n]
			else:
				a = intAt(e,n)
			if not a < 0:
				s = False
				if r == 0:
					#print('-',self.content['t'], a)
					self.content[self.content['t']] = a
					self.content['t'] += 1
				elif r + i > self.DB:
					#print("####",self.content[self.content['t'] - 1], self.content['t'], a, r,"####")
					#print('--1',self.content['t']-1, self.content[self.content['t']-1] | (a & (1 << self.DB -r) - 1) << r)
					self.content[self.content['t']-1] |= (a & (1 << self.DB -r) - 1) << r
					#print('--2',self.content['t'], a >> self.DB -r)
					self.content[self.content['t']] = a >> self.DB -r
					self.content['t'] += 1
				else:
					#print("****", self.content['t'], self.content[self.content['t'] - 1], a, r,"****")
					#print('---',self.content['t']-1, self.content[self.content['t']-1] | (a<<r))
					self.content[self.content['t'] - 1] |= a << r
				r += i
				if r >= self.DB:
					r -= self.DB
			elif e[n] == '-':
				s = True
			n-=1
		if i == 8 and 0 != (128 & e[0]):
			print("BOMMM")
			self.content['s'] = -1
			if r > 0:
				self.content[self.content['t'] - 1] |= (1 << self.DB -r) -1 << r
		self.bnpClamp()






'''
function BigInteger(e, t, i) {
if (null != e) if ('number' == typeof e) this.fromNumber(e, t, i);
 else if (null == t && 'string' != typeof e) this.fromString(e, 256);
 else this.fromString(e, t)
}
'''

'''
var RSAPublicKey = function (e, t) {
this.modulus = new BigInteger(Hex.encode(e), 16);
this.encryptionExponent = new BigInteger(Hex.encode(t), 16)
};
'''
class RSAPublicKey:
	def __init__(self, e, t):
		hexstring_e = ''.join( [ "%02x"%x for x in e ] ).strip()
		hexstring_t = ''.join( [ "%02x"%x for x in t ] ).strip()
		self.modulus = BigInteger(hexstring_e, 16)
		self.encryptionExponent = BigInteger(hexstring_t, 16)




'''
var ASN1Data = function (e) {
this.error = !1;
this.parse = function (e) {
if (!e) {
  this.error = !0;
  return null
}
var t = [
];
for (; e.length > 0; ) {
  var i = e.charCodeAt(0);
  e = e.substr(1);
  var n = 0;
  if (5 == (31 & i)) e = e.substr(1);
   else if (128 & e.charCodeAt(0)) {
    var s = 127 & e.charCodeAt(0);
    e = e.substr(1);
    if (s > 0) n = e.charCodeAt(0);
    if (s > 1) n = n << 8 | e.charCodeAt(1);
    if (s > 2) {
      this.error = !0;
      return null
    }
    e = e.substr(s)
  } else {
    n = e.charCodeAt(0);
    e = e.substr(1)
  }
  var r = '';
  if (n) {
    if (n > e.length) {
      this.error = !0;
      return null
    }
    r = e.substr(0, n);
    e = e.substr(n)
  }
  if (32 & i) t.push(this.parse(r));
   else t.push(this.value(128 & i ? 4 : 31 & i, r))
}
return t
};
this.value = function (e, t) {
if (1 == e) return t ? !0 : !1;
 else if (2 == e) return t;
 else if (3 == e) return this.parse(t.substr(1));
 else if (5 == e) return null;
 else if (6 == e) {
  var i = [
  ];
  var n = t.charCodeAt(0);
  i.push(Math.floor(n / 40));
  i.push(n - 40 * i[0]);
  var s = [
  ];
  var r = 0;
  var a;
  for (a = 1; a < t.length; a++) {
    var o = t.charCodeAt(a);
    s.push(127 & o);
    if (128 & o) r++;
     else {
      var c;
      var _ = 0;
      for (c = 0; c < s.length; c++) _ += s[c] * Math.pow(128, r--);
      i.push(_);
      r = 0;
      s = [
      ]
    }
  }
  return i.join('.')
}
return null
};
this.data = this.parse(e)
};
'''
class ASN1Data:

	def __init__(self, e):
		print("new ASN1Data")
		self.error = False
		self.data = self.parse(e)

	def parse(self,e):
		if not e:
			self.error = True
			return None
		t = []
		while len(e) > 0:
			i = e[0]
			#print("i = ",i)
			e = e[1:]
			#print("e.length = ",len(e))
			n = 0
			if 31 & i == 5:
				e = e[1:]
			elif e[0] & 128:
				s = 127 & e[0]
				e = e[1:]
				if s > 0:
					n = e[0]
				if s > 1:
					n = n << 8 | e[1]
				if s > 2:
					self.error = True
					return None
				e = e[s:]
			else:
				n = e[0]
				e = e[1:]
			r = ''
			#print(n,len(e))
			if n:
				if n > len(e):
					self.error = True
					return None
				r = e[:n]
				e = e[n:]
			if 32 & i:
				t.append(self.parse(r))
			else:
				if 128 & i:
					t.append(self.value(4,r))
				else:
					t.append(self.value(31 & i, r))
		return t

	def value(self,e, t):
		#print(e,len(t))
		if e == 1:
			if t:
				return True
			else:
				return False
		elif e == 2:
			return t
		elif e == 3:
			return self.parse(t[1:])
		elif e == 5:
			return None
		elif e == 6:
			i = []
			n = t[0]
			i.append(math.floor(n / 40))
			i.append(n - 40 * i[0])
			s = []
			r = 0
			for a in range(1,len(t)):
				o = t[a]
				s.append(127 & o)
				if 128 & o:
					r += 1
				else:
					tmp = 0
					for c in range(len(s)):
						tmp += s[c] * pow(128, r)
						r -= 1
					i.append(tmp)
					r = 0
					s = []
			sret = ''
			for sr in range(len(i)):
				sret += "%d"%(i[sr])
				if sr != len(i) - 1:
					sret += '.'
			return sret
		return None





'''
var RSA = {
getPublicKey: function (e) {
	if (e.length < 50) return !1;
	if ('-----BEGIN PUBLIC KEY-----' != e.substr(0, 26)) return !1;
	e = e.substr(26);
	if ('-----END PUBLIC KEY-----' != e.substr(e.length - 24)) return !1;
	e = e.substr(0, e.length - 24);
	e = new ASN1Data(Base64.decode(e));
	if (e.error) return !1;
	e = e.data;
	if ('1.2.840.113549.1.1.1' == e[0][0][0]) return new RSAPublicKey(e[0][1][0][0], e[0][1][0][1]);
 	else return !1
},

encrypt: function (e, t) {
	if (!t) return !1;
	var i = t.modulus.bitLength() + 7 >> 3;
	e = this.pkcs1pad2(e, i);
	if (!e) return !1;
	e = e.modPowInt(t.encryptionExponent, t.modulus);
	if (!e) return !1;
	e = e.toString(16);
	for (; e.length < 2 * i; ) e = '0' + e;
	return Base64.encode(Hex.decode(e))
},

decrypt: function (e) {
	var t = new BigInteger(e, 16)
},

pkcs1pad2: function (e, t) {
	if (t < e.length + 11) return null;
	var i = [
];
var n = e.length - 1;
for (; n >= 0 && t > 0; ) i[--t] = e.charCodeAt(n--);
i[--t] = 0;
for (; t > 2; ) i[--t] = Math.floor(254 * Math.random()) + 1;
i[--t] = 2;
i[--t] = 0;
return new BigInteger(i)
}
};
'''

class RSA:
	def __init__(self):
		print('new RSA')

	def getPublicKey(self, e):
		if len(e) < 50:
			return False
		if '-----BEGIN PUBLIC KEY-----' != e[:26]:
			return False
		e = e[26:]
		if '-----END PUBLIC KEY-----' != e[-24:]:
			return False
		e = e[:-24]
		e = ASN1Data(base64.b64decode(e))
		if e.error:
			return False
		e = e.data
		if '1.2.840.113549.1.1.1' == e[0][0][0]:
			return RSAPublicKey(e[0][1][0][0], e[0][1][0][1])
		else:
			return False

	'''
	pkcs1pad2: function (e, t) {
		if (t < e.length + 11) return null;
		var i = [];
		var n = e.length - 1;
		for (; n >= 0 && t > 0; ) i[--t] = e.charCodeAt(n--);
		i[--t] = 0;
		for (; t > 2; ) i[--t] = Math.floor(254 * Math.random()) + 1;
		i[--t] = 2;
		i[--t] = 0;
		return new BigInteger(i)
	}
	'''
	def pkcs1pad2(self, e, t):
		if t < len(e) + 11:
			return None
		i = [0 for o in range(t)]
		n = len(e) - 1
		while n >= 0 and t > 0:
			t -= 1
			i[t] = ord(e[n])
			n-=1
		t-=1
		i[t] = 0
		while t > 2:
			t-=1
			i[t] = math.floor(254 * random.random()) + 1
		t-=1
		i[t] = 2
		t-=1
		i[t] = 0
		i = [0, 2, 62, 44, 61, 212, 156, 15, 229, 170, 228, 22, 183, 110, 24, 196, 134, 2, 9, 235, 185, 52, 240, 39, 200, 52, 72, 252, 131, 131, 149, 152, 35, 103, 112, 168, 65, 204, 118, 3, 88, 130, 104, 233, 9, 237, 80, 143, 113, 238, 91, 28, 208, 74, 42, 20, 223, 199, 141, 29, 221, 72, 81, 38, 11, 53, 183, 251, 248, 208, 229, 85, 88, 152, 28, 128, 172, 182, 195, 40, 188, 163, 157, 250, 119, 118, 163, 31, 12, 145, 71, 45, 5, 18, 180, 122, 47, 61, 67, 4, 101, 150, 108, 149, 45, 167, 106, 71, 163, 147, 179, 30, 64, 112, 174, 103, 196, 247, 0, 115, 108, 49, 57, 57, 52, 51, 49, 55]
		return BigInteger(i)


	'''
	encrypt: function (e, t) {
		if (!t) return !1;
		var i = t.modulus.bitLength() + 7 >> 3;
		e = this.pkcs1pad2(e, i);
		if (!e) return !1;
		e = e.modPowInt(t.encryptionExponent, t.modulus);
		if (!e) return !1;
		e = e.toString(16);
		for (; e.length < 2 * i; ) e = '0' + e;
		return Base64.encode(Hex.decode(e))
	},
	'''
	def encrypt(self,e ,t):
		if not t:
			return False
		if t.modulus.content['t'] <= 0:
			i = 7 >> 3
		else:
			i = t.modulus.bnBitLength() + 7 >> 3;
		e = self.pkcs1pad2(e, i)
		if not e:
			return False
		#e = e.modPowInt(t.encryptionExponent, t.modulus);
		if not e:
			return False
		print(e.content)
		e = e.bnToString(16)
		while len(e) < 2 * i:
			e = '0'+e
		print(e)
		#return base64.encode(Hex.decode(e))
		return base64.b64encode(codecs.decode(e,"hex"))

'''
encrypt2: function (e) { // e是密码，l是公钥
  var t = RSA.getPublicKey(l);
  return RSA.encrypt(e, t)
},
'''
def encrypt(pk="", pw=""):
	print("encrypt pw: %s"%(pw))
	rsa = RSA()
	t = rsa.getPublicKey(pk)
	#print(t.modulus.content)
	#print(t.encryptionExponent.content)
	print(rsa.encrypt(pw,t))

def main():
	print("crack 163 mail")
	pk = "-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5gsH+AA4XWONB5TDcUd+xCz7ejOFHZKlcZDx+pF1i7Gsvi1vjyJoQhRtRSn950x498VUkx7rUxg1/ScBVfrRxQOZ8xFBye3pjAzfb22+RCuYApSVpJ3OO3KsEuKExftz9oFBv3ejxPlYc5yq7YiBO8XlTnQN0Sa4R4qhPO3I2MQIDAQAB-----END PUBLIC KEY-----"
	pw = 'sl1994317'

	encrypt(pk,pw)

if __name__ == '__main__':
	main()