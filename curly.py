'''_____________________________________________________________________
|[] R3DXPL0IT SHELL                                            |ROOT]|!"|
|"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""|"| 
|CODED BY > R3DXPLOIT(JIMMY)                                          | |
|EMAIL > RETURN_ROOT@PROTONMAIL.COM                                   | |
|GITHUB > https://github.com/r3dxpl0it                                | |
|WEB-PAGE > https://r3dxpl0it.Github.io                               |_|
|_____________________________________________________________________|/|
''' 
# imports 
import re
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import os 
from urllib.parse import urlsplit
import socket 
import requests
import string 
import http.cookiejar
from random import Random
import sys
import time
#globals 
global action
global crawler
global form
global init1
global request
global Form_Debugger
global Uri_Checker
global Crawler_Handler

def request(referer,action,form,opener,cookie):

    data = urllib.parse.urlencode(form)
    if cookie != '': 
        headers = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
                'Set-Cookie' : cookie,
                'Referer' : referer
                } 
    else:
        headers = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
                'Referer' : referer
                } 
    try:
        return opener.open(action,data).read()

    except urllib.error.HTTPError: 
        print("[ERROR] HTTP Error 1 : "+action) 
        return

    except ValueError: 
        print("[ERROR] Value Error : "+action) 
        return

    except Exception as e:
        return ("[ERROR] "  , e  ,  action) 
	
def inputin():

	web = input('[INPUT] Enter target address :> ') 
	if 'https' in web : 
		web = web.split('//')[1]
	if 'http' not in web: 
		web = 'http://' + web

	web0 = web.split('//')[1]
	try:
		print('[VERBOSE]' , 'Testing site status...')
		socket.gethostbyname(web0) # test whether site is up or not
		print('[INFO] ' , 'Site seems to be up!')

	except socket.gaierror: # if site is down
		print('[INFO]' , ' Site seems to be down...')
		sys.exit(0)

	cook = input('[VERBOSE]  Got any cookies? '+'[Enter for None]'+' :> ')
	if web.endswith('/'):
		return web, cook
	else:
		web = web + '/' 
		return web, cook

class Uri_Checker : 
	def buildUrl(url, href): 

		exclusions = 'logout action=out action=logoff action=delete UserLogout osCsid file_manager.php'
		if href == "http://localhost" or any((re.search(s,href)) for s in exclusions.split()):
			return '' # csrf stuff :o

		url_parts = urlsplit(url) 
		href_parts = urlsplit(href)
		app = '' 

		if href_parts.netloc == url_parts.netloc:
			app = href # assuming this url is built

		else:
			if len(href_parts.netloc) == 0 and (len(href_parts.path) != 0 or len(href_parts.query) != 0): # parse result
				domain = url_parts.netloc # done!
				if href_parts.path.startswith('/'):
					app = 'http://' + domain + href_parts.path # startpage dom
				else:
					try:
						app = 'http://' + domain + re.findall('(.*\/)[^\/]*', url_parts.path)[0] + href_parts.path
						# get real protocol urls
					except IndexError:
						app = 'http://' + domain + href_parts.path
				if href_parts.query:
					app += '?' + href_parts.query # parameters :D

		return app

	def buildAction(url, action):

		print('[VERBOSE]',  'Parsing URL parameters...')
		if action and not re.match('#', action): 
			return buildUrl(url, action)
		else:
			return url 

buildUrl = Uri_Checker.buildUrl
buildAction = Uri_Checker.buildAction

