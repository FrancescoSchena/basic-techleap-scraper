from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
import re

if __name__ == "__main__":
	print("Not supposed to be run this way")

# Generating list of company links
def get_complink(link, complinks):
	url = "https://finder.techleap.nl" + link
	page = urlopen(url)
	soup = BeautifulSoup(page, 'html.parser')
	
	fancy_link= link.replace("_", "")
	save = True
	for href in soup.find_all('a'):
		templink = href.get('href')
		if fancy_link.split("/")[2] in templink and "http" in templink:
			for domain in ["facebook", "google", "linkedin", "twitter", "apple"]:
				if domain in templink:
					save = False
			if save:
				complinks.append(templink)


# Searching each link for emails
def get_email(link, compmails):
	print("*"*10)
	print(link)
	try:
		req = urllib.request.Request(link, headers={'User-Agent' : "Magic Browser"}) 
		con = urlopen(req)
	except Exception as e:
		pass
	s = con.read().decode("utf-8")
	emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", s)
	newemails = list(set(emails))
	for mail in newemails:
		if mail.split(".")[-1] == link.split(".")[-1] and "%20" not in mail:
			try:
				compmails[link].append(mail)
			except KeyError:
				compmails[link] = [mail]
			print(link, "\t", mail)
	print("*"*35)