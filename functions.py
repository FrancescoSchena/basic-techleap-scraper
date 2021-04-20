from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
import re

if __name__ == "__main__":
	print("Not supposed to be run this way")

# Printing functions
def line(number=1):
	print("\n"*number)
	return

# Generating list of company links
def get_complink(link, complinks):
	fancy_link= link.replace("_", "")
	url = "https://finder.techleap.nl" + fancy_link
	keepgoing = False
	try:
		req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
		page = urlopen(req)
		keepgoing = True
	except Exception as e:
		print("error:\t" + str(e))
	soup = BeautifulSoup(page, 'html.parser')
	
	for href in soup.find_all('a'):
		templink = href.get('href')
		if fancy_link.split("/")[-1] in templink and "http" in templink:
			save = True
			for domain in ["facebook", "google", "linkedin", "twitter", "apple", "dealroom"]:
				if domain in templink:
					save = False
			if save:
				complinks.append(templink)


# Searching each link for emails
def get_email(link, compmails):
	try:
		req = urllib.request.Request(link, headers={'User-Agent' : "Magic Browser"}) 
		con = urlopen(req)
		keepgoing = True
	except Exception as e:
		print(f" * * * Error opening {link}")
		print(" * * * " + str(e))
		keepgoing = False
	if keepgoing:
		mailexists = False
		s = con.read().decode("utf-8")
		emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", s)
		newemails = list(set(emails))
		for mail in newemails:
			if mail.split(".")[-1] == link.split(".")[-1]:  # Checks the .com/whateves
				mailexists = True
				try:
					compmails[link].append(mail)
				except KeyError:
					compmails[link] = [mail]
		if not mailexists:
			try:
				if link[-1] == "/":
					spacer = ""
				else:
					spacer = "/"
				req = urllib.request.Request(link + spacer + "contact", headers={'User-Agent' : "Magic Browser"}) 
				con = urlopen(req)
				keepgoing = True
			except Exception as e:
				print(f" * * * Error opening {link + spacer + 'contact'}")
				print(" * * * " + str(e))
				keepgoing = False
			if keepgoing:
				s = con.read().decode("utf-8")
				emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", s)
				newemails = list(set(emails))
				for mail in newemails:
					if mail.split(".")[-1] == link.split(".")[-1]:  # Checks the .com/whateves
						mailexists = True
						try:
							compmails[link].append(mail)
						except KeyError:
							compmails[link] = [mail]
		