class Form_Debugger():
	def prepareFormInputs(self, form):
			print('[VERBOSE]' , ' Crafting inputs as form type...')
			print('[VERBOSE]' , ' Parsing final inputs...')
			input = dict()
			print('[VERBOSE]' , 'Processing'+' <input type="hidden" name="...') 
			for m in form.findAll('input',{'name' : True,'type' : 'hidden'}):
					if re.search(' value=',m.__str__()):
						value=m['value'].encode('utf8') 
					else:
						value=randString()
					input[m['name']] = value 

			print('[VERBOSE]' , 'Processing '+'<input type="test" name="...') 
			for m in form.findAll('input',{'name' : True,'type' : 'text'}):
					if re.search(' value=',m.__str__()):
						value=m['value'].encode('utf8') 
					else:
						value=randString()
					input[m['name']] = value 

			print('[VERBOSE]' , 'Processing'+' <input type="password" name="...') 
			for m in form.findAll('input',{'name' : True,'type' : 'password'}):
					if re.search(' value=',m.__str__()):
						value=m['value'].encode('utf8') 
					else:
						value=randString()
					input[m['name']] = value 

			print('[VERBOSE]' , ' Processing <input type="submit" name="...')
			for m in form.findAll('input',{'name' : True,'type' : 'submit'}):
					if re.search(' value=',m.__str__()):
						value=m['value'].encode('utf8') 
					else:
						value=randString()
					input[m['name']] = value 

			print('[VERBOSE]' , ' Processing <input type="checkbox" name="...') 
			for m in form.findAll('input',{'name' : True,'type' : 'checkbox'}):
					if re.search(' value=',m.__str__()):
						value=m['value'].encode('utf-8') 
					else:
						value=randString()
					input[m['name']] = value 

			print('[VERBOSE]' , ' Processing <input type="radio" name="...') 
			listRadio = []
			for m in form.findAll('input',{'name' : True,'type' : 'radio'}):
					if (not m['name'] in listRadio) and re.search(' value=',m.__str__()):
						listRadio.append(m['name'])
						try : 
							input[m['name']] = value.encode('utf-8') 
						except : 
							input[m['name']] = value
			print('[VERBOSE]' , ' Processing <textarea name="...')
			for m in form.findAll('textarea',{'name' : True}):
					if len(m.contents)==0:
						m.contents.append(randString()) 
					try : 
						input[m['name']] = m.contents[0].encode('utf8') 
					except : 
						input[m['name']] = value
			print('[VERBOSE]' , 'Processing  <select name="...') 
			for m in form.findAll('select',{'name' : True}):
					if len(m.findAll('option',value=True))>0:
						name = m['name'] 
						input[name] = m.findAll('option',value=True)[0]['value'].encode('utf8') 

			return input

def randString(): 
	print('Compiling strings...')
	return ''.join( Random().sample(string.ascii_letters, 6)) 

def getAllForms(soup): 
	return soup.findAll('form',action=True,method=re.compile("post", re.IGNORECASE)) 		

class Crawler_Handler():

	def __init__(self, start,opener):

		self.visited = [] 
		self.toVisit = [] 
		self.uriPatterns = [] 
		self.currentURI = ''; 
		self.opener = opener; 
		self.toVisit.append(start) 

	def __next__(self):
		self.currentURI = self.toVisit[0] 
		self.toVisit.remove(self.currentURI) 
		return self.currentURI

	def getVisited(self):
		return self.visited 

	def getToVisit(self):
		return self.toVisit 

	def noinit(self):
		if len(self.toVisit) > 0:
				return True 
		else:
				return False 

	def addToVisit(self,Uri_Checker):
		self.toVisit.append(Uri_Checker) 

	def process(self, root):
		url = self.currentURI 

		try:
				query = self.opener.open(url)

		except urllib.error.HTTPError as msg:
				print('Request Error: '+msg.__str__()) 
				if url in self.toVisit:
					self.toVisit.remove(url)
				return

		if not re.search('html',query.info()['Content-Type']):
				return

		print('[INFO] Making request to new location...')
		if hasattr(query.info(),'Location'): 
				url=query.info()['Location']
		print('[INFO] Reading response...') 
		response = query.read()

		try:
				print('[INFO] Trying to parse response...')
				soup = BeautifulSoup(response ,  'lxml') 

		except HTMLParser.HTMLParseError:
				print('[INFO] BeautifulSoup Error: '+url) 
				self.visited.append(url)

				if url in self.toVisit: 
					self.toVisit.remove(url)
				return

		for m in soup.findAll('a',href=True): 

				app = ''
				if not re.match(r'javascript:',m['href']) or re.match('http://',m['href']): 
					app = Uri_Checker.buildUrl(url,m['href'])

				if app!='' and re.search(root, app):
					while re.search(r'/\.\./',app): 
						p = re.compile('/[^/]*/../')
						app = p.sub('/',app)
					p = re.compile('\./') 
					app = p.sub('',app)

					uriPattern=removeIDs(app)
					if self.notExist(uriPattern) and app!=url:
						print('[VERBOSE]' , '[ADDED]' ,	app) 
						self.toVisit.append(app) 
						self.uriPatterns.append(uriPattern)

		self.visited.append(url) 
		return soup 

	def getUriPatterns(self): 
		return self.uriPatterns

	def notExist(self, test): 
		if (test not in self.uriPatterns): 
				return 1
		return 0

	def addUriPatterns(self,Uri_Checker): 
		self.uriPatterns.append(Uri_Checker)

	def addVisited(self,Uri_Checker): 
		self.visited.append(Uri_Checker)

