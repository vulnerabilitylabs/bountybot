### Importing Libs
import bountybotlibrary as bb
from backports import configparser
import os,datetime,requests,json

### Read Config
config = configparser.ConfigParser()
config.read("settings.ini")

### Settins
ownpath = os.getcwd()
settings = config["Settings"]
vulns = config["Vulnerabilities"]
variable_timeout = int(settings["RequestTimeout"])

### Banner
bb.printbanner()

### Options
option = input("1) Get list from github.com/arkadiyt/bounty-targets-data\n2) Get list from txt\nSelect : ")
if option == "1":
	websites = requests.get('https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/master/data/domains.txt').text.split("\n")
	pass
elif option == "2":
	path = input("Get file path : ")
	websites = open(path, "r").read().split("\n")
	pass

### Creating Results Directory
try:
	os.mkdir("Results")
	pass
except Exception as e:
	pass

### Checking
for website in websites:
	output = ""
	server = ""
	if "/" in website:
		website = website.split("/")[0]
		pass

	if vulns["nopasswordmysql"] == "1":
		if bb.trymysql(website,3306,int(settings["MysqlFTPTimeout"]))==True:
			output = output + "\n\nMysql (No Password)\nHost : "+website+"\nPort : 3306"
			pass
		if bb.trymysql(website,9306,int(settings["MysqlFTPTimeout"]))==True:
			output = output + "\n\nMysql (No Password)\nHost : "+website+"\nPort : 9306"
			pass
		pass

	if vulns["nopasswordftp"] == "1":
		if bb.tryftp(website,int(settings["MysqlFTPTimeout"])) == True:
			output = output + "\n\nFtp (No Password)\nHost : " + website
			pass
		pass

	if vulns["unclaimedsocialmedialinks"] == "1":
		results = bb.getunclaimedsocialmedia(website,variable_timeout)
		resultsjson = json.dumps(results)
		if bool(results) != False:
			output = output + "\n\nUnclaimed Social Media : " + json.dumps(resultsjson)
			pass
		pass

	if vulns["hostinjection"] == "1":
		if bb.hostinjection(website,variable_timeout) == True:
			output = output + "\n\nHost Injection Detected!"
			pass
		pass


	if vulns["useragentbasedsql"] == "1":
		if bb.useragentsql(website,variable_timeout) == True:
			output = output + "\n\nUser Agent Based SQL Injection Detected!"
			pass
		pass

	if output != "":
		writer = open("Results/"+website+".txt","a") 
		writer.write(str(datetime.datetime.now())+"\nBountyBot 1.0\ngithub.com/xyele\ntwitter.com/rootxyele")
		writer.write("\nTarget : " + website)
		writer.write(output)
		writer.close()
		pass
	print("["+str(datetime.datetime.now())+"] Checked - " + website)
	pass