def removeIDs(Uri_Checker):

	p = re.compile('=[0-9]+') 
	Uri_Checker = p.sub('=',Uri_Checker) 
	p = re.compile('(title=)[^&]*') 
	Uri_Checker = p.sub('\\1',Uri_Checker)
	return Uri_Checker
class CSRF() : 
	def xsrf_main(web , cookie): 
		form1 =  """<form action="/drupal/?q=node&amp;destination=node"  accept-charset="UTF-8" method="post" id="user-login-form">
					<div><div class="form-item" id="edit-name-wrapper">
					<label for="edit-name">Username: <span class="form-required" title="This field is required.">*</span></label>
					<input type="text" maxlength="60" name="name" id="edit-name" size="15" value="test2" class="form-text required" />
					</div>
					<div class="form-item" id="edit-pass-wrapper">
					<label for="edit-pass">Password: <span class="form-required" title="This field is required.">*</span></label>
					<input type="password" value="a9z8e7" name="pass" id="edit-pass"  maxlength="60"  size="15"  class="form-text required" />
					</div>
					<input type="submit" name="op" id="edit-submit" value="Log in"  class="form-submit" />
					<div class="item-list"><ul><li class="first"><a href="/drupal/?q=user/register" title="Create a new user account.">Create new account</a></li>
					<li class="last"><a href="/drupal/?q=user/password" title="Request new password via e-mail.">Request new password</a></li>
					</ul></div><input type="hidden" name="form_build_id" id="form-6a060c0861888b7321fab4f5ac6cb908" value="form-6a060c0861888b7321fab4f5ac6cb908"  />
					<input type="hidden" name="form_id" id="edit-user-login-block" value="user_login_block"  />
					</div></form> """
		form2 =  """<form action="/drupal/?q=node&amp;destination=node"  accept-charset="UTF-8" method="post" id="user-login-form">
					<div><div class="form-item" id="edit-name-wrapper">
					<label for="edit-name">Username: <span class="form-required" title="This field is required.">*</span></label>
					<input type="text" maxlength="60" name="name" id="edit-name" size="15" value="test2" class="form-text required" />
					</div>
					<div class="form-item" id="edit-pass-wrapper">
					<label for="edit-pass">Password: <span class="form-required" title="This field is required.">*</span></label>
					<input type="password" value="a9z8e7" name="pass" id="edit-pass"  maxlength="60"  size="15"  class="form-text required" />
					</div>
					<input type="submit" name="op" id="edit-submit" value="Log in"  class="form-submit" />
					<div class="item-list"><ul><li class="first"><a href="/drupal/?q=user/register" title="Create a new user account.">Create new account</a></li>
					<li class="last"><a href="/drupal/?q=user/password" title="Request new password via e-mail.">Request new password</a></li>
					</ul></div><input type="hidden" name="form_build_id" id="form-6a060c0861888b7321fab4f5ac6cb908" value="form-6a060c0861888b7321fab4f5ac6cb908"  />
					<input type="hidden" name="form_id" id="edit-user-login-block" value="user_login_block"  />
					</div></form> """

		Cookie0 = http.cookiejar.CookieJar() 
		Cookie1 = http.cookiejar.CookieJar() 
		try : 
			resp1 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(Cookie0)) 
			resp2 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(Cookie1)) 
		except : 
			pass
		actionDone = [] 

		csrf='' 
		init1 = web 
		form = Form_Debugger() 

		bs1=BeautifulSoup(form1 , 'lxml').findAll('form',action=True)[0] 
		bs2=BeautifulSoup(form2  , 'lxml').findAll('form',action=True)[0] 

		action = init1 
		try : 
			resp1.open(action) 
			resp2.open(action) 
		except : 
			pass	
		crawler = Crawler_Handler(init1,resp1) 
		print("[INFO] ' , 'Initializing crawling and scanning...")

		try:

			while crawler.noinit():
					url = next(crawler) 

					print('[VERBOSE]' , '[CRAWLER STATUS]', url) 

					try:
						soup=crawler.process(web)
						if not soup:
							continue; 
						i=0 
						print('[INFO] ' , 'Retrieving all forms on ' , url)
						for m in getAllForms(soup): 
							action = Uri_Checker.buildAction(url,m['action']) 
							if not action in actionDone and action!='': 
									try:
										result = form.prepareFormInputs(m) 
										r1 = request(url, action, result, resp1, cookie) 
										result = form.prepareFormInputs(m) 
										r2 = request(url, action, result, resp2, cookie) 

										if(len(csrf)>0):
											if not re.search(csrf, r2): 
													print(' [+] CSRF vulnerability Detected : ' , url+'!\n')
													try:
														if m['name']: 
															print('\n +---------+')
															print(' |	PoC	|')
															print(' +---------+\n')
															print(' [+] URL : ' +url)
															print(' [+] Name : ' +m['name'])
															print(' [+] Action : ' +m['action'])

													except KeyError: 

														print('\n +---------+')
														print(' |	PoC	|')
														print(' +---------+\n')
														print(' [+] URL : ' +url)
														print(' [+] Action : ' +m['action'])

													print('[+] Code : '++urllib.parse.urlencode(result))									

											continue;

										o2 = resp2.open(url).read() 

										try:
											form2 = getAllForms(BeautifulSoup(o2 , 'lxml'))[i] 

										except IndexError:
											print('Form Error') 
											continue; 

										print('[VERBOSE]' , 'Preparing form inputs...')
										contents2 = form.prepareFormInputs(form2) 
										r3 = request(url,action,contents2,resp2, cookie) 

										try:
											checkdiff = difflib.ndiff(r1.splitlines(1),r2.splitlines(1)) 
											checkdiff0 = difflib.ndiff(r1.splitlines(1),r3.splitlines(1)) 

											result12 = []
											for n in checkdiff:
													if re.match('\+|-',n):
														result12.append(n) 

											result13 = [] 
											for n in checkdiff0:
													if re.match('\+|-',n): 
														result13.append(n) 

											if len(result12)<=len(result13): 
													print('No CSRF Detected At : '+url)
													time.sleep(0.3)
													print('PoC of response and request...')
													try: 
														if m['name']:
															print('\n +---------+')
															print(' |	PoC	|')
															print(' +---------+\n')
															print(' [+] URL : ' +url) 
															print(' [+] Name : ' + m['name']) 
															print(' [+] Action : ' + m['action']) 

													except KeyError:

														print(color.RED+'\n +---------+')
														print(color.RED+' |	PoC	|')
														print(color.RED+' +---------+\n')
														print(color.BLUE+' [+] URL : ' +color.CYAN+url) 
														print(color.GREEN+' [+] Action : ' +color.END+ m['action']) 

													print(color.ORANGE+' [+] Code : '+color.END+ urllib.parse.urlencode(result).strip())
													print('')												

										except KeyboardInterrupt:
											print('[INFO]' , ' User Interrupt!')
											print('[INFO]' , ' Aborted!') 
											sys.exit(1)

										except: 
											pass

									except urllib.error.HTTPError as msg: 
										print('Exception : '+msg.__str__()) 

							actionDone.append(action) 
							i+=1 

					except urllib.error.URLError: 
						print('[Exception] ' , 'Raised for : '+url) 
						time.sleep(0.4)
						print('[INFO] ' , 'Moving on...')
						continue; 

			print('\n'+"Scan completed!"+'\n')

		except urllib.error.HTTPError as e:
			if str(e.code) == '403':
					print('[INFO] ' , 'HTTP Authentication Error!')
					print('[INFO] ' , 'Error Code : ' + str(e.code))
					pass

		except KeyboardInterrupt: 
			print('[INFO]' , ' User Interrupt!')
			print('[INFO] ' , 'Aborted!') 
			sys.exit(1)
			
web, cookie = inputin()
CSRF.xsrf_main(web, cookie)